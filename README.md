# Cloud Sage: Robust application load forecasting for predictive auto-scaling

This is a consulting project with Manifold.co



## Problem
Nowadays cloud computing is on the rise. More and more businesses deploy their web apps on cloud platforms. When users access the web apps, this process generates web traffic. On the cloud platform, the orchestration system, for example, Kubernetes, will provision resources to handle different web traffic, this is done through auto-scaling. 

However, currently the auto-scaling is usually done reactively,  this causes two problems: when the traffic is increasing, the control system couldn’t provision enough resource, this causes performance degradation, and leads to bad user experience. When the traffic is becoming light, the over-provision will cost extra money.

## Solution
To solve this problem, we need a better orchestration system with predictive auto-scaling. So we can predict the upcoming load, and adjust the provision beforehand ---in this way, the performance is guaranteed, and cost is optimized.

To achieve predictive auto-scaling, we need to forecast the web application load traffic, which is essentially HTTP request time series. 

### Model
recurrent neural network with long short term memory

### Data
the public available data, the wikipedia hourly pageview

### Pipeline
I built the entire pipeline on AWS:
Data preprocessor --> training instance --> deploy trained model as Sagemaker endpoint --> Real-time query endpoint for inference


## Demo: inference from the deployed model endpoint

## What's included in this repo:

### Time series characterization and data segmentation


 ``
Detailed evaluation of model performance from different buckets

### Data preprocessor

`src/`

### Train and deploy the model by yourself
The pipeline is built on AWS sagemaker. Upload all the three module notebooks to sagemaker, start a notebook instance, and run the following code in order:

`data_preprocessor.ipynb` will prepare the data channel in a S3 bucket to feed into the training instance. If you already have training/testing data, then skip this step and go head to train the model.

`trainer.ipynb` will train the model, deploy the model as a Sagemaker endpoint for inference. The hyperparameters are obtained from a hyperparameter tuning job with smallest RMSE. Remember to delete the endpoint if the model is no longer in use.

`predictor.ipynb` will take the test data as input, send http request to the specified model endpoint and get inference. Then followed with amazing analysis and beautiful plots (add them by yourself). 



