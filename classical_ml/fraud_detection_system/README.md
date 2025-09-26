# Fraude Detection System

<p align="center">
  🚧 <br />
  <b>Under Construction</b>
</p>

- Here we design a ML system to identify fradulent credict transactions 

## System Components

1. Training Pipeline: EDA, Training pipeline, Versioning
2. Inference Pipeline: API design and deployment

## Training Pipeline

- Complete pipeline in a Kaggle Notebook: [Link](https://www.kaggle.com/code/vimukthi1997/fraud-detection#Feature-Engineering:-Upsampling)

### 1. EDA

- First step is to analyze the dataset to get the insights
- These operations are done in Jupyter Notebooks: 
    - In this case, we can utilize cloud based environments like `Vertex AI Workbench` or `AWS Sagemaker`

### 2. Running Experiments

- In this step, we run some experiments with set of configurations to identify the pipeline issue and select the best model for the deployment
- All the experiments are tracked using `Weights & Biases` and artifacts are stored in a cloud bucket using `DVC`

## Inference Pipeline

### 1. Designing an API For The Deployment

- In this step, we design a FastAPI by wrapping up the best trained model
    - Model weights are dowloaded from the cloud bucket
- It is dockerized and set up for production-grade deployment 

### 2. Deployment In The Cloud

- The API will be deployed in GCP Cloud Run 