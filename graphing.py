import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import data_exploration
from statsmodels.graphics.tsaplots import plot_pacf
import plotly.express as px


def graph_anomaly_histogram(df):
    """
    Takes dataframe and plots anomaly distribution histogram
    :param df:Indexed pandas dataframe with 2 columns: meter-reading and anomaly
    :return:
    """
    hist_data_anomaly = df["anomaly"].tolist()
    number_of_non_anomalies, number_of_anomalies = hist_data_anomaly.count(0), hist_data_anomaly.count(
        1)  # finds ratio of anomalies
    anomalies_to_non_ratio = number_of_anomalies / number_of_non_anomalies

    plt.hist(hist_data_anomaly, bins=2)
    plt.show()

    return anomalies_to_non_ratio


def graph_histogram(df):
    """
    Takes dataframe and plots histogram
    :param df: Pandas Dataframe with 1 column: meter_reading
    :return:None
    """
    hist_data = data_exploration.create_missing_value_histogram_data(df, "building_id", "meter_reading")
    plt.hist(hist_data, bins=50)
    plt.show()


def graph_pacf(df, lag):
    """
    Takes series and lag column and plots Partial Auto-correlation graph
    :param df:Pandas dataframe with only 1 column: meter_reading
    :param lag:Int, number of lags
    :return:None
    """
    plot_pacf(df["meter_reading"], lags=lag)
    plt.show()


def graph_heatmap(df):
    """
    Takes data-frame and plots heatmap based on days of week/time of day
    :param df: Pandas data-frame with two columns: timestamp (index column) and meter-reading
    :return:None
    """
    # time_column = data_exploration.create_time_series(df[0:len(df):500])
    time_column = data_exploration.create_time_series(df)
    time_lists = [
        [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []],
        [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]]
    for time in range(len(time_column)):
        time_lists[time_column[time].weekday()][time_column[time].hour].append(df["meter_reading"].iloc[time])
    heatmap_data = [[], [], [], [], [], [], []]
    for i in range(len(time_lists)):  # i = day of week
        for j in range(len(time_lists[i])):  # j = time of day
            try:
                my_list = [x for x in time_lists[i][j] if not np.isnan(x)]
                avg = sum(my_list) / len(my_list)
                heatmap_data[i].append(avg)
            except ZeroDivisionError:
                heatmap_data[i].append("No Data")
    heatmap_data = np.array(heatmap_data)
    heatmap_dataframe = pd.DataFrame(heatmap_data)
    fig = px.imshow(heatmap_dataframe, text_auto=True)
    fig.show()

def plot_scatter(df, x, y):
    """
    Generate Pyplot scatter plot from Pandas dataframe
    :param df: Pandas dataframe
    :param x: x axis column
    :param y: y axis column
    :return: None
    """
    x_data = getattr(df, x)
    y_data = getattr(df, y)
    plt.scatter(x_data, y_data, color='blue')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()