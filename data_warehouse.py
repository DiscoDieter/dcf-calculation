import os
import datetime

import numpy as np
import pandas as pd
import logging
from dateutil.relativedelta import relativedelta
from scipy.optimize import fsolve

logger = logging.getLogger()


class CFCollectorandStorage:

    def __init__(self, main_path):
        self._main_path = str(main_path)
        self._cf_storage = None
        self._data_to_calc = None

    @property
    def cf_storage(self):
        return self._cf_storage

    @cf_storage.setter
    def cf_storage(self, cfstorage):
        self._cf_storage = cfstorage

    @cf_storage.deleter
    def cf_storage(self):
        del self._cf_storage

    @property
    def data_to_calc(self):
        return self._data_to_calc

    def init_or_import_cf_storage(self):
        if not os.path.exists(self._main_path + "\\cf_storage.csv"):
            with open("cf_storage.csv", 'w'):
                self._cf_storage = pd.DataFrame(columns=["dates", "cash_flows"]).set_index("dates")
        else:
            try:
                with open("cf_storage.csv", 'r') as cf:
                    self._cf_storage = pd.read_csv(cf, index_col="dates")
                    self._cf_storage.index = pd.DatetimeIndex(self._cf_storage.index)
            except pd.errors.EmptyDataError:
                self._cf_storage = pd.DataFrame(columns=["dates", "cash_flows"]).set_index("dates")

    def save_cf_storage(self):
        with open("cf_storage.csv", 'w') as csv:
            csv.write(self._cf_storage.to_csv())

    @staticmethod
    def input_cf():
        while True:
            inp = input("\nplease enter date: ")
            if inp == "":
                date = datetime.datetime.today().date()
                break
            else:
                try:
                    date = datetime.datetime.today() + datetime.timedelta(days=float(inp))
                    date = date.date()
                    break
                except SyntaxError:
                    try:
                        date = datetime.datetime.strptime(inp, '%Y-%m-%d').date()
                        break
                    except ValueError as e:
                        try:
                            date = datetime.datetime.strptime(inp, '%d.%m.%Y').date()
                            break
                        except ValueError as etwo:
                            logger.warning("date format not properly set: " + str(e) + " and: " + str(etwo))
        cf_today = float(input("please enter cash flows generated at this date: "))
        return (date, cf_today)

    def add_tuple(self, *args):
        date = args[0][0]
        cf_today = args[0][1]
        self._cf_storage.loc[pd.to_datetime(date)] = cf_today

    def clean_duplicates(self):
        self._cf_storage = self._cf_storage[~self._cf_storage.index.duplicated(keep='first')]

    def add_data_to_calc(self):
        self._data_to_calc = self._cf_storage.copy()
        self._data_to_calc["diff"] = [-(pd.Timestamp.today() - x).days/365 for x in self._data_to_calc.index]



