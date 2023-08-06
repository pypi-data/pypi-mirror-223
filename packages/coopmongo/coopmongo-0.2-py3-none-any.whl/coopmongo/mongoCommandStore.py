from cooptools.commandDesignPattern import CommandStore, CommandProtocol
from dataclasses import dataclass, field, asdict
import uuid
from typing import TypeVar, Dict, List
from coopmongo.mongoCollectionHandler import MongoCollectionHandler
from pydoc import locate

T = TypeVar('T')

class UuidSupportedDict(dict):
    @staticmethod
    def accommodate_uuid_serializer(x):
        if type(x) == uuid.UUID:
            return str(x)
        return x
    def __init__(self, data):
        super().__init__(x for x in data if x[1] is not None)

@dataclass(frozen=True)
class MongoCommandDocument:
    cursor: int
    command: CommandProtocol
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    obj_type: str = None

    def to_jsonable_dict(self):
        return asdict(self, dict_factory=UuidSupportedDict)

    @classmethod
    def from_(cls, base_schema=None, **kwargs):
        if base_schema is not None:
            definition = base_schema.__dict__
            for kwarg, val in kwargs.items():
                definition[kwarg] = val
        else:
            definition = kwargs

        if type(definition['id']) == str:
            definition['id'] = uuid.UUID(definition['id'])

        return cls(**definition)


    def __post_init__(self):
        if type(self.command) == dict:
            class_ = locate(self.obj_type)
            object.__setattr__(self, 'command', class_(**self.command))

        _fqn = type(self.command).__module__ + '.' + type(self.command).__qualname__
        object.__setattr__(self, 'obj_type', _fqn)

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        return asdict(self)

@dataclass(frozen=True)
class MongoCacheDocument:
    cursor: int
    state: T
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    obj_type: str = None

    def to_jsonable_dict(self):
        return asdict(self, dict_factory=UuidSupportedDict)

    @classmethod
    def from_(cls, base_schema=None, **kwargs):
        if base_schema is not None:
            definition = base_schema.__dict__
            for kwarg, val in kwargs.items():
                definition[kwarg] = val
        else:
            definition = kwargs

        if type(definition['id']) == str:
            definition['id'] = uuid.UUID(definition['id'])

        return cls(**definition)

    def __post_init__(self):
        if type(self.state) == dict:
            class_ = locate(self.obj_type)
            object.__setattr__(self, 'state', class_(**self.state))

        _fqn = type(self.state).__module__ + '.' + type(self.state).__qualname__
        object.__setattr__(self, 'obj_type', _fqn)

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        return asdict(self)

class MongoCommandStore(CommandStore):
    def __init__(self,
                 mongo_command_collection_handler: MongoCollectionHandler,
                 mongo_cache_collection_handler: MongoCollectionHandler):
        self.mongo_command_collection_handler = mongo_command_collection_handler
        self.mongo_cache_collection_handler = mongo_cache_collection_handler

    def add_command(self, command: CommandProtocol, cursor: int):
        return self.mongo_command_collection_handler.add_items([MongoCommandDocument(
            cursor=cursor,
            command=command
        )], fail_on_duplicate=False)

    def _get_command_internal(self, start_cursor: int = None, end_cursor: int = None) -> List[MongoCommandDocument]:
        cursor_query = {}
        if start_cursor is not None:
            cursor_query['$gte'] = start_cursor

        if end_cursor is not None:
            cursor_query['$lte'] = end_cursor

        return self.mongo_command_collection_handler.get_items(query={'cursor': cursor_query})

    def remove_commands(self, start_cursor: int):
        docs = self._get_command_internal(start_cursor=start_cursor)
        ids = [x.id for x in docs]

        if id in ids:
            self.mongo_command_collection_handler.delete_item(id=id)

    def get_commands(self, start_cursor: int = None, end_cursor: int = None):
        return [x.command for x in self._get_command_internal(start_cursor, end_cursor)]

    def _get_cached_internal(self):
        return self.mongo_cache_collection_handler.get_items()

    def add_cached(self, state: T, cursor: int):
        return self.mongo_cache_collection_handler.add_items([MongoCacheDocument(
            cursor=cursor,
            state=state
        )])

    def remove_cached_at_cursor(self, cursor: int):
        cached = self._get_cached_internal()
        to_delete = next(x for x in cached if x.cursor == cursor)

        self.mongo_cache_collection_handler.delete_item(id=to_delete)

    def get_cached(self) -> Dict[int, CommandProtocol]:
        return {x.cursor: x.state for x in self._get_cached_internal()}

if __name__ == "__main__":
    from dataclasses import dataclass
    import mongo_utils as utils
    from cooptools.commandDesignPattern import CommandProtocol

    @dataclass
    class StoredState:
        name: str
        dummy_1: int = 1
        dummy_2: float = 4.13

        def __hash__(self):
            return hash(self.name)

        def __eq__(self, other):
            return type(other) == StoredState and hash(other) == hash(self)

    @dataclass
    class DummyIncrementCommand(CommandProtocol):
        a: int

        def execute(self, state: T) -> T:
            pass

    uri_template = "mongodb+srv://<user>:<password>@cluster0.bfcjjod.mongodb.net/?retryWrites=true&w=majority&uuidRepresentation=standard"

    mongo_command_collection_handler = MongoCollectionHandler(
        db_name='coopmongo_test',
        collection_name='commands',
        uri=utils.connection_string_uri(user="tylertjburns",
                                        pw="Chick3nCoopDissonanc3!",
                                        uri_template=uri_template),
        dataclass_model=MongoCommandDocument
    )

    mongo_cache_collection_handler = MongoCollectionHandler(
        db_name='coopmongo_test',
        collection_name='cache',
        uri=utils.connection_string_uri(user="tylertjburns",
                                        pw="Chick3nCoopDissonanc3!",
                                        uri_template=uri_template),
        dataclass_model=MongoCacheDocument
    )


    store = MongoCommandStore(mongo_command_collection_handler=mongo_command_collection_handler,
                              mongo_cache_collection_handler=mongo_cache_collection_handler)


    store.add_command(DummyIncrementCommand(a=5), cursor=25)
    cmds = store.get_commands(0, 100)
    print(cmds)

    store.add_cached(StoredState(name='tj'), cursor=0)
    print(store.get_cached())