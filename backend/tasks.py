from dependencies import get_s3_client

from ml.restavration import process


async def save_file(file_name, bucket, filename):
    async for s3_client in get_s3_client():
        await s3_client.upload_file(file_name, bucket, filename)
    
    processed_file, words, tags = process(file_name, to_separate=True)
    print(words, tags)
    print('Файл сохранён')