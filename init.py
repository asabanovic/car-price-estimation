from flask import Flask, request, render_template
from fastai.imports import *
from fastai.structured import *
import feather
import datetime
#from pandas_summary import DataFrameSummary
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
#from IPython.display import display
#print(fastai.modules.keys())
from sklearn import metrics
app = Flask(__name__)

@app.route('/')
def hello_world():
    PATH = "data/"
    
    df_raw = pd.read_csv(f'{PATH}olx-cars-100-400.csv', low_memory=False, na_values = [''], 
                     parse_dates=["Published"]) 
    df_raw.Price = np.log(df_raw.Price)
    add_datepart(df_raw, 'Published')
    train_cats(df_raw)
    os.makedirs('tmp', exist_ok=True)
    df_raw.to_feather('tmp/olx-raw')
    df_raw = pd.read_feather('tmp/olx-raw')
    print('TYpe 1: ', type(df_raw['Model']))
    df_options = pd.DataFrame()

    for column_name in df_raw.columns.values:
        print(column_name)
        df_options[column_name] = df_raw[column_name]
        print('OPTION COLUMN: ', type(df_options[column_name]))

    manufacturers = list(zip(df_options['Manufacturer'].dropna().unique().codes, df_options['Manufacturer'].dropna().unique().categories))
    models = list(zip(df_options['Model'].dropna().unique().codes, df_options['Model'].dropna().unique().categories))
    fuels = list(zip(df_options['Fuel'].dropna().unique().codes, df_options['Fuel'].dropna().unique().categories))
    volumes = df_options['Volume'].dropna().unique()
    volumes = np.sort(volumes)
    print('Volume type: ', type(volumes), volumes)
    now = datetime.datetime.now()

    return render_template(
        'index.html',
        df=df_raw,
        manufacturers=manufacturers,
        now=now,
        models=models,
        fuels=fuels,
        volumes=volumes
    )

if __name__ == '__main__':
    app.run(debug=True)
