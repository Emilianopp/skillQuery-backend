# SkillQuery 

This project was developed with the goal of accumulating the large amount of of open-source job description data into a single location. 

If you wish to contribute there are a few things that the project is missing please see the needed [Contributions](#Contributions) below. 




# Data Collection 

Data was collected using a Selenium web crawler
Every available job posting correlated to the term "Data Science" was gathered. 
Exact procedure can be found in the [get_data notebook](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/1_get_data.ipynb)

A [data pipeline](https://github.com/Emilianopp/DataScienceReq/tree/master/modeling/DataPipe) was then integrated. The pipeline scrapes data and walks it through preprocess all the way to model prediction, making database calls as needed. If you wish to apply the pipeline yourself please see the ReadMe in the pipeline directory. 

# Data Cleansing 

Multiple cleansing procedures such as;
* Removing major punctuation marks
* Formatting data into a Pandas readable format
* Lemmatisation
* Appropriately splitting the data
* Elimination of unrelated roles 

Procedures can be found in within the [formatting notebook](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/3_format_data.ipynb) and are streamlined in the pipeline. 

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

# Contributions

There are a few contributions that could be easy to add that I have not have had time to do, if you wish to implement them you may create a pull request. 

* More keyword selections like this one for [education](https://github.com/Emilianopp/skillQuery-backend/tree/master/analysis_files)
* More plots and analytics to be added to the [dashboard](https://github.com/Emilianopp/SkillQuery/tree/main/src/components/Plots)
* Bigram/n-gram analysis

  
