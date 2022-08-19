import os
import unittest
from pathlib import Path

import boto3
from botocore.config import Config
from pyspark import SparkConf

from example.main import setupSparkContext


class TestS3(unittest.TestCase):
    TEST_DATA_PATH = Path(f"{os.path.dirname(os.path.abspath(__file__))}/../testdata")
    s3_bucket = "test"
    spark_conf = None

    @classmethod
    def setUpClass(cls) -> None:
        s3_endpoint = os.environ.get("S3_ENDPOINT", "http://127.0.0.1:9000")
        s3_access_key = os.environ.get("AWS_ACCESS_KEY_ID", "minioadmin")
        s3_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "minioadmin")

        # create the s3 client
        cls.s3_client = boto3.client(
            "s3",
            endpoint_url=s3_endpoint,
            aws_access_key_id=s3_access_key,
            aws_secret_access_key=s3_secret_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )

        # create the spark config
        spark_config = SparkConf()
        spark_config.set(
            key="spark.hadoop.fs.s3a.endpoint",
            value=s3_endpoint,
        )
        spark_config.set(key="spark.hadoop.fs.s3a.access.key", value=s3_access_key)
        spark_config.set(key="spark.hadoop.fs.s3a.secret.key", value=s3_secret_key)
        # non AWS S3 needs a path style setup
        spark_config.set(key="spark.hadoop.fs.s3a.path.style.access", value="true")
        spark_config.set(
            key="spark.hadoop.fs.s3a.impl",
            value="org.apache.hadoop.fs.s3a.S3AFileSystem",
        )

        cls.spark_conf = spark_config

    def setUp(cls) -> None:
        if cls.s3_bucket not in cls.s3_client.list_buckets()["Buckets"]:
            cls.s3_client.create_bucket(Bucket=cls.s3_bucket)

    # tear down method if you want to see what has been written skip the auto teardown
    def tearDown(self) -> None:
        file_list = self.s3_client.list_objects_v2(Bucket=self.s3_bucket)
        if "Contents" in file_list:
            for obj in file_list["Contents"]:
                self.s3_client.delete_object(Bucket=self.s3_bucket, Key=obj["Key"])

        self.s3_client.delete_bucket(Bucket=self.s3_bucket)

    def testWithLocalS3Setup(self):

        # setup s3 boto client for testing
        spark_session = setupSparkContext(spark_conf=self.spark_conf)
        df = spark_session.read.csv(
            path=f"{self.TEST_DATA_PATH}/creditcard.csv", header=True
        )

        df.write.format("parquet").save("s3a://test/creditcards")

        df_creditcards = spark_session.read.format("parquet").load(
            "s3a://test/creditcards"
        )
        assert df_creditcards.count() == 284807
