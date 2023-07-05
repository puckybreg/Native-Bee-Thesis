# Native-Bee-Thesis
Juypter Notebook for data analysis work on Native Bee Monitoring Project
## Set-up

### Installing Dependencies

Make sure you have python 3 installed. I used python 3.9.13

Before running, it would be ideal to create a new virtual environment I use venv. With the virtual environment activated run `pip install -r requirements.txt` 

## Training and Deploying time-to-event predictor models with Python Notebooks
- To run through a traditional Cox Regression Hazards model and the PyCox Nueral Network model please see the notebook: `notebook_for_data_analysis.ipynb`
- To run Tibshirani's stacking methodology with Logistic Regression classifier model see the notebook: `Stacking_notebook.ipynb`
- To use multiple regression to derive covariate weights from survival curves see the notebook: `regression_on_survival_curve.ipynb`
