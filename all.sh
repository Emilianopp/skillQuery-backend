#!/bin/bash
#test commit
cd modeling/DataPipe
python scrape.py main_exec.yaml 
python processData.py main_exec.yaml 
python predict.py main_exec.yaml 
python analyze.py main_exec.yaml