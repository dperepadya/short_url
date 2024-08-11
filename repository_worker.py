import json
import aiofiles
import motor.motor_asyncio
from pymongo.errors import PyMongoError


class RepositoryWorker:
    def __init__(self, *args, **kwargs):
        pass

    async def save(self, data):
        return NotImplemented

    async def load(self, query):
        return NotImplemented


class FileWorker(RepositoryWorker):
    def __init__(self, path="url_map.json", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.repository = "short_urls"

    async def save(self, data):
        try:
            key = data['short_url']
            value = data['url']
            url_map = await self.load(query=None)
            url_map[key] = value
            async with aiofiles.open(self.path, "w") as f:
                await f.write(json.dumps(url_map))
        except FileNotFoundError:
            return

    async def load(self, query):
        try:
            async with (aiofiles.open(self.path, "r") as f):
                res = await f.read()
                if res is not None:
                    json_res = json.loads(res)
                    if query is None:
                        return json_res
                    return json_res.get(query, None)
        except FileNotFoundError:
            return None

class MongoWorker(RepositoryWorker):
    def __init__(self, connection_string="mongodb://root:example@localhost:27017",
                 user_name="root", password="example",
                 host='localhost', port=27017, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if connection_string is None:
            if host is None or port is None or user_name is None or password is None:
                raise ValueError("host and port must be specified")
            self.connection_string = f"mongodb://{user_name}:{password}@{host}:{port}"
        else:
            self.connection_string = connection_string
        print(self.connection_string)
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string)
        self.db = self.client["short_url_db"]
        self.repository = "short_urls"

    async def save(self, data):
        try:
            if self.client is None:
                return False
            res = await self.db[self.repository].insert_one(data)
            return res.inserted_id
        except PyMongoError as e:
            print(f"Error saving data: {e}")
            return None

    async def load(self, query):
        try:
            res = await self.db[self.repository].find_one({'short_url': query})
            return res['url'] if res is not None else None
        except PyMongoError as e:
            print(f"Error loading data: {e}")
            return None
