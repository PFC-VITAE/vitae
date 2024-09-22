import aiofiles
from core.interfaces.file_storage import IFileStorage


class FileStorage(IFileStorage):

    def __init__(self, path: str = "app/infra/storage/data/"):
        self.path = path

    async def save(self, file):
        async with aiofiles.open(f"{self.path + file.filename}", "wb") as aiofile:
            content = await file.read()
            await aiofile.write(content)
