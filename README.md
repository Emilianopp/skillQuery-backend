# Data Science Qualifications

This project's goal is to gather insight on what is needed become a Data Scientist in Canada.

# Data Collection 

Data was collected using a Selenium web crawler
Every available job posting correlated to the term "Data Science" was gathered. 
Exact procedure can be found in the [get_data notebook](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/1_get_data.ipynb)

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

Results were stagnant for both [SVM models and Naive Bayes Classifier](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/5.1_modelling.ipynb)(~88% accuracy on test set).
On the contrary [LSTM network](https://github.com/Emilianopp/DataScienceReq/blob/master/notebooks/5.2_Nueral_nets.ipynb) worked extremely well on the data achieving an astounding 96% accuracy on test set. 
LSTM network was chosen as model of choice moving forward.

# Qualification Analytics

Current focus. 