import os
from pathlib import Path
from typing import Optional

import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession


def setupSparkContext(spark_conf: Optional[SparkConf]) -> SparkSession:
    sparkConf = spark_conf
    if sparkConf is None:
        sparkConf = SparkConf()

    # add spark config settings for delta lake
    sparkConf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    sparkConf.set(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )

    # set the maven repository for spark to sonatype, because the default
    # is bintray.com but this one is not available one more
    sparkConf.setIfMissing(
        "spark.jars.repositories",
        "https://oss.sonatype.org/content/repositories/releases",
    )

    # download deltalake and aws s3 jar to enable aws s3 and deltalake support
    sparkConf.setIfMissing(
        "spark.jars.packages",
        "org.apache.hadoop:hadoop-aws:3.1.1,io.delta:delta-core_2.12:1.0.1",
    )

    # return spark session with 2 workers
    return (
        pyspark.sql.SparkSession.builder.master("local[2]")
        .config(conf=sparkConf)
        .getOrCreate()
    )


def main() -> None:
    spark_session = setupSparkContext(None)
    TEST_DATA_PATH = Path(
        f"{os.path.dirname(os.path.abspath(__file__))}/../../tests/testdata"
    )
    df = spark_session.read.csv(path=f"{TEST_DATA_PATH}/creditcard.csv", header=True)
    df.show(5)


if __name__ == "__main__":
    main()
