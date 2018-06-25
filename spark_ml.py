from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.sql.functions import col

from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression

from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler

from pyspark.ml.evaluation import BinaryClassificationEvaluator,MulticlassClassificationEvaluator

#from pyspark.ml import PipelineModel

sc =SparkContext("local[2]", "Tweet Streaming App")
sqlContext = SQLContext(sc)
data = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('data.csv')

#drop_list = ['ItemID']
#data = data.select([column for column in data.columns if column not in drop_list])
data.show(5)

data.printSchema()

data.groupBy("airline_sentiment") \
    .count() \
    .orderBy(col("count").desc()) \
    .show()

data.groupBy("text") \
    .count() \
    .orderBy(col("count").desc()) \
    .show()

# set seed for reproducibility
(trainingData, testData) = data.randomSplit([0.7, 0.3], seed = 100)
print("Training Dataset Count: " + str(trainingData.count()))
print("Test Dataset Count: " + str(testData.count()))

# regular expression tokenizer
regexTokenizer = RegexTokenizer(inputCol="text", outputCol="words", pattern="\\W")

# stop words
add_stopwords = ["http","https","amp","rt","t","c","the"]
stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)

# bag of words count
countVectors = CountVectorizer(inputCol="filtered", outputCol="features", vocabSize=10000, minDF=5)

# convert string labels to indexes
label_stringIdx = StringIndexer(inputCol = "airline_sentiment", outputCol = "label")

lr = LogisticRegression(maxIter=20, regParam=0.3, elasticNetParam=0)
#lrModel = lr.fit(trainingData)


# build the pipeline
pipeline = Pipeline(stages=[regexTokenizer, stopwordsRemover, countVectors, label_stringIdx, lr])

# Fit the pipeline to training documents.
pipelineFit = pipeline.fit(trainingData)
predictions = pipelineFit.transform(testData)

predictions.filter(predictions['prediction'] == 0) \
    .select("text","airline_sentiment","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

predictions.filter(predictions['prediction'] == 1) \
    .select("text","airline_sentiment","probability","label","prediction") \
    .orderBy("probability", ascending=False) \
    .show(n = 10, truncate = 30)

# Evaluate, metricName=[accuracy | f1]default f1 measure
evaluator = MulticlassClassificationEvaluator(predictionCol="prediction",labelCol="label")
print("F1: %g" % (evaluator.evaluate(predictions)))

# save the trained model for future use
pipelineFit.save("new.model")

# PipelineModel.load("logreg.model")
