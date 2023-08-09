import boto3
import requests
from tqdm import tqdm

S3_FILE_CONF = {
    "ACCESS_KEY": "a35e9409ca044e9696bee64b6a74955b",
    "SECRET_KEY": "b5a729970ad6925bd29edc6c5fa2f31960b9426896b0658654a7f113817f6c0e",
    "BUCKET_NAME": "file",
    "ENDPOINT_URL": "https://ea2399efdad8c26cba1f231fdeec938b.r2.cloudflarestorage.com",
}

# 连接s3
s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=S3_FILE_CONF["ACCESS_KEY"],
    aws_secret_access_key=S3_FILE_CONF["SECRET_KEY"],
    endpoint_url=S3_FILE_CONF["ENDPOINT_URL"],
)

url = "https://webcdn.m.qq.com/spcmgr/download/DeskGo_3_3_1482_127_full_wallpaper.exe"
response = requests.get(url, stream=True)

if response.status_code == 200:
    total_size = int(response.headers.get("content-length", 0))
    block_size = 5 * 1024 * 1024  # 缓冲区大小5M
    progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)

    content = b""
    for data in response.iter_content(block_size):
        content += data
        progress_bar.update(len(data))

    s3.put_object(
        Body=content,
        Bucket="file",
        Key="DeskGo_3_3_1482_127_full_wallpaper.exe",
    )

    progress_bar.close()
