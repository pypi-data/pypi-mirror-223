from google.cloud import storage
import gcshus
import boto3


class UnsupportedService(Exception):
    pass


class UnsupportedOperation(Exception):
    pass


class Client:
    def __init__(self, service) -> None:
        if service.lower() == "gcs":
            self.storage_service = GCS()
            return

        if service.lower() == "s3":
            self.storage_service = S3()
            return

        raise UnsupportedService(f"Unsupported service: {service}")

    def upload(self, bucket, src_file, dst_file):
        self.storage_service.upload(bucket, src_file, dst_file)


class StorageService:
    def upload(self, bucket, src_file, dst_file):
        raise UnsupportedOperation("Upload operation is not supported")


class GCS(StorageService):
    def __init__(self) -> None:
        self.gcs_client = storage.Client()

    def upload(self, bucket, src_file, dst_file):
        gcshus.upload(self.gcs_client, bucket, src_file, dst_file)


class S3(StorageService):
    def upload(self, bucket, src_file, dst_file):
        boto3.resource("s3").Bucket(bucket).upload_file(src_file, dst_file)
