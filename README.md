## Integration and analysis were completed, documentation will be updated soon

# Data Science Qualifications

Original project goal was to gather insight on what is needed become a Data Scientist in Canada.

The project has then become larger and is now trying to encapsulate the skills required for a variety of roles across multiple locations into an analytics web app. Project description will soon be refactored to represent current goals

Below is the developmental process that has been done, any of which is subject to change as development continues.




# Data Collection 

Data was collected using a Selenium web crawler
Every available job posting correlated to the term "Data Science" was gathered. 
Exact procedure can be found in the [get_data notebook](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/1_get_data.ipynb)

Updates have been made to integrate a [data pipeline](https://github.com/Emilianopp/DataScienceReq/tree/master/modeling/DataPipe). The pipeline scrapes data and walks it through preprocess all the way to model prediction, making database calls as needed.

# Data Cleansing 

Multiple cleansing procedures such as;
* Removing major punctuation marks
* Formatting data into a Pandas readable format
* Lemmatisation
* Appropriately splitting the data
* Elimination of unrelated roles 

Procedures can be found in within the [formatting notebook](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/3_format_data.ipynb)

# Modeling
Manually finding qualifications of roles within data(404 job postings) would be extremely time inefficient and cumbersome. 
Therefore, natural language processing was used to differentiate qualification sentences from general job description sentences. 

A wide variety of models were tested and interpreted 
* Naive Bayes classifier 
* Linear Kernel Support Vector Machine
* Gaussian Radial Basis Kernel Support Vector Machine
* Long Term Short Term Memory Neural Network
* BERT transfer learning

Results were stagnant for both [SVM models and Naive Bayes Classifier](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/5.1_modelling.ipynb)(~88% accuracy on test set).
Unfortunantly [LSTM network](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/5.2_Nueral_nets.ipynb) did not work well with the data, achieving the lowest accuracy yet of 83%. [BERT](https://github.com/Emilianopp/DataScienceReq/blob/master/modeling/notebooks/BERT_classification.ipynb) transfer learning was found to be extremely accurate when used for text classification(94% accuracy), and will be used in production.


# Qualification Analytics

* Word Bigrams/Trigrams to determine common terminology of desired role
* Pie chart to encapsulate most desired technical skills
  
To do
* Location filtering
* Packages/frameworks utilized
* Cloud technologies 
* Statistical concepts (where applicable)
  
