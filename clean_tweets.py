import pandas as pa
import numpy as np

path = "Tweets.csv"

X = pa.read_csv(path)

#print(list(df.columns.values))
df = X['text']
df = df.dropna(how='any',axis=0) 
df = df.replace({'http\S+':''}, regex = True)
df = df.replace({'\n|\t':''}, regex = True)
df = df.replace({'RT ':''}, regex = True)
df = df.replace({'@[A-Za-z0-9:]+':''}, regex = True)
df = df.replace({'[^\.\,\'\#A-Za-z0-9 ]':''}, regex = True)

da = X['airline_sentiment']
ds = X['tweet_id']

frames = [df, da, ds]
result = pa.DataFrame()
result = pa.concat([df, da], axis=1)
print(result)
result.to_csv("data.csv", index= None)