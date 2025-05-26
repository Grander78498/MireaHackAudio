import time

from dependencies import get_s3_client

def test():
    time.sleep(10)
    print('Сосал?')


async def save_file(file_name, bucket, filename):
    async for s3_client in get_s3_client():
        await s3_client.upload_file(file_name, bucket, filename)
    print('Файл сохранён')