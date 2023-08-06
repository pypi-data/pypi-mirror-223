import json
from typing import Type
from pydantic import BaseModel
from redis import Redis

from .client_factory import RedisClientFactory


class RedisRepository:
    def __init__(self, client: Redis = RedisClientFactory.get_client()):
        self.client = client

    def _get_cached_id(
        self, entity_type: str, entity_id: str, parent_collections: dict
    ) -> str:
        redis_key = ""
        for key, val in parent_collections.items():
            redis_key += f"{key}:{val}:"
        redis_key += f"{entity_type}:{entity_id}"
        return redis_key

    def _convert_to_json(
        self, data: str | int | BaseModel | dict | list[BaseModel] | list[dict]
    ) -> str | int:
        if isinstance(
            data,
            (
                str,
                int,
            ),
        ):
            return data
        if isinstance(data, dict):
            return json.dumps(data)
        if isinstance(data, BaseModel):
            return data.json()
        if isinstance(data, list):
            object_as_list_of_dicts = []
            for item in data:
                if isinstance(item, BaseModel):
                    object_as_list_of_dicts.append(item.dict())
                else:
                    object_as_list_of_dicts.append(item)
        return json.dumps(object_as_list_of_dicts)

    def set(
        self,
        entity_type: str,
        entity_id: str,
        parent_collections: dict,
        data: str | int | BaseModel | dict | list[BaseModel] | list[dict] | None,
    ):
        if not data:
            return
        self.client.set(
            self._get_cached_id(entity_type, entity_id, parent_collections),
            self._convert_to_json(data),
        )

    def get(
        self,
        entity_type: str,
        entity_id: str,
        parent_collections: dict,
        model: Type[BaseModel] | None = None,
    ) -> BaseModel | dict | str | int | list | None:
        res = self.client.get(
            self._get_cached_id(entity_type, entity_id, parent_collections)
        )
        if not res:
            return None
        if isinstance(res, int):
            return res
        try:
            loaded_res = json.loads(res)
        except json.decoder.JSONDecodeError:
            return res
        if not model:
            return loaded_res
        if isinstance(loaded_res, list):
            return [model(**item) for item in loaded_res]
        return model(**loaded_res)
