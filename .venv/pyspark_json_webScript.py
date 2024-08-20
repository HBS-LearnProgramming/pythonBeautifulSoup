from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StringType, IntegerType, ArrayType, StructType

spark = SparkSession.builder.appName("Process JSON").getOrCreate()

schema = StructType([
    StructField("_corrupt_record", StringType(), True),
    StructField("ID", IntegerType(), True),
    StructField("Product_Name", StringType(), True),
    StructField("Price", StringType(), True),
    StructField("Rating", StringType(), True),
    StructField("URL", StringType(), True),
    StructField("product_detail", ArrayType(
        StructType([
            StructField("type_title", StringType(), True),
            StructField("type_name", ArrayType(StringType()), True)
        ])
    ), True)
])

df = spark.read.schema(schema).json("products.json")

# Show records with errors
df.filter(df["_corrupt_record"].isNotNull()).show(truncate=False)

# Show valid records
df.filter(df["_corrupt_record"].isNull()).show(truncate=False)
