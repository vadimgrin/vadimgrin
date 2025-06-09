import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

def plot(df):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Stacked bar chart for Total Compensation (Base + IC)
    ax1.bar(df['Year'], df['Base'], label="Base Pay", color='royalblue')
    ax1.bar(df['Year'], df['IC'], bottom=df['Base'], label="Incentive Compensation", color='lightblue')
    ax1.plot(df['Year'], df['Historic'], color='red', marker='o', linestyle='dashed', label="Historic Salary")

    # Labels and legend
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Total Compensation ($)", color='blue')
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
    ax1.legend(loc="upper left")

    plt.title("Total Compensation vs. Historic Salary")
    plt.show()

def clean_data(df):
    df = df.iloc[2:].reset_index(drop=True)  # Remove extra header rows
    df.columns = ['Index', 'Year', 'Base', 'IC', 'Total', 'Historic']  # Rename columns
    return df.drop(columns=['Index']).astype({'Year': int, 'Base': float, 'IC': float, 'Total': float, 'Historic': float})

if __name__ == '__main__':
    df = clean_data(pd.read_excel('C:/Users/Vadim/Documents/Salary History.xlsx'))
    plot(df)
