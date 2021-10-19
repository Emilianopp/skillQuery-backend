# Data Pipeline Module

This python module deals with inserting and extracting data from the database
This module is also responsible for model prediction.

### Requirments 
Create a conda environment for execution with the below command

```
conda create --name <env_name> --file requirements.txt
```

### Configuration

To configure pipeline execution configure the main_exec.yaml file
alternatively create a clone of it for more costumed configuration

### Executing module from root directory

**Scrape Data:**
{PATH_TO_PYTHON_EXECUTABLE} ./scrape.py main_exec.yaml

**Process Data:**
{PATH_TO_PYTHON_EXECUTABLE} ./scrape.py main_exec.yaml

**Prediction:**
{PATH_TO_PYTHON_EXECUTABLE} ./predict.py main_exec.yaml

### Outputs

All outputs are stored into MongoDB database 