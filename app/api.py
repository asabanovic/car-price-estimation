from fastai.structured import *
# from sklearn.ensemble import RandomForestRegressor
import datetime


class Api:
    def load_data(self):
        self.df_raw = pd.read_feather('tmp/olx-raw')
        return self.df_raw

    def load_categorized_data(self):
        self.load_data()
        print("COLUMNS BEFORE: ", list(self.df_raw.columns))
        df_raw_categorized, y, nas = proc_df(self.df_raw, 'Price')
        print("COLUMNS AFTER PROC: ", list(df_raw_categorized.columns))
        return df_raw_categorized

    def load_prediction_model(self):
        filename = 'tmp/olx-raw-prediction.sav'
        model = pickle.load(open(filename, 'rb'))
        return model

    def get_options(self, df_raw):
        print("RAW COLUMNS: ", list(df_raw.columns))
        df_options = pd.DataFrame()
        print("First: ", df_raw.dtypes)
        print("Second: ", df_raw.columns.values)

        for column_name in self.df_raw.columns.values:
            df_options[column_name] = self.df_raw[column_name]

        print("OPTIONS: ", (df_options['Manufacturer']))
        print("CATEGORIES: ", list(df_options['Manufacturer'].dropna().unique().codes))

        manufacturers = list(zip(df_options['Manufacturer'].dropna().unique().codes,
                                 df_options['Manufacturer'].dropna().unique().categories))
        print("MANU: ", manufacturers)
        models = list(
            zip(df_options['Model'].dropna().unique().codes, df_options['Model'].dropna().unique().categories))
        fuels = list(zip(df_options['Fuel'].dropna().unique().codes, df_options['Fuel'].dropna().unique().categories))
        volumes = df_options['Volume'].dropna().unique()
        volumes = np.sort(volumes)
        print('Volume type: ', type(volumes), volumes)
        now = datetime.datetime.now()
        self.options = df_options
        return df_raw, manufacturers, now, models, fuels, volumes

    def get_models(self, brand):
        print('Inside models ...')
        print('Checking for brand: ' + brand)
        self.load_data()
        return list(self.df_raw[self.df_raw['Manufacturer'].isin([brand])].Model.values.unique())

    def get_manufacturer_code_value(self, df_raw, query_val):
        print('INSIDE MANU CODE VALUE: ', df_raw.dtypes)
        indices = dict(enumerate(df_raw['Manufacturer'].cat.categories))
        print(indices)
        for key, val in indices.items():
            print(key, val)
            if val == query_val:
                return key
        return False

    def get_model_code_value(self, df_raw, query_val):
        indices = dict(enumerate(df_raw['Model'].cat.categories))
        print(indices)
        for key, val in indices.items():
            print(key, val)
            if val == query_val:
                return key
        return False

    def format_prediction_data(self, df_raw, data):
        print("RECEIVING DATA: ", data)
        for key, index in data.items():
            print(key, index)

        data_dict = {'Manufacturer': self.get_manufacturer_code_value(df_raw, data['brand']),
                     'Model': self.get_model_code_value(df_raw, data['model']),
                     'Made': data['year'],
                     'Mileage': data['mileage'],
                     'Fuel': data['fuel'],
                     'Volume': data['volume'],
                     'Published': datetime.datetime.today().strftime('%Y-%m-%d')
                     }
        df = pd.DataFrame(data_dict, index=[0])
        add_datepart(df, 'Published')
        return df.get_values()

    def predict(self, df_raw, data):
        model = self.load_prediction_model()
        predict_data = self.format_prediction_data(df_raw, data)

        k = model.predict(predict_data)
        print("PREDICTION: (log)", k)
        print("PREDICTION: (price)", np.exp(k))
        print("PREDICTION TYPE: ", type(np.exp(k)))
        return (np.exp(k)).item(0)
