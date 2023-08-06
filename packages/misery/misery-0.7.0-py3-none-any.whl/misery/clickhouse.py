import dataclasses
from abc import abstractmethod
import typing
from typing import (
    Any,
    Generic,
    Iterable,
    Optional,
    Sequence,
    TypeVar,
)

from aiohttp import ClientSession
from pypika import (  # type: ignore
    ClickHouseQuery,
    Criterion,
    CustomFunction,
    Not,
    Order,
    Parameter,
    Table,
    functions as fn,
)
from pypika.terms import PseudoColumn  # type: ignore
from pypika.clickhouse.array import Array, HasAny, Field  # type: ignore
from pypika.clickhouse.search_string import Match  # type: ignore

from .core import (
    F,
    FilterType,
    NotFound,
    QueryError,
)


T = TypeVar("T")

_is_ip_address_in_range = CustomFunction("isIPAddressInRange", ["address", "prefix"])
_is_null = CustomFunction("isNull", ["x"])
_is_not_null = CustomFunction("isNotNull", ["x"])


class ClickHouseRepo(Generic[T]):
    """Implementation of the :class:`misery.Repo` protocol
    that uses aiohttp to communicate with ClickHouse.
    """

    id_field = "id"
    """Name of the ID field of an entity."""

    @property
    @abstractmethod
    def table(self) -> Table:
        """Main table of the repository.
        It is used to autogenerate SQL queries.
        """

    def __init__(self, session: ClientSession) -> None:
        """:param session: Client session for
        making HTTP requests to ClickHouse.
        """
        self.session = session

    @property
    def query(self) -> ClickHouseQuery:
        """Query to select records from the database.

        Override this property when you need
        something more complex than selecting
        all columns from the main table
        of the repository.
        """
        return ClickHouseQuery.from_(self.table).select("*")

    @property
    def _entity_type(self) -> type:
        return typing.get_args(self.__orig_bases__[0])[0]  # type: ignore

    def load(self, record: dict) -> T:
        """Map a database record to an entity.

        Override this method if needed.
        """
        return self._entity_type(**record)

    def dump(self, entity: T) -> dict:
        """Map an entity to a database record.

        Override this method if needed.
        """
        return dataclasses.asdict(entity)

    async def request_json(self, query: ClickHouseQuery) -> dict:
        query_str = str(query) + " FORMAT JSON"

        async with self.session.post(
            "/",
            data=query_str,
        ) as resp:
            if resp.status != 200:
                raise QueryError(
                    message=(await resp.read()).decode(),
                    query=query_str,
                )

            data = await resp.json()
            return data

    async def request(self, query: ClickHouseQuery) -> bytes:
        query_str = str(query)

        async with self.session.post(
            "/",
            data=query_str,
        ) as resp:
            if resp.status != 200:
                raise QueryError(
                    message=(await resp.read()).decode(),
                    query=query_str,
                )
            data = await resp.read()
            return data

    async def fetch_one(self, query: ClickHouseQuery) -> T:
        """Find a record in the database
        and map it to an entity.
        """
        data = await self.request_json(query)

        if data["rows"] < 1:
            raise NotFound

        return self.load(data["data"][0])

    async def fetch_many(self, query: ClickHouseQuery) -> Iterable[T]:
        """Find multiple records in the database
        and map them to entities.
        """
        data = await self.request_json(query)
        return map(self.load, data["data"])

    async def add(self, entity: T) -> None:
        data = self.dump(entity)
        query = (
            ClickHouseQuery.into(self.table)
            .columns(*data.keys())
            .insert(*data.values())
        )

        await self.request(query)

    async def add_many(self, entities: Iterable[T]) -> None:
        entities = list(entities)

        if len(entities) == 0:
            return

        data = self.dump(entities[0])

        query = (
            ClickHouseQuery.into(self.table)
            .columns(*data.keys())
            .insert(*[tuple(self.dump(e).values()) for e in entities])
        )

        await self.request(query)

    async def get(self, **kwargs: Any) -> T:
        query = self.query.limit(1)

        for k, v in kwargs.items():
            query = query.where(self.table[k] == v)

        return await self.fetch_one(query)

    async def get_for_update(self, **kwargs: Any) -> T:
        return await self.get(**kwargs)

    async def get_many(
        self,
        filters: Sequence[F] = (),
        order: Sequence[str] = (),
        limit: Optional[int] = None,
        page: int = 1,
        offset: int = 0,
    ) -> Iterable[T]:
        query = self._params_to_query(
            filters=filters,
            order=order,
            limit=limit,
            page=page,
            offset=offset,
        )

        return await self.fetch_many(query)

    def _params_to_query(
        self,
        filters: Sequence[F] = (),
        order: Sequence[str] = (),
        limit: Optional[int] = None,
        page: int = 1,
        offset: int = 0,
    ) -> ClickHouseQuery:
        query = self.query

        if limit is not None:
            query = query.limit(limit).offset((page - 1) * limit + offset)
        elif offset > 0:
            query = query.offset(offset)

        for field in order:
            if field.startswith("-"):
                query = query.orderby(field[1:], order=Order.desc)
            else:
                query = query.orderby(field)

        for f in filters:
            criterion = self._filter_to_criterion(f)
            query = query.where(criterion)

        return query

    def _filter_to_criterion(self, f: F) -> Criterion:
        column = self.table[f.field]
        criterion: Any = None

        if f.type == FilterType.OR:
            criterion = Criterion.any([self._filter_to_criterion(ff) for ff in f.value])
        elif f.type == FilterType.AND:
            criterion = Criterion.all([self._filter_to_criterion(ff) for ff in f.value])
        elif f.type == FilterType.EQ:
            if f.value is None:
                criterion = _is_null(column)
            else:
                criterion = column == f.value
        elif f.type == FilterType.NEQ:
            if f.value is None:
                criterion = _is_not_null(column)
            else:
                criterion = column != f.value
        elif f.type == FilterType.IEQ:
            if f.value is None:
                criterion = _is_null(column)
            else:
                criterion = column.ilike(f.value)
        elif f.type == FilterType.INEQ:
            if f.value is None:
                criterion = _is_not_null(column)
            else:
                criterion = column.not_ilike(f.value)
        elif f.type == FilterType.LT:
            criterion = column < f.value
        elif f.type == FilterType.GT:
            criterion = column > f.value
        elif f.type == FilterType.LTE:
            criterion = column <= f.value
        elif f.type == FilterType.GTE:
            criterion = column >= f.value
        elif f.type == FilterType.STARTSWITH:
            criterion = column.like(f"{f.value}%")
        elif f.type == FilterType.NSTARTSWITH:
            criterion = column.not_like(f"{f.value}%")
        elif f.type == FilterType.ENDSWITH:
            criterion = column.like(f"%{f.value}")
        elif f.type == FilterType.NENDSWITH:
            criterion = column.not_like(f"%{f.value}")
        elif f.type == FilterType.ISTARTSWITH:
            criterion = column.ilike(f"{f.value}%")
        elif f.type == FilterType.NISTARTSWITH:
            criterion = column.not_ilike(f"{f.value}%")
        elif f.type == FilterType.IENDSWITH:
            criterion = column.ilike(f"%{f.value}")
        elif f.type == FilterType.NIENDSWITH:
            criterion = column.not_ilike(f"%{f.value}")
        elif f.type == FilterType.CONTAINS:
            criterion = column.like(f"%{f.value}%")
        elif f.type == FilterType.NCONTAINS:
            criterion = column.not_like(f"%{f.value}%")
        elif f.type == FilterType.ICONTAINS:
            criterion = column.ilike(f"%{f.value}%")
        elif f.type == FilterType.NICONTAINS:
            criterion = column.not_ilike(f"%{f.value}%")
        elif f.type == FilterType.IN:
            criterion = column.isin(f.value)
        elif f.type == FilterType.NIN:
            criterion = column.notin(f.value)
        elif f.type == FilterType.MATCHES:
            criterion = Match(column, f.value)
        elif f.type == FilterType.NMATCHES:
            criterion = Not(Match(column, f.value))
        elif f.type == FilterType.IMATCHES:
            criterion = Match(column, "(?i)" + f.value)
        elif f.type == FilterType.NIMATCHES:
            criterion = Not(Match(column, "(?i)" + f.value))
        elif f.type == FilterType.IPIN:
            criterion = _is_ip_address_in_range(column, f.value)
        elif f.type == FilterType.NIPIN:
            criterion = Not(_is_ip_address_in_range(column, f.value))
        elif f.type == FilterType.HASANY:
            criterion = HasAny(column, Array(list(f.value)))

        if f.not_:
            return Not(criterion)

        return criterion

    async def get_first(
        self, filters: Sequence[F] = (), order: Sequence[str] = ()
    ) -> T:
        try:
            return list(await self.get_many(filters, order=order, limit=1))[0]
        except IndexError:
            raise NotFound

    async def update(self, entity: T) -> None:
        """Don't use this method in production
        because ClickHouse isn't good at updating records.
        """

        old_entity = await self.get(**{self.id_field: getattr(entity, self.id_field)})
        old_record = self.dump(old_entity)
        record = self.dump(entity)
        query = ClickHouseQuery.update(self.table)

        for k, v in record.items():
            if old_record[k] != record[k]:
                query = query.set(k, v)

        query = query.where(self.table[self.id_field] == getattr(entity, self.id_field))
        await self.request(query)

    async def delete(self, **kwargs: Any) -> None:
        """Don't use this method in production
        because ClickHouse isn't good at deleting records.
        """

        query = ClickHouseQuery.from_(self.table).delete()

        if kwargs:
            for k, v in kwargs.items():
                query = query.where(self.table[k] == v)
        else:
            query = query.where(PseudoColumn(1) == 1)

        await self.request(query)

    async def exists(self, **kwargs: Any) -> bool:
        query = ClickHouseQuery.from_(self.table).select(1).limit(1)

        for k, v in kwargs.items():
            query = query.where(self.table[k] == v)

        data = await self.request_json(query)
        return data["rows"] > 0

    async def count(self, **kwargs: Any) -> int:
        query = ClickHouseQuery.from_(self.table).select(fn.Count("*"))

        for k, v in kwargs.items():
            query = query.where(self.table[k] == v)

        data = await self.request_json(query)
        return int(data["data"][0]["count()"])

    async def count_filtered(self, filter_: F) -> int:
        criterion = self._filter_to_criterion(filter_)
        query = self.query.where(criterion).distinct()
        query = ClickHouseQuery.from_(query).select(fn.Count(1))
        data = await self.request_json(query)
        return int(data["data"][0]["count()"])


class ClickHouseTransactionManager:
    """This class exists only for compatibility with the protocol
    because ClickHouse doesn't support transactions.
    It doesn't do anything to the database."""

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        pass
