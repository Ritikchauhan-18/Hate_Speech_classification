# Hate_Speech_classification
This repo contain Hate Speech detection system using machine learning , deep Learning and Transformers(BERT)

In Machine_learning_models.py file,
I use three model to train on the dataset in order to predict the class as HATE SPEECH, OFFENSIVE LANGUAGE & NEITHER.
# MODELs including Logistic regression, decision tree Classifier and Random Forest Classifier
Accuracy:
# Decision Tree = 0.880781089414183 
# Random forest  = 0.8787255909558068
near same for the above two

But i use hyperparameter tuning for Logistic regression 
Accuracy 
# logistic regression = 0.895169578622816

# Done this By using deep Learning Technique:
I have use LSTM Model
In this I have use one LSTM layer as hidden layer and dense layer with softmax as a activation function
accuracy: 0.9506

# Done This task by using Transformers bert model
I have use Bert transformer model to classify the Hate Speech, Offensive speech and Neither
# this model actually work well 
# Accuracy : 0.9141381382942


