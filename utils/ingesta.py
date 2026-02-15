import pandas as pd
from google.cloud import storage
from dotenv import load_dotenv
import os
load_dotenv()



def upload_to_gcs(bucket_name, file_name, object_name):
    storage_client = storage.Client.from_service_account_json(os.getenv("NAME_FILE"))
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(file_name)
    blob.make_public()