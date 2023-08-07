from google.cloud import storage
import gcshus
import boto3
import dataclasses


class UnsupportedService(Exception):
    pass


class UnsupportedOperation(Exception):
    pass


@dataclasses.dataclass
class UploadResult:
    url: str


class Client:
    def __init__(self, service) -> None:
        if service.lower() == "gcs":
            self.storage_service = GCS()
            return

        if service.lower() == "s3":
            self.storage_service = S3()
            return

        raise UnsupportedService(f"Unsupported service: {service}")

    def upload(self, bucket, src_file, dst_file) -> UploadResult:
        return self.storage_service.upload(bucket, src_file, dst_file)


class StorageService:
    def upload(self, bucket, src_file, dst_file) -> UploadResult:
        raise UnsupportedOperation("Upload operation is not supported")


class GCS(StorageService):
    def __init__(self) -> None:
        self.gcs_client = storage.Client()

    def upload(self, bucket, src_file, dst_file) -> UploadResult:
        gcshus.upload(self.gcs_client, bucket, src_file, dst_file)
        return UploadResult(f"https://storage.googleapis.com/{bucket}/{dst_file}")


class S3(StorageService):
    def upload(self, bucket, src_file, dst_file) -> UploadResult:
        boto3.resource("s3").Bucket(bucket).upload_file(src_file, dst_file)
        return UploadResult(f"https://{bucket}.s3.amazonaws.com/{dst_file}")
