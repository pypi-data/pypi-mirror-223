import unittest
import stowrap
from dotenv import load_dotenv
import tempfile
from datetime import datetime
import os

load_dotenv()


class TestUpload(unittest.TestCase):
    def upload_test_file(self, service, bucket, filename):
        with tempfile.TemporaryDirectory() as tempdir:
            testfile = os.path.join(tempdir, "test.txt")
            with open(testfile, "w") as f:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            stowrap.Client(service).upload(bucket, testfile, filename)

    def test_gcs_upload(self):
        self.upload_test_file("gcs", os.environ["TEST_GCS_BUCKET"], "test.txt")

    def test_s3_upload(self):
        self.upload_test_file("s3", os.environ["TEST_S3_BUCKET"], "test.txt")


if __name__ == "__main__":
    unittest.main()
