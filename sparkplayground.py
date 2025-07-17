from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark import StorageLevel

spark = SparkSession.builder \
    .appName("ImportCSV") \
    .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.memory.fraction", "0.8") \
    .getOrCreate()

df1 = spark.read.csv("movies.csv",header=True,inferSchema=True,sep=",")


df2 = spark.read.csv("ratings.csv",header=True,inferSchema=True,sep=",")

# Fait le produit cartésien complet
df_cartesian = df1.alias("df1").crossJoin(df2.alias("df2"))

# Filtre selon les colonnes ID
df_result = df_cartesian.filter(df_cartesian["df1.movieId"] == df_cartesian["df2.movieId"])


# Affiche le résultat
df_result.show()


movie_rate=df_result.groupBy('df1.movieId','df1.genres').agg(F.avg("df2.rating").alias("avg_rating"))


movie_rate.show()

top10 = movie_rate.orderBy(F.col("avg_rating").desc()).limit(10)

top10.show()

movie_rate_split = movie_rate.withColumn("genre", F.explode(F.split(F.col("genres"), "\\|")))

genre_avg_rating = movie_rate_split.groupBy("genre") \
    .agg(F.avg("avg_rating").alias("avg_genre_rating"))

genre_avg_rating.show()

top10_genre=genre_avg_rating.orderBy(F.col("avg_genre_rating").desc()).limit(10)

top10_genre.show()

als = ALS(maxIter=10,regParam=0.1,userCol="userId",itemCol="movieId",ratingCol="rating",coldStartStrategy="drop")

data=df_result.select('df1.movieId','userId','rating')

data.show()

training, test = data.randomSplit([0.3, 0.7], seed=31) #création du jeu de donnée

training.persist(StorageLevel.MEMORY_AND_DISK) 

model=als.fit(training)

test.persist(StorageLevel.MEMORY_AND_DISK) 

predictions = model.transform(test)

predictions.persist(StorageLevel.MEMORY_AND_DISK)

evaluator = RegressionEvaluator(metricName="rmse",labelCol="rating",predictionCol="prediction")

rmse = evaluator.evaluate(predictions)
print(f"Root-mean-square error = {rmse}")