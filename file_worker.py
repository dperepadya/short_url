import json
import aiofiles

class FileWorker:
    def __init__(self, path):
        self.path = path

    async def save(self, data):
        async with aiofiles.open(self.path, "w") as f:
            await f.write(json.dumps(data))

    async def load(self):
        try:
            async with aiofiles.open(self.path, "r") as f:
                res = await f.read()
                return json.loads(res)
        except FileNotFoundError:
            return {}
