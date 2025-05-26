import time

from dependencies import get_s3_client

# from ml.restavration import process

def test():
    time.sleep(10)
    print('Сосал?')


async def save_file(file_name, bucket, filename):
    async for s3_client in get_s3_client():
        await s3_client.upload_file(file_name, bucket, filename)
    
    # processed_file, words, tags = process(file_name)
    # print(words, tags)
    print('Файл сохранён')