import pandas as pd
# # For preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn_pandas import DataFrameMapper 
from sklearn.metrics import mean_squared_error, r2_score
import torch # For building the networks 
import torchtuples as tt # Some useful functions

# import pycox as pc
from pycox.datasets import metabric
from pycox.models import LogisticHazard

def say_hello():
  print('Hello_world')

def import_and_shape_data():
  interval_and_weather_merged = pd.read_csv('./interval_and_weather_merged.csv')
  interval_and_weather_merged_reyna = pd.read_csv('./reyna_interval_and_weather_merge.csv')
  df_list = [interval_and_weather_merged, interval_and_weather_merged_reyna ]
  print(interval_and_weather_merged.shape)
  print(interval_and_weather_merged_reyna.shape)
  interval_and_weather_merged = pd.concat(df_list)

  # Data Cleanup including Removing American Aster
  interval_and_weather_merged = interval_and_weather_merged[(interval_and_weather_merged['sheet_title'] != '10-14-2022 i11 American Aster') & (interval_and_weather_merged['sheet_title'] != '10-14-2022 i8 American Aster')]

  # Add status to the dataframe
  interval_and_weather_merged = interval_and_weather_merged.assign(status=1)

  # Convert to seconds for the interval
  interval_and_weather_merged['interval'] = interval_and_weather_merged['interval'] / 1000000000

  # rename same_insect column
  interval_and_weather_merged.rename(columns={'same_insect': 'same_species'}, inplace=True)

  return interval_and_weather_merged


# Creating Pycox Function
def run_pycox_on_group(df, num_durations):
  # Step 2: Split data into training, validation, and test sets
  df_test = df.sample(frac=0.2)
  df_train = df.drop(df_test.index)
  df_val = df.sample(frac=0.2)
  df_train = df.drop(df_val.index)

  cols_standardize = []
  cols_leave = ['interval', 'status', 'temp', 'dwpt', 'wspd', 'coco', 'same_species']

  standardize = [([col], StandardScaler()) for col in cols_standardize]
  leave = [(col, None) for col in cols_leave]

  x_mapper = DataFrameMapper(standardize + leave)
  x_train = x_mapper.fit_transform(df_train).astype('float32')
  x_val = x_mapper.transform(df_val).astype('float32')
  x_test = x_mapper.transform(df_test).astype('float32')

  # num_durations = 1000
  labtrans = LogisticHazard.label_transform(num_durations)
  get_target = lambda df: (df['interval'].values, df['status'].values)
  y_train = labtrans.fit_transform(*get_target(df_train))
  y_val = labtrans.transform(*get_target(df_val))
  train = (x_train, y_train)
  val = (x_val, y_val)

  # We don't need to transform the test labels
  durations_test, events_test = get_target(df_test)

  in_features = x_train.shape[1]
  num_nodes = [32, 32]
  out_features = labtrans.out_features
  batch_norm = True
  dropout = 0.1

  net = tt.practical.MLPVanilla(in_features, num_nodes, out_features, batch_norm, dropout)

  model = LogisticHazard(net, tt.optim.Adam(0.01), duration_index=labtrans.cuts)
  batch_size = 256
  epochs = 100
  bad_param = 'test'
  callbacks = [tt.cb.EarlyStopping()]
  log = model.fit(x_train, y_train, batch_size, epochs, callbacks, val_data=val, verbose=0)

  return log, model, x_test, df_test, x_mapper