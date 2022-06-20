import pandas as pd
import openpyxl
from tkinter import *
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class Data:
    def __init__(self, location, sheet):
        self.data = pd.read_excel(location, sheet_name=sheet)
        self.labels = self.data['Measure']
        self.low_bound = self.data['Low Boundary']
        self.high_bound= self.data['High Boundary']

    def get_data_toplot(self, label):
        return self.data[self.data['Measure'] == label]


class Form:
    def __init__(self, data):
        try:
            self.data = data
            self.root = Tk()
            self.root.title('Blood Tests')
            self.toplabel = None
            self.metric = None
        except RuntimeError as e:
            logger.exception('Failed to load data', e)

    def label_changed(self, *args):
        self.toplabel['text'] = f'You selected: {self.metric.get()}'
        data = self.data.get_data_toplot(self.metric.get())
        print(data)

    def show(self):
        labels = self.data.labels.tolist()
        self.metric = StringVar(self.root)
        om = OptionMenu(self.root, self.metric, labels[0], *labels, command=self.label_changed)
        om.grid(column=0, row=0)
        self.root.geometry('600x400+80+80')

        rightframe = Frame(self.root)
        self.toplabel = Label(rightframe)
        self.toplabel.pack()

        plotFrame = Canvas(rightframe)
        plotFrame.pack()

        rightframe.grid(column=1, row=0)
        self.root.mainloop()


if __name__ == '__main__':
    _loc = "\\\MYBOOKLIVE\\Public\\Vadim Documents\\BloodTests Vadim\\Blood Test Results.xlsx"
    data = Data(_loc, 'Vadim')
    _form = Form(data)
    _form.show()
