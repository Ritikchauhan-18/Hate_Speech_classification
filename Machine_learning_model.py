# -*- coding: utf-8 -*-
"""Frisson_Task.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18XABTkvJksc9nowSo_diLwmu_4YhQORg
"""

import pandas as pd
import numpy as np



data = pd.read_excel('/content/hatespeechdata.xlsx')

data.head()

data.info()

"""#**Data Preprocessing**"""

import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.util import pr
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stopword = set(stopwords.words('english'))



def preprocess_data(text):
  text = str(text).lower()
  text = text.replace('rt','')
  text = re.sub(r"@\w+:|@\w+",'',text)
  text = re.sub('\[.*?\]','',text)
  text = re.sub('https?://\S+|www\.\S+','',text)
  text = re.sub('<.*?>+','',text)
  text = re.sub(r'[^\w\s]','',text)
  text = re.sub('\n','',text)
  text = re.sub('\w\d\w', '', text)
  text = [word for word in text.split(' ') if word not in stopword]
  text = " ".join(text)
  return text


data["Clean_tweet"] = data["tweet"].apply(preprocess_data)

data["labels"] = data["class"].map({0: "Hate Speech", 1: "Offensive Language", 2: "Neither"})
print(data.head())



# Printing top 10 cleaned Tweets
for i in range(10):
  print(data.Clean_tweet[i])

tweet_clean = data.drop_duplicates("Clean_tweet")

data = data[["Clean_tweet",'labels']]

data.head()

unique_tweets = data.drop_duplicates("Clean_tweet")

unique_tweets.shape

unique_tweets.isnull().sum()

lemmatizer=WordNetLemmatizer()
def lemmatizing(data):
    tweet=[lemmatizer.lemmatize(word) for word in data]
    return data

unique_tweets.loc[:, 'Clean_tweet']=unique_tweets['Clean_tweet'].apply(lambda x: lemmatizing(x))

unique_tweets.labels.value_counts()

"""#**Data Visualization**"""

import seaborn as sns
import matplotlib.pyplot as plt   #for data visualization and graphical plotting
from matplotlib import style      #for styling the plot
style.use("ggplot")

fig = plt.figure(figsize=(5,5))
ax = sns.countplot(x='labels', data=unique_tweets, color='blue')

ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()

fig = plt.figure(figsize=(7,7))
colors = ('red', 'green', 'blue')
wp = {'linewidth':2, "edgecolor":'black'}
tags = unique_tweets['labels'].value_counts()
explode=(0.1,0.1,0.1)
tags.plot(kind='pie', autopct="%1.1f%%", shadow=True, colors=colors, startangle=90, wedgeprops=wp, explode=explode, label='')
plt.title("Distribution of sentiments")

unique_tweets['tweet_length'] = unique_tweets['Clean_tweet'].apply(len)

# plotting the histogram
plt.figure(figsize=(10, 6))
sns.histplot(data=unique_tweets, x='tweet_length', hue='labels', multiple='stack')
plt.title('Distribution of tweet lengths by labels')
plt.xlabel('Tweet length')
plt.ylabel('Count')
plt.show()



non_hate_tweets = unique_tweets[unique_tweets.labels=='Neither']
non_hate_tweets.head()

from wordcloud import WordCloud

text=''.join([word for word in non_hate_tweets['Clean_tweet']])
plt.figure(figsize=(20,15), facecolor='None')
wordcloud=WordCloud(max_words=500, width=1600, height=800).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most frequent words in non hate tweets", fontsize=19)
plt.show()

"""#**Convert our input features to Vectors**"""

from sklearn.feature_extraction.text import TfidfVectorizer

vect=TfidfVectorizer(ngram_range=(1,3)).fit(unique_tweets['Clean_tweet'])

feature_names=vect.get_feature_names_out()

feature_names[:20]

"""#**Spliting Our DataSet**"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

X = unique_tweets['Clean_tweet']
Y = unique_tweets['labels']
X = vect.transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

X_train.shape, X_test.shape, Y_train.shape, Y_test.shape

"""#**Model Training & Testing**"""

#Logistic Regression

Lr = LogisticRegression()
Lr.fit(X_train, Y_train)
Lr_predict = Lr.predict(X_test)
Lr_acc = accuracy_score(Lr_predict, Y_test)

print(classification_report(Y_test, Lr_predict))

cm = confusion_matrix(Y_test, Lr_predict)

# Define labels for the axes
labels = ['Hate Speech', 'Offensive Language', 'Neither']

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix for Logistic Regression")
plt.xticks(ticks=[0, 1, 2], labels=labels, rotation=45)
plt.show()

from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import GridSearchCV
# Define the grid of hyperparameters to search
grid = {'C': [0.1, 1, 10, 100], 'penalty': ['l1', 'l2', 'elasticnet', 'none']}

# Create a logistic regression object
logreg = LogisticRegression()

# Instantiate the GridSearchCV object
clf = GridSearchCV(logreg, grid, cv=5, verbose=1, n_jobs=-1)

# Fit the model to the training data
clf.fit(X_train, Y_train)

# Print the best parameters
print("Best parameters:", clf.best_params_)

# Predict on the test data
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(Y_test, y_pred)
print("Test accuracy:", accuracy)

cm = confusion_matrix(Y_test, y_pred)

# Define labels for the axes
labels = ['Hate Speech', 'Offensive Language', 'Neither']

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix for Logistic Regression")
plt.xticks(ticks=[0, 1, 2], labels=labels, rotation=45)
plt.show()

"""#**Decision tree**"""

dtree = DecisionTreeClassifier()
dtree.fit(X_train, Y_train)
dtree_pred = dtree.predict(X_test)
dtree_acc = accuracy_score(dtree_pred, Y_test)

dtree_acc

print(classification_report(Y_test, dtree_pred))

cm = confusion_matrix(Y_test, dtree_pred)

# Define labels for the axes
labels = ['Hate Speech', 'Offensive Language', 'Neither']

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix for Decision Tree Classifier")
plt.xticks(ticks=[0, 1, 2], labels=labels, rotation=45)
plt.show()

"""#**Random forest**"""

from sklearn.ensemble import RandomForestClassifier

# Instantiate the RandomForestClassifier
rfc = RandomForestClassifier()

# Fit the model to the training data
rfc.fit(X_train, Y_train)

# Predict on the test data
rfc_pred = rfc.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(Y_test, rfc_pred)
print("Test accuracy:", accuracy)
# Confusion matrix
cm = confusion_matrix(Y_test, rfc_pred)

# Define labels for the axes
labels = ['Hate Speech', 'Offensive Language', 'Neither']

# Plot the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix for Random Forest")
plt.xticks(ticks=[0, 1, 2], labels=labels, rotation=45)
plt.show()

"""#**AS the **"""



# I have use the following three models:
# Decision Tree = 0.880781089414183
# Random forest  = 0.8787255909558068


# logistic regression = 0.895169578622816 after Hyperparameter tuning






