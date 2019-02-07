# robust_forecasting
Application Load Forecasting Project@Insight
## Problem
The aim of this project is to take our current application load forecasting approach: 
1. Understand its accuracy and validity  across different types of workload
- Provide metrics and test tools as well as overall report.
2. Improve it so that its fairly accurate  across different workloads
- Push the current accuracy across workloads up so we can be fairly confident
about using it
3. Prove its robustness: 
- This means it works at different time resolutions (5s, 1m, 1h) and at different request scales ie. 1 Requests Per Second 100 Requests Per Second, 1e6 Requests Per Second, 1e10 Requests Per second.
4. Provide a  path forward  for further improvements: 
- Provide us with details on how to further improve including: What degree does
aggregation and time scale matter for forecasting. How can we further improve, etc.


## To use the code
The pipeline is built on AWS sagemaker. Upload all the three module notebooks to sagemaker, start a notebook instance, and run the following code in order:
`data_preprocessor.ipynb` This notebook will prepare the data channel in a S3 bucket to feed into the training instance. If you already have training/testing data, then skip this step and go head to train the model.

`trainer.ipynb` will train the model, deploy the model as a Sagemaker endpoint for inference. The hyperparameters are obtained from a hyperparameter tuning job with smallest RMSE. Remember to delete the endpoint if the model is no longer in use.

`predictor.ipynb` will take the test data as input, send http request to the specified model endpoint and get inference. Then followed with amazing analysis and beautiful plots (add them by yourself). 
