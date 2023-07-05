# Native-Bee-Thesis
Juypter Notebook for data analysis work on Native Bee Monitoring Project.

## Background
While working at the United States Geological Survey Native Bee Lab, I devised an innovative hardware solution to perform cost-effective pollinator-monitoring by transforming donated cell phones into pollinator camera-traps. By placing these modified phones in the Patuxent wildlife preserve, we were able to capture repeated photos of individual pollen-producing blooms. I then designed and developed lightweight data pipelines to process and analyze this novel photo data. These pipelines consolidated input from various lab teams, processed over 200 GB of video and photo data, and integrated with third-party APIs, ultimately storing the combined results in a database. Alongside these contributions, I built a series of predictive models incorporating neural networks, logistic regression, and various other methods of time-to-event prediction to study the impact of ecological factors on bee abundance and diversity. These models not only influenced survey design for future bee monitoring but also had implications for environmental policy at the lab. This repo contains the models used during this project. 

## Set-up

### Installing Dependencies

Make sure you have python 3 installed. I used python 3.9.13

Before running, it would be ideal to create a new virtual environment I use venv. With the virtual environment activated run `pip install -r requirements.txt` 

## Training and Deploying time-to-event predictor models with Python Notebooks
- To run through a traditional Cox Regression Hazards model and the PyCox Nueral Network model please see the notebook: `notebook_for_data_analysis.ipynb`
- To run Tibshirani's stacking methodology with Logistic Regression classifier model see the notebook: `Stacking_notebook.ipynb`
- To use multiple regression to derive covariate weights from survival curves see the notebook: `regression_on_survival_curve.ipynb`
