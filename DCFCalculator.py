import logging
import numpy as np
from scipy.optimize import fsolve
import pandas as pd
import datetime

logger = logging.getLogger()

class DCFCalculator:

    def __init__(self, main_path, dataframe):
        self._main_path = main_path
        self.df = dataframe
        self._internal_return_rate = self.irr(self.df["cash_flows"], self.df["diff"], x0=0.1)
        self._irr_after_tax = None

    @property
    def internal_return_rate(self):
        return self._internal_return_rate

    def irr_after_tax(self):
        tax = self.df["cash_flows"].sum() * 0.25
        self.df["cash_flows"][self.df.index == datetime.date.today().strftime("%Y-%m-%d")] = self.df.loc[datetime.date.today().strftime("%Y-%m-%d")]["cash_flows"] - tax
        return self.irr(self.df["cash_flows"], self.df["diff"], x0=0.1)

    def plot(self):
        pass

    def npv(self, irr, cfs, yrs):
        return np.sum(cfs / (1. + irr) ** yrs)

    def irr(self, cfs, yrs, x0):
        return fsolve(self.npv, x0=x0, args=(cfs, yrs))[0]
