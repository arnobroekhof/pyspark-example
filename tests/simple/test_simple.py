import os
import unittest
from pathlib import Path

from example.main import setupSparkContext


class TestSimple(unittest.TestCase):
    TEST_DATA_PATH = Path(f"{os.path.dirname(os.path.abspath(__file__))}/../testdata")

    def testSimple(self):
        spark_session = setupSparkContext(None)

        df = spark_session.read.csv(
            path=f"{self.TEST_DATA_PATH}/creditcard.csv", header=True
        )
        assert df.count() == 284807
