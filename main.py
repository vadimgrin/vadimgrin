import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
            self.root = tk.Tk()
            self.root.title('Blood Tests')
            self.toplabel = None
            self.plotFrame = None
            self.metric = None
        except RuntimeError as e:
            logger.exception('Failed to load data', e)

    def label_changed(self, *args):
        self.toplabel['text'] = f'You selected: {self.metric.get()}'
        self.drawchart(self.plotFrame)

    def drawchart(self, container):
        figure = plt.Figure(figsize=(5, 4), dpi=100)
        ax2 = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, container)
        df2 = self.data.get_data_toplot(self.metric.get())
        df2.plot(kind='line', legend=False, ax=ax2, color='r', marker='o', fontsize=8)
        ax2.set_title(self.toplabel['text'])
        return line.get_tk_widget()

    def show(self):
        labels = self.data.labels.tolist()
        self.metric = tk.StringVar(self.root)
        om = tk.OptionMenu(self.root, self.metric, labels[0], *labels, command=self.label_changed)
        om.grid(column=0, row=0)
        self.root.geometry('600x400+80+80')

        rightframe = tk.Frame(self.root)
        self.toplabel = tk.Label(rightframe)
        self.toplabel.pack()

        self.plotFrame = tk.Canvas(rightframe)
        self.plotFrame.pack()

        graph = self.drawchart(self.plotFrame)
        graph.pack()

        rightframe.grid(column=1, row=0)
        self.root.mainloop()


if __name__ == '__main__':
    _loc = "\\\MYBOOKLIVE\\Public\\Vadim Documents\\BloodTests Vadim\\Blood Test Results.xlsx"
    data = Data(_loc, 'Vadim')
    _form = Form(data)
    _form.show()
