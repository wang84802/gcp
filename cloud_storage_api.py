from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./chris-project-364416-2cbb3d0fd013.json"

bucket_name = 'chris_bucket_4'

def get_bucket_list(bucket_name):
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("")
    blobs = storage_client.list_blobs(bucket_name)

    print("Data list:")
    # get data list in bucket
    for blob in blobs:
        print(blob.name)
    print("")

get_bucket_list(bucket_name)

blob_name = 'test.csv'

def download_blob_into_memory(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    contents = blob.download_as_string()
    print(blob_name + ":")
    print(contents)

download_blob_into_memory(bucket_name, blob_name)


