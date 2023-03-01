import tkinter as tk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging

logger = logging.getLogger(__name__)


class Data:
    def __init__(self, location, sheet):
        self.data = pd.read_excel(location, sheet_name=sheet)
        self.data.rename_axis(['Date'])
        self.labels = self.data['Measure']

    def get_data_toplot(self, label):
        _low = _hi = None
        row = self.data[self.data['Measure'] == label]
        a = row.drop(columns=["Category", "Measure", "Low Boundary", "High Boundary"])
        a = a.fillna(method='ffill', axis=1)
        a = a.transpose()
        if not a.empty:
            a = a.iloc[:, 0].rename('Measure')
            _low = a.apply(lambda x: row['Low Boundary'].iloc[0])
            _low = pd.DataFrame(_low).iloc[:, 0].rename('Low Boundary')
            _hi = a.apply(lambda x: row['High Boundary'].iloc[0])
            _hi = pd.DataFrame(_hi).iloc[:, 0].rename('High Boundary')
        return a, _low, _hi


class Form:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Blood Tests')
        self.toplabel = None
        self.option = tk.StringVar(self.root)
        self.om = None
        self.canvas = None
        self.data = Data("\\\MYBOOKLIVE\\Public\\Vadim Documents\\BloodTests Vadim\\Blood Test Results.xlsx", 'Vadim')

    def label_changed(self, *args):
        self.toplabel['text'] = f'You selected: {self.option.get()}'
        print(f"You selected {self.option.get()}")
        return self.drawchart()

    def drawchart(self):
        figure = plt.Figure(figsize=(20, 5), dpi=100)
        ax1 = figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(figure, self.root)
        self.canvas.get_tk_widget().grid(column=1, row=1)
        df1, l, h = self.data.get_data_toplot(self.option.get())
        if not df1.empty:
            print(df1.to_string())
            print("Lower Bound:", l.to_string())
            print("Upper Bound:", h.to_string())
            l.plot(kind='line', legend=True, ax=ax1)
            h.plot(kind='line', legend=True, ax=ax1)
            df1.plot(kind='line', legend=True, ax=ax1)
            ax1.set_title(self.option.get())
        return self.canvas

    def show(self):
        labels = self.data.labels.tolist()
        self.om = tk.OptionMenu(self.root, self.option, labels[0], *labels, command=self.label_changed)
        self.om.grid(column=0, row=0)

        self.toplabel = tk.Label(self.root)
        self.toplabel.grid(column=1, row=0)

        self.drawchart()
        self.root.mainloop()


if __name__ == '__main__':
    # test()
    _form = Form()
    _form.show()