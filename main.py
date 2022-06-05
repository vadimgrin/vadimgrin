import pandas as pd
import openpyxl
from tkinter import *
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class Data:
    def __init__(self, wb, sheet):
        self.sheet = wb[sheet]
        self.measures = self.getMeasures()
        self.bounds = self.getBounds()
        self.labels = self.getLabels()

    def getData(self, **kwargs):
        data = []
        for values in self.sheet.iter_rows(**kwargs):
            data.append(values)
        return pd.DataFrame(data)

    def getMeasures(self):
        return self.getData(min_col=5, values_only=True)

    def getBounds(self):
        return self.getData(min_row=3, min_col=3, max_col=4, values_only=True)

    def getLabels(self):
        return self.getData(min_row=3, min_col=2, max_col=2, values_only=True)


class Form:
    def __init__(self, data):
        try:
            self.data = data
            self.root = Tk()
            self.root.title('Blood Tests')
            self.form = None
        except RuntimeError as e:
            logger.exception('Failed to open the file', e)

    def show(self):

        labels = self.data.labels.values
        metric = StringVar(self.root)
        w = OptionMenu(self.root, metric, labels[0], *labels)
        self.root.geometry('600x400+80+80')
        rightframe = Frame(self.root)
        toplabel = Label(rightframe)
        w.grid(column=0, row=0)
        rightframe.grid(column=1, row=0)
        self.root.mainloop()


if __name__ == '__main__':

    _loc = "\\\MYBOOKLIVE\\Public\\Vadim Documents\\BloodTests Vadim\\Blood Test Results.xlsx"
    _data = Data(openpyxl.load_workbook(_loc), 'Vadim')
    _form = Form(_data)
    print('Measures: ')
    print(_data.measures.describe())
    print('Bounds: ')
    print(_data.bounds.describe())
    print('Labels: ')
    print(_data.labels.describe())

    _form.show()
