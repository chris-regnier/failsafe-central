import inspect
from datetime import datetime
from typing import Iterable, List

from fastapi import Depends
from fastapi.routing import APIRoute, APIRouter
from inflection import pluralize
from sqlmodel import Session

from ..db import get_db
from ..models import BaseModel


def custom_generate_unique_id(route: APIRoute):
    parts = [route.name]
    parts.extend(route.methods)
    parts.extend(route.tags)

    return "_".join(parts)


class CollectionsAPIRouter(APIRouter):
    def __init__(self, collections: Iterable[BaseModel], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collections = collections
        for collection in self.collections:
            self.add_collection(collection)

    def add_collection(self, collection: BaseModel):
        collection_name = pluralize(collection.__tablename__)
        self.add_api_route(
            f"/{collection_name}/",
            self._collection_get(collection),
            methods=["GET"],
            response_model=List[collection],
            status_code=200,
            summary=f"Get all {collection_name}",
            description=f"Get all {collection_name}",
            tags=[f"{collection_name}"],
            generate_unique_id_function=custom_generate_unique_id,
        )
        self.add_api_route(
            f"/{collection_name}/{{id_}}",
            self._collection_get_one(collection),
            methods=["GET"],
            response_model=collection,
            status_code=200,
            summary=f"Get {collection_name} by id",
            description=f"Get {collection_name} by id",
            tags=[f"{collection_name}"],
            generate_unique_id_function=custom_generate_unique_id,
        )
        self.add_api_route(
            f"/{collection_name}/",
            self._collection_create(collection),
            methods=["POST"],
            # response_model=collection,
            status_code=201,
            summary=f"Create {collection_name}",
            description=f"Create {collection_name}",
            tags=[f"{collection_name}"],
            generate_unique_id_function=custom_generate_unique_id,
        )
        # self.add_api_route(
        #     f"/{collection_name}/{{id_}}",
        #     self._collection_update(collection, is_replace=True),
        #     methods=["PUT"],
        #     response_model=collection,
        #     status_code=200,
        #     summary=f"Replace {collection_name} at id",
        #     description=f"Replace {collection_name} at id",
        #     tags=[f"{collection_name}"],
        # )
        # self.add_api_route(
        #     f"/{collection_name}/{{id_}}",
        #     self._collection_update(collection, is_replace=False),
        #     methods=["PATCH"],
        #     response_model=collection,
        #     status_code=200,
        #     summary=f"Update {collection_name} at id",
        #     description=f"Update {collection_name} at id",
        #     tags=[f"{collection_name}"],
        # )
        # self.add_api_route(
        #     f"/{collection_name}/{{id_}}",
        #     self._collection_delete(collection),
        #     methods=["DELETE"],
        #     status_code=204,
        #     summary=f"Delete {collection_name} at id",
        #     description=f"Delete {collection_name} at id",
        # )

    def _collection_get(self, collection: BaseModel):
        arg_dict = {name: field.type_ for name, field in collection.__fields__.items()}
        params = [
            inspect.Parameter(
                name,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=arg_dict[name],
                default=None,
            )
            for name in arg_dict
        ]
        params.append(
            inspect.Parameter(
                "db",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=Session,
                default=Depends(get_db),
            )
        )
        sig = inspect.Signature(parameters=params)

        async def _base_get_resource(db: Session = Depends(get_db), **filters):
            query = db.query(collection)
            if filters:
                for key in dict.keys(filters):
                    val = dict.get(filters, key, None)
                    if key in collection.__fields__ and val is not None:
                        query = query.filter(getattr(collection, key) == val)
            collection_results = query.all()
            return collection_results

        _base_get_resource.__signature__ = sig
        _base_get_resource.__name__ = f"get_{collection.__tablename__}"

        return _base_get_resource

    def _collection_get_one(self, collection: BaseModel):
        async def get_resource(id_: int, db: Session = Depends(get_db)):
            resource = db.get(collection, id_)
            return resource

        get_resource.__name__ = f"get_{collection.__tablename__}_by_id"

        return get_resource

    def _collection_create(self, collection: BaseModel):
        params = [
            inspect.Parameter(
                collection.__tablename__,
                inspect.Parameter.KEYWORD_ONLY,
                annotation=collection,
            ),
            inspect.Parameter(
                "db",
                inspect.Parameter.KEYWORD_ONLY,
                annotation=Session,
                default=Depends(get_db),
            ),
        ]
        sig = inspect.Signature(parameters=params)
        print(sig)

        async def _base_create_resource(**kwargs):
            # put controls on the function the old fashioned way
            if len(kwargs) > 2:
                raise ValueError(
                    f"_base_create_resource only accepts two keyword arguments"
                )
            db = kwargs.pop("db")
            resource = list(dict.values(kwargs))[0]
            db.add(resource)
            db.commit()
            db.refresh(resource)
            return resource

        _base_create_resource.__signature__ = sig
        _base_create_resource.__name__ = f"create_{collection.__tablename__}"

        return _base_create_resource

    def _collection_update(self, collection: BaseModel, is_replace: bool = False):
        params = [
            inspect.Parameter(
                "id_", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=int
            ),
            inspect.Parameter(
                collection.__tablename__,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=collection,
            ),
            inspect.Parameter(
                "db",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=Session,
                default=Depends(get_db),
            ),
        ]
        sig = inspect.Signature(parameters=params)

        async def _base_update_resource(
            id_: int, resource: collection, db: Session = Depends(get_db)
        ):
            existing_resource = db.get(collection, id_)
            if existing_resource:
                if is_replace:
                    db.update(resource)
                else:
                    for key in dict.keys(resource):
                        setattr(existing_resource, key, resource[key])
                db.commit()
                # session.refresh(resource)
                return resource
            raise ValueError(f"{collection} with id {id_} not found")

        _base_update_resource.__signature__ = sig
        _base_update_resource.__name__ = f"update_{collection.__tablename__}"

        return _base_update_resource

    def _collection_delete(self, collection: BaseModel):
        async def delete_resource(id_: int, db: Session = Depends(get_db)):
            resource = db.get(collection, id_)
            if resource:
                resource.deleted_at = datetime.utcnow()
                db.update(resource)
                db.commit()
                return {"message": f"{collection} soft deleted"}

        delete_resource.__name__ = f"delete_{collection.__tablename__}"

        return delete_resource
