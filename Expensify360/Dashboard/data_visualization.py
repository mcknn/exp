import pickle
from numpy import datetime64
import datetime
from Expensify360.toolkit import *
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from sklearn.svm import SVR
import glob


class VisualizationManager:

    def __init__(self, user, resolution='M', lookback=100):
        self.resolution = resolution
        self.user = user
        self.lookback = lookback
        self.name = f'{self.lookback}_{self.resolution}_{self.user}'
        self.fig = None

    # TODO add a summary method
    def summary(self):
        # expenses [up/down] x% since last [period] and [increasing/decreasing] x1%/[period]
        pass

    def preprocess(self):
        """
            resolution:char
            'Y'|'M'|'W'|'D'
            default:'M'

            returns: tuple of x:datetime64, y:float
        """
        expenses = get_expenses(self.user)
        if len(expenses) == 0: return np.array([]), np.array([])

        t = pd.date_range(end=datetime.datetime.now(), periods=self.lookback, freq=self.resolution)
        t = np.unique(np.array(t).astype(f'datetime64[{self.resolution}]'))
        binned = np.zeros(self.lookback)
        # aggregate according to resolution
        for i, ele in enumerate(t):
            for expense in expenses:
                if (  # all this just to compare dates TODO: try just casting like in assignment to t
                        np.datetime_as_string(datetime64(expense.expenseDate), unit=self.resolution) ==
                        np.datetime_as_string(datetime64(ele), unit=self.resolution)
                ):
                    # have to check this, 2 will be null
                    if expense.expenseTotal:
                        binned[i] += float(expense.expenseTotal)
                    elif expense.mileageTotal:
                        binned[i] += float(expense.mileageTotal)
                    elif expense.hourTotal:
                        binned[i] += float(expense.hourTotal)
        return t, binned

    def create_plot(self):
        data = self.load_data()
        # TODO change this chart
        # TODO check for at least x timesteps
        # TODO include forecast plot
        self.fig = px.line(data, x='Time', y=['Expenses', 'Trend']).to_html()
        return self.fig

    def load_data(self):
        try:
            data = pd.read_pickle(f'{self.name}_data')
        except FileNotFoundError:
            x, y = self.preprocess()
            if x.shape[0] < 1: return None
            svr_rbf = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
            X = np.arange(x.shape[0]).reshape(-1, 1)
            data = pd.DataFrame({'Time': x, 'Expenses': y, 'Trend': svr_rbf.fit(X, y).predict(X)})
            data.to_pickle(f'{self.name}_data')
        return data

    def update(self, expense):
        date = np.datetime64(expense.expenseDate).astype(f'datetime64[{self.resolution}]')
        df = self.load_data()
        if df[df['Time'] == date]['Expenses'].shape[0] != 0:
            df[df['Time'] == date]['Expenses'] += expense_total(expense)
        else:
            # then append a new record
            # but there could be empty timesteps
            # between end of df and this record so
            # fill-forward if needed
            fill_forward = {'Time': [], 'Expense': []}
            last_record_date = df['Time'].iloc[-1]
            date_i = last_record_date + 1
            while last_record_date != date:
                fill_forward['Time'].append(date_i)
                fill_forward['Expenses'].append(0.0)
            fill_forward['Time'].append(date)
            fill_forward['Expenses'].append(expense_total(expense))

        # DEBUG
        print(df[df['Time'] == date]['Expenses'])
        print(expense.expenseDate)
        df.to_pickle(f'{self.name}_data')

    @classmethod
    def save(cls, instance):
        # create a pickle file
        f = open(instance.name, 'wb')
        # pickle the dictionary and write it to file
        pickle.dump(instance, f)
        # close the file
        f.close()

    @classmethod
    def load(cls, instance_name):
        try:
            f = open(instance_name, 'rb')
            instance = pickle.load(f)
            f.close()
        except FileNotFoundError:
            # probably won't ever happen, but just in case instatiate a new model
            user, resolution, lookback = instance_name.split('_', 2)
            instance = cls(user, resolution=resolution, lookback=lookback)  # up to user to save instance

        return instance

    @classmethod
    def load_all(cls, user):
        instances = []
        instance_files = glob.glob(f'*_{user.username}')
        for i in instance_files:
            instances.append(cls.load(i))
        return instances

    @classmethod
    def update_all(cls, user, expense):
        instances = cls.load_all(user)
        for instance in instances:
            instance.update(expense)

