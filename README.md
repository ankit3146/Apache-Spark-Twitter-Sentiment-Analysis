# Apache-Spark-Twitter-Sentiment-Analysis
#### Task Description:
In the given scenario, real time twitter tweets (between 2000 to 10,000) are subjected for sentiment analysis with the help of classifier. The real time twitter tweets are streamed into EC2 server. Apache spark is used to stream twitter tweets in to EC2 server. To perform the sentiment analysis, training model of data is developed using Logistic regression model. Once the model is trained, the application will perform sentiment analysis accordingly to the real time twitter tweets. Tweepy API is used to fetch tweets. 

Github Link: https://github.com/ankit3146/Apache-Spark-Twitter-Sentiment-Analysis <br/>
Sentiment data used: https://www.kaggle.com/crowdflower/twitter-airline-sentiment/

Files <br/>
.py files:  <br/>
	1) spark_stream_listener.py – Spark streaming API and sentiment analysis of streaming tweets <br/>
	2) tweepy_stream.py	- Program to stream twitter tweets <br/>
	3) spark_ml.py – Program to train model and create pipeline <br/>
	4) clean_dataset.py – Program to clean the dataset for training model <br/>
.csv files: <br/>
	1) data.csv – Cleaned tweets for training data <br/>
	2) Tweets.csv – Airline dataset <br/>

Tools:  Spyder  <br/>
Server: AWS EC2  <br/>
Application to connect server: Putty, Puttygen and WinSCP <br/>

#### Sentiment Analysis Algorithm:
ML algorithms are used to classify tweets in positive, negative and neutral. In this task, logistic regression is used to classify tweets. The model is trained on the cleaned data from Airline twitter sentiment data. The below snippet is used to create Logistic Regression. Currently data is not passed in the below code as it becomes one of the stage in pipeline. The below model is trained on the training data. 
  
The classifier used is a multinomial classifier as the family property in not mentioned in defining the logistic regression, so it selects the classifier automatically based on the label present in data. Multinomial classification is good for predicting more than two labels. The classifier gives a F1 score of 76.679.

#### Labelling Training data
The dataset used for training in the model is already labelled. There are three labels present in the data i.e. Neutral, Positive and Negative. The model uses this dataset and StringIndexer classifies them as 0 -> Negative, 1-> Positive and 2-> Neutral.
Feature Selection
RegexTokenizer is used to convert tweets into words. On the tweets StopWordsRemover is applied to remove any words given in the add_stopwords array. The output of the StopWordsRemover is then passed as the input to countVectorizer. 
countVectorizer then counts the number of times a word is used in the sentence. This then generates the features that will be inputted to the Logistic regression model. 
 
#### Output
The sentiment analysis using the model is far better than the analysis done in the second assignment. In the second assignment, tweets were classified based on the polarity of words so the result were not perfect. 
In this assignment the model is trained to understand the behavior of words as a result it generates better output. The accuracy of the algorithm is 76.69 but this can be improved by providing a larger set of training to Logistic model. The current model only consist of ~14000 words and out of which ~9000 words are negative, 3099 are neutral and rest i.e. 2363 are positive. The dataset supplied for positive and negative are very less compared to negative. So, a larger dataset can train out algorithm finer. Also, we use K-fold cross validation with the Logistic regression, accuracy can be improved.
