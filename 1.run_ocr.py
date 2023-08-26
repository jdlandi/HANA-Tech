import os
import json
import re
from google.cloud import vision, storage

CONFIG_FILE = "_CONFIG.json"
CONFIG = {}


def load_configuration(filename: str) -> dict:
    """
    Load configuration from the given file.

    Args:
        filename (str): Name of the configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    with open(filename, "r") as file:
        return json.load(file)


CONFIG = load_configuration(CONFIG_FILE)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CONFIG["GCLOUD_WORKER_FILE"]


def upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str) -> None:
    """Uploads a file to the given GCP bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def delete_blobs(bucket_name: str) -> None:
    """Deletes all blobs in the given GCP bucket."""
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        blob.delete()

    print(f"All blobs in {bucket_name} have been deleted.")


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS"""
    mime_type = "application/pdf"
    batch_size = 2
    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(gcs_destination=gcs_destination, batch_size=batch_size)
    async_request = vision.AsyncAnnotateFileRequest(features=[feature], input_config=input_config, output_config=output_config)

    operation = client.async_batch_annotate_files(requests=[async_request])
    print("Waiting for the operation to finish.")
    operation.result(timeout=120)

    storage_client = storage.Client()

    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    blob_list = [
        blob
        for blob in list(bucket.list_blobs(prefix=prefix))
        if not blob.name.endswith("/")
    ]
    print("Output files:")
    for blob in blob_list:
        print(blob.name)

    output = blob_list[1]

    json_string = output.download_as_bytes().decode("utf-8")
    response = json.loads(json_string)

    first_page_response = response["responses"][0]
    annotation = first_page_response["fullTextAnnotation"]
    print("Finished processing")

    with open(filename.replace(".pdf", ".txt"), "w") as file:
        file.write(annotation["text"])
    print("Saved OCR Results to:", f'{filename.replace(".pdf", ".txt")}')



if __name__ == "__main__":
    DIRECTORY = os.getcwd()
    BUCKET_NAME = CONFIG["GCLOUD_BUCKET"]

    for filename in os.listdir(DIRECTORY):
        if filename.lower().endswith(".pdf"):
            source_file = os.path.join(DIRECTORY, filename)
            upload_blob(BUCKET_NAME, source_file, filename)

            gcs_source_uri = f"gs://{BUCKET_NAME}/{filename}"
            gcs_destination_uri = f"gs://{BUCKET_NAME}/{os.path.splitext(filename)[0]}"
            async_detect_document(gcs_source_uri, gcs_destination_uri)

    delete_blobs(BUCKET_NAME)
