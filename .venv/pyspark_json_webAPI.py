import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StringType, IntegerType, ArrayType, StructType

# Initialize Spark session
spark = SparkSession.builder.appName("Process JSON").getOrCreate()

# Define the schema for the JSON
schema = StructType([
    StructField("video_id", StringType(), True),
    StructField("video_title", StringType(), True),
    StructField("comments", ArrayType(
        StructType([
            StructField("author_name", StringType(), True),
            StructField("comment", StringType(), True),
            StructField("likes", IntegerType(), True)
        ])
    ), True)
])

# Read the JSON file with the defined schema
df = spark.read.schema(schema).json("youtube_review.json")

# df.printSchema()
# df.show(truncate=False)
# # Show records with errors (if any)
# df.filter(df["_corrupt_record"].isNotNull()).show(truncate=True)

# Show valid records
# df.filter(df["_corrupt_record"].isNull()).show(truncate=True)

df.filter(df["video_id"].isNull() & df["video_title"].isNull()).show(truncate=False)
