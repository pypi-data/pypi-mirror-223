import unittest
import stowrap
from dotenv import load_dotenv
import tempfile
from datetime import datetime
import os

load_dotenv()


class TestUpload(unittest.TestCase):
    def upload_test_file(self, service, bucket, filename) -> stowrap.UploadResult:
        with tempfile.TemporaryDirectory() as tempdir:
            testfile = os.path.join(tempdir, "test.txt")
            with open(testfile, "w") as f:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return stowrap.Client(service).upload(bucket, testfile, filename)

    def test_gcs_upload(self):
        result = self.upload_test_file("gcs", os.environ["TEST_GCS_BUCKET"], "test.txt")
        self.assertTrue(result.url.startswith("https://storage.googleapis.com/"))

    def test_s3_upload(self):
        bucket = os.environ["TEST_S3_BUCKET"]
        result = self.upload_test_file("s3", bucket, "test.txt")
        self.assertTrue(
            result.url.startswith(f"https://{bucket}.s3.amazonaws.com/"),
            f"url is {result.url}",
        )


if __name__ == "__main__":
    unittest.main()
