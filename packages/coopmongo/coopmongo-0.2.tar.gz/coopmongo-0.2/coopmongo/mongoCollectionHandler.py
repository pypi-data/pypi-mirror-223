import pymongo as pmon
import coopmongo.mongo_utils as utils
from typing import List, Dict, Generic, TypeVar, Callable
from coopmongo.errors import DuplicateException

T = TypeVar('T')
class MongoCollectionHandler(Generic[T]):

    def __init__(self,
                db_name: str,
                collection_name: str,
                client: pmon.MongoClient = None,
                uri: str = None,
                facade_handler: utils.DocumentFacadeHandler = None,
                dataclass_model: type = None,
                sample_doc_gen: Callable[[...], T] = None
                ):
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = client if client is not None else utils.get_client(uri)
        self.facade_handler = facade_handler
        self.dataclass_model = dataclass_model
        self.sample_doc_gen = sample_doc_gen
        self.tracked_time = {}

    @property
    def Collection(self):
        return utils.get_collection(db_name=self.db_name,
                                    collection_name=self.collection_name,
                                    client=self.client)

    @property
    def CollectionSize(self):
        return self.Collection.count_documents({})

    @property
    def CollectionSizeEstimated(self):
        return self.Collection.estimated_document_count({})

    def add_items(self, items: List[T], fail_on_duplicate: bool = True) -> List[T]:
        try:
            ret = utils.insert_documents(collection=self.Collection,
                                         jsonable_objs=items,
                                         facade_handler=self.facade_handler)
            return ret
        except DuplicateException as e:
            if fail_on_duplicate:
                raise e


    def get_items(self,
                  ids: List[str] = None,
                  query: Dict=None,
                  limit: int = None) -> List[T]:
        retrieved = utils.get_documents(self.Collection,
                                        facade_handler=self.facade_handler,
                                        dataclass_model=self.dataclass_model,
                                        query=query,
                                        ids=ids,
                                        limit=limit)
        return retrieved

    def find_item(self,
                  id: str) -> T:
        retrieved = utils.get_document(collection=self.Collection,
                                       facade_handler=self.facade_handler,
                                       id=id)
        return retrieved

    def update_item(self,
                    id: str = None,
                    update_values: Dict = None,
                    update_obj: T = None) -> T:
        return utils.update_document(collection=self.Collection,
                                     id=id,
                                     update_dict=update_values,
                                     update_obj=update_obj,
                                     facade_handler=self.facade_handler)

    def delete_item(self,
                    id: str):
        return utils.delete_document(self.Collection,
                                     id=id,
                                     facade_handler=self.facade_handler)
