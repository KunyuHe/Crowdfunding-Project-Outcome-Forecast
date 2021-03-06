"""
Summary:     A collections of functions for visualization.

Description: contains a function that reads data and data types, and many
             other functions for visualization
Author:      Kunyu He, CAPP'20
"""

import random
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.font_manager import FontProperties


INPUT_DIR = "../data/"

COLORS = list(sns.color_palette("Set2")) + list(sns.color_palette("Set3"))
TITLE = FontProperties(family='serif', size=14, weight="semibold")
AXIS = FontProperties(family='serif', size=12)
TICKS = FontProperties(family='serif', size=10)


#----------------------------------------------------------------------------#
def read_data(file_name, drop_na=False):
    """
    Read credit data in the .csv file and data types from the .json file.

    Inputs:
        - data_file (string): name of the data file.
        - drop_na (bool): whether to drop rows with any missing values

    Returns:
        (DataFrame) clean data set with correct data types

    """
    data = pd.read_csv(INPUT_DIR + file_name)

    if drop_na:
        data.dropna(axis=0, inplace=True)

    data['date_posted'] = pd.to_datetime(data['date_posted'])
    data['datefullyfunded'] = pd.to_datetime(data['datefullyfunded'])

    return data


def bar_plot(ax, data, column, labels, sub=True, x_tick=[None, None]):
    """
    Create a bar plot from a categorical vairable in the data set.

    Inputs:
        - ax (axes): axes instance to draw the plot on
        - data (DataFrame): to extract the categotical column from
        - column (string): name of the categorical column
        - sub (bool): whether the plot is a subplot
        - labels (list of strings): [title, xlabel, ylabel]
        - x_tick (list): [[x-axis tick labels], horizontal or vertical]

    Returns:
        None
    """
    sns.countplot(x=column, data=data, palette="Set3", ax=ax, edgecolor='black')

    plot_title, xlabel, ylabel = labels
    x_ticks, xtick_rotation = x_tick
    ax.set_title(plot_title, fontproperties=[TITLE, AXIS][int(sub)])
    ax.set_xlabel(xlabel, fontproperties=AXIS)
    ax.set_ylabel(ylabel, fontproperties=AXIS)
    if x_ticks:
        ax.set_xticklabels(x_ticks, fontproperties=TICKS, rotation=xtick_rotation)

    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        ax.annotate(y_value, (x_value, y_value), xytext=(0, 5),
                    textcoords="offset points", ha='center', va='bottom',
                    fontproperties=TICKS)


def hist_plot(ax, ds, col, cut=False):
    """
    Create a histogram for a specific continuous variable.

    Inputs:
        - ax (axes): axes instance to draw the plot on
        - ds (Series): the series of the continuous variable
        - col (string): color to use for the histogram
        - cut (bool): whether to cut off the largest 5% of observations

    Returns:
        None
    """
    xlim = (ds.min(), [ds.max(), ds.quantile(0.95)][int(cut)])
    ax.hist(ds, range=xlim, edgecolor='black', color=col)

    ax.set_xlabel(ds.name.title(), fontproperties=AXIS)
    ax.set_ylabel("Frequency", fontproperties=AXIS)


def hist_panel(data, panel_title="", cut=False):
    """
    Plot a panel of histograms showing the distribution of variables, with two
    histograms in a row, a fixed width of 20, and a fixed height per histogram
    of 4. The colors are randomly chosen from the seaborn color palette "Set3".

    Inputs:
        - data (DataFrame): a matrix of numerical variables

    Returns:
        None
    """
    count = data.shape[1]
    rows = count // 2

    fig, _ = plt.subplots(figsize=[20, rows * 4])

    for i in range(count):
        ax_sub = fig.add_subplot(rows, 2, i + 1)
        hist_plot(ax_sub, data.iloc[:, i], random.choice(COLORS), cut)

    fig.suptitle(panel_title, fontproperties=TITLE)


def corr_triangle(ax, data, sub=False, plot_title=""):
    """
    Plot a correlation triangel.

    Inputs:
        - ax (axes): axes instance to draw the plot on
        - data (DataFrame): a matrix of numerical variables
        - sub (bool): whether the plot is a subplot
        - plot_title (string): title of the triangle

    Returns:
        None
    """
    corr = data.corr()

    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0, square=True,
                linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
    ax.set_title(plot_title, fontproperties=[TITLE, AXIS][int(sub)])


def box_plot(data):
    """
    Draw a box plot for every column of the data.

    Inputs:
        - data (DataFrame): a matrix of numerical variables

    Returns:
        None
    """
    n_cols = data.shape[1]
    fig_cols = 2
    fig_rows = n_cols // fig_cols
    _, axes = plt.subplots(nrows=fig_rows, ncols=fig_cols,
                           figsize=[20, fig_rows * 4])

    for i, col_name in enumerate(data.columns):
        subdata = data[col_name]
        sns.boxplot(subdata, ax=axes[i // fig_cols, i % fig_cols],
                    color=random.choice(COLORS))
    sns.despine()
