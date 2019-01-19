from fastai.structured import *

class Api:
    def load_data(self):
        PATH = "data/"

        self.df_raw = pd.read_csv(f'{PATH}olx-cars-100-400.csv', low_memory=False, na_values=[''],
                             parse_dates=["Published"])
        self.df_raw.Price = np.log(self.df_raw.Price)
        add_datepart(self.df_raw, 'Published')
        train_cats(self.df_raw)
        os.makedirs('tmp', exist_ok=True)
        self.df_raw.to_feather('tmp/olx-raw')
        return self.df_raw

    def get_options(self, df_raw):
        df_options = pd.DataFrame()

        for column_name in self.df_raw.columns.values:
            df_options[column_name] = df_raw[column_name]

        manufacturers = list(zip(df_options['Manufacturer'].dropna().unique().codes,
                                 df_options['Manufacturer'].dropna().unique().categories))
        models = list(zip(df_options['Model'].dropna().unique().codes, df_options['Model'].dropna().unique().categories))
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

        # print(type(self.df_raw['Manufacturer']))
        # # list(self.df_raw[self.df_raw['Manufacturer'].cat.categories.isin([brand])].Model.values.unique())
        return list(self.df_raw[self.df_raw['Manufacturer'].isin([brand])].Model.values.unique())
