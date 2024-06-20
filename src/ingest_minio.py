import os
import copy
import urllib3
from minio import Minio
from dotenv import load_dotenv

def main():
    # Disable warnings for SSL
    urllib3.disable_warnings()

    # Load environment variables from .env file
    load_dotenv("../.env")
    MINIO_ACCESSKEY = os.getenv("MINIO_ACCESSKEY")
    MINIO_SECRETKEY = os.getenv("MINIO_SECRETKEY")

    # MinIO configuration
    MINIO_URL = "localhost:9000"
    MINIO_TLS = True
    MINIO_BUCKET_NAME = "mlops-lazada"

    # Initialize Minio client
    client = Minio(
        endpoint=MINIO_URL,
        access_key=MINIO_ACCESSKEY,
        secret_key=MINIO_SECRETKEY,
        secure=MINIO_TLS,
        cert_check=False  # Ignore certificate verification
    )

    # Check if the bucket exists
    if not client.bucket_exists(MINIO_BUCKET_NAME):
        raise RuntimeError("Bucket Not Found!")

    # List objects in the bucket
    object_names = []
    res = client.list_objects(bucket_name=MINIO_BUCKET_NAME)

    for obj in res:
        object_names.append(obj.object_name)

    # Download and save objects
    object_data = []

    for name in object_names:
        res = client.get_object(bucket_name=MINIO_BUCKET_NAME, object_name=name)
        object_data.append(copy.deepcopy(res.data.decode()))

    # Write data to local files
    with open("../data/raw/dataset_items.csv", "w") as out:
        out.write(object_data[0])

    with open("../data/raw/dataset_reviews.csv", "w") as out:
        out.write(object_data[1])

    with open("../data/raw/categories.txt", "w") as out:
        out.write(object_data[2])

if __name__ == "__main__":
    main()
