import pandas as pd
import numpy as np
from datetime import datetime, date
from pathlib import Path
import os
import csv

success_rate = {}


def generate_report():
    csv_columns = ['trade_interval_days', 'number_of_successful_trades']
    with open('statistics_report.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for key in success_rate:
            writer.writerow({'trade_interval_days': key, 'number_of_successful_trades': success_rate[key]})


def read_input(input_file):
    print('Start_time:', datetime.now())
    data = pd.read_csv(input_file)
    print('Data read completed at:', datetime.now())
    data.to_csv('bitcoin_trade.csv')
    print('Data write completed at:', datetime.now())
    print('Total null open prices: %s' % data['Open'].isnull().sum())


def create_output_directory(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print("Directory Created::{}".format(output_path))
        print("-" * 150)
    else:
        pass


def transform_and_save_data(output_path):
    num_days = [5, 10, 15, 30, 45, 60, 90, 100, 120, 150, 180, 365, 730, 900, 1095, 1300, 1460, 1825, 2190, 2555, 2920]
    df = pd.read_csv("bitcoin_trade.csv")
    for i in num_days:
        data = df.copy()
        print('Start_time: ' + str(i) + ' days', datetime.now())
        data = data.drop(['Volume_(BTC)', 'Volume_(Currency)', 'Weighted_Price'], axis=1)
        data = data.dropna(axis=0, how='any').reset_index()
        data['buy_date'] = pd.to_datetime(data['Timestamp'], unit='s').dt.date
        data['min_Timestamp'] = data.groupby(['buy_date'], sort=False)['Timestamp'].transform('min')
        data['max_Timestamp'] = data.groupby(['buy_date'], sort=False)['Timestamp'].transform('max')
        data['Open_Price'] = np.where(data['Timestamp'] == data['min_Timestamp'], data['Open'], 0)
        data['Closed_Price'] = np.where(data['Timestamp'] == data['max_Timestamp'], data['Close'], 0)
        data = data[(data['Open_Price'] != 0) | (data['Closed_Price'] != 0)]
        data = data.groupby(['buy_date']).agg(epoch_time=('Timestamp', 'max'), buy_price=('Open_Price', 'max'),
                                              High_final=('High', 'max'), Low_final=('Low', 'min'),
                                              Close_final=('Closed_Price', 'max')).reset_index()
        data['selling_price'] = data['Close_final'].shift(-i).rolling(1).apply(lambda x: x[0], raw=True)
        data['selling_date'] = data['epoch_time'].shift(-i).rolling(1).apply(lambda x: x[0], raw=True)
        data['success'] = np.zeros(len(data))
        data.loc[data['selling_price'] > data['buy_price'], 'success'] = 1
        data = data[data['success'] == 1].reset_index()
        data['selling_date'] = pd.to_datetime(data['selling_date'], unit='s').dt.date
        data['roi_percentage'] = ((data['selling_price'] - data['buy_price']) / data['buy_price']) * 100
        data = data.drop(['index', 'epoch_time', 'High_final', 'Low_final', 'Close_final'], axis=1)
        print('Number of successful trades:', len(data))
        success_rate[i] = len(data)
        data.to_csv(output_path + '/success_trades_' + str(i) + '_days.csv')
        print('End_time: ' + str(i) + ' days', datetime.now())
        print("-" * 150)


def main():
    input_file = 'https://storage.googleapis.com/zalora-interview-data/bitstampUSD_1-min_data_2012-01-01_to_2020-09-14.csv'
    read_input(input_file)
    output_path = str(Path.joinpath(Path.home(), 'bitcoin_output', str(date)))
    create_output_directory(output_path)
    transform_and_save_data(output_path)
    generate_report()


main()
