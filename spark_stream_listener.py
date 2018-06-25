from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.ml import PipelineModel
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql import Row
import pandas as pd
from pyspark.sql import DataFrame
from collections import namedtuple

fields = ("text")
Tweet = namedtuple( 'Tweet', fields )

def getSparkSessionInstance(sparkConf):
    if 'sparkSessionSingletonInstance' not in globals():
        globals()['sparkSessionSingletonInstance'] = \
            SparkSession.builder.config(conf=sparkConf).getOrCreate()
    return globals()['sparkSessionSingletonInstance']


def convtoDataframe(rdd):
    spark = getSparkSessionInstance(rdd.context.getConf())
    rowRdd = rdd.map(lambda w: Tweet(w))
    df = spark.createDataFrame(rowRdd)
    model = PipelineModel.load('new.model')
    predictions = model.transform(df)
    # print(predictions.show())
    #print isinstance(predictions, DataFrame)
    predictions.toPandas().to_csv('result.csv', mode='a', header=False)

sc = SparkContext("local[2]", "Tweet Streaming App")
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)
spark = SparkSession(sc)
ssc.checkpoint( "file:/home/ubuntu/tweets/checkpoint/")
socket_stream = ssc.socketTextStream("ec2-18-191-146-13.us-east-2.compute.amazonaws.com", 5555) # Internal ip of  the tweepy streamer
lines = socket_stream.window(20)
lines.count().map(lambda x:'Tweets in this batch: %s' % x).pprint()
# If we want to filter hashtags only
lines.filter( lambda word: word.lower().startswith("#") )
lines.foreachRDD(lambda rdd: convtoDataframe(rdd))

ssc.start()
ssc.awaitTermination()
