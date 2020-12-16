"""
__author__: Anmol_Durgapal

Python module for visualizations.
"""

## import necessary packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import ticker as mtick
import seaborn as sns

## define global
day_name = {
    1: "Monday", 2: "Tuesday",  3: "Wednesday",  4: "Thrusday", 5: "Friday", 6: "Saturday", 7: "Sunday"
}

month_name = { 
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

def plot_distribution(df, nrows, ncols, figsize=(12,8), filename=None):
    """
    Function to plot histogram for each columns in dataframe.

    Args:
        df (pandas.DataFrame): required dataframe.
        nrows, ncols (int): number of rows and columns.
        figsize (tuple): figure size.
        filename (str, optional): path where plot will be saved. Defaults to None.

    Return:
        pyplot.Figure: figure object.
        axes.Axes: axes object
    """    
    ## fetch columns
    cols = df.columns

    ## set default fontfamily and fontcolor
    rcParams["font.family"] = "Liberation Serif"
    rcParams["text.color"] = "#121212"
    rcParams["xtick.labelsize"] = 16
    rcParams["ytick.labelsize"] = 16

    ## make subplots
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, facecolor="#F0F0F0")

    ## init two variables
    i, j = 0, 0

     ## traverse the axes
    for n in range(0, nrows*ncols):
        if n <= len(cols) - 1:
            ## set facecolor
            ax[i,j].set_facecolor("#F0F0F0")
            
            ## plot histogram
            ax[i,j].hist(df[cols[n]], color="#845EC2")

            ## set xlabel
            ax[i,j].set_xlabel(cols[n])
            
            j += 1

            if j == ncols:
                i += 1
                j = 0
        else:
            ## do not plot
            ax[i,j].axis("off")
    
    ## clean layout
    plt.tight_layout(pad=3.0)

    if filename:
        fig.savefig(filename, dpi=500, bbox_inches="tight")
    
    return fig, ax

def sales_over_month(df, figsize=(12,8), bar=False, filename=None):
    """
    Function to plot line plot showing sales over the month.

    Args:
        df (pandas.DataFrame): required dataframe.
        figsize (tuple, default): size of the figure. Defaults to (12,8).
        bar (bool, default): to plot bar or not. Defaults to False.
        filename (str, default): path where plot will be saved. Defaults to None.

    Returns:
        pyplot.Figure: figure object.
        axes.Axes: axes object.
    """    
    ## create dataframe containing year, month and corresponding sales
    sales_df = df.groupby(
        by=["year", "month"]
    ).sum()["sales"].reset_index()

    ## create two empty dictionary to contain month name and corresponding sales
    month, sales = [], []

    ## traverse the sales-dataframe
    for _, data in sales_df.iterrows():
        ## add month name
        month.append(
            f'{month_name[data["month"]]}, {int(data["year"])}'
        )

        ## add sales
        sales.append(
            round(data["sales"], 2)
        )
    
    ## set default fontfamily and fontcolor
    rcParams["font.family"] = "Liberation Serif"
    rcParams["text.color"] = "#121212"

    ## create subplot
    fig, ax = plt.subplots(figsize=figsize, facecolor="#F0F0F0")
    ax.set_facecolor("#F0F0F0")

    if bar:
        ## plot sales over month
        ax.bar(month, sales, zorder=3)
    else:
        ## plot sales over month
        ax.plot(month, sales)

    ## make grid in the plot
    ax.grid()

    ## set title and labels
    ax.set_title("Sales Over Month (Dec 2010 - Dec 2011)", fontsize=20)
    ax.set_xlabel("Months", fontsize=18)
    ax.set_ylabel("Sales (in million)", fontsize=18)

    ## increase size of tick-params
    ax.tick_params(axis='both', which='major', labelsize=15)

    ## rotate the x-ticks
    plt.xticks(range(0,13), month, rotation=90)

    ## save the plot
    if filename:
        fig.savefig(filename, dpi=500, bbox_inches="tight")

    return fig, ax

def plot_two_axis(df, group, ax1_col, ax2_col, labels, figsize=(12,8), y_ticks=(9, 9, 10000, 10000), filename=None):
    """
    Function to plot a bar and a line plot in the same subplot.

    Args:
        df (pandas.DataFrame): required dataframe.
        group (str): column name on which groupby is applied.
        ax1_col (str): column name to be plotted as a bar.
        ax2_col (str): column name to be plotted as line.
        labels (list): list of lables for x and y axis and title. 
        figsize (tuple, optional): size of the figure. Defaults to (12,8).
        y_ticks (tuple, optional): number of yticks and maximum values for yticks labels. Defaults to (9, 9, 10000, 10000).
        filename (str, optional): path where plot will be saved. Defaults to None.

    Returns:
        pyplot.Figure: figure object.
        axes.Axes: axes object.
    """    
    ## make dataframe using groupby
    temp_df = df.groupby(
        by=group
    ).sum().sort_values(ax1_col, ascending=False).head(15)[[ax1_col, ax2_col]].reset_index()

    ## make subplot
    fig, ax = plt.subplots(figsize=figsize, facecolor="#F0F0F0")
    ax.set_facecolor("#F0F0F0")

    ## set default fontfamily and fontcolor
    rcParams["font.family"] = "Liberation Serif"
    rcParams["text.color"] = "#121212"
    rcParams["xtick.labelsize"] = 16
    rcParams["ytick.labelsize"] = 16

    ## set a second axis
    ax_2 = ax.twinx()

    ## plot bar
    ax.bar(
        temp_df[group], temp_df[ax1_col], zorder=2, label="Sales"
    )

    ## plot line
    ax_2.plot(
        temp_df[group], temp_df[ax2_col], zorder=2, color="#121212", label="Quantity Sold"
    )

    ## set labels
    ax.set_xlabel(labels[0], fontsize=18)
    ax.set_ylabel(labels[1], fontsize=18)
    ax_2.set_ylabel(labels[2], fontsize=18)

    ## set title 
    ax.set_title(labels[3], fontsize=20)

    ## rotate the x-ticks
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)

    ## make grid in the plot
    ax.grid()

    ## set y-tick labels
    ax.yaxis.set_major_locator(mtick.LinearLocator(y_ticks[0]))
    ax_2.yaxis.set_major_locator(mtick.LinearLocator(y_ticks[1]))
    ax.set_ylim(0, temp_df[ax1_col].max() + y_ticks[2])
    ax_2.set_ylim(0, temp_df[ax2_col].max() + y_ticks[3])

    ## add legend
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax_2.get_legend_handles_labels()
    ax_2.legend(lines + lines2, labels + labels2, loc=0, fontsize=14)

    ## save the plot
    if filename:
        fig.savefig(filename, dpi=500, bbox_inches="tight")

    return fig, ax

def make_bar(df, group, value, labels, func="sum", figsize=(12,8), filename=None, iscus=False, isline=False):
    """
    Function to make bar charts.

    Args:
        df (pandas.DataFrame): required dataframe.
        group (str): column name on which groupby clause will be applied.
        value (str): column name whose value will be plotted.
        labels (list): list of lables for x and y axis and title. 
        func (str, optional): which aggregation function to perform. Defaults to "sum".
        figsize (tuple, optional): size of the figure. Defaults to (12,8).
        filename (str, optional): path where plot will be saved. Defaults to None.
        iscus (bool, optional): plot for customer id. Defaults to False.
        isline (bool, optional): for plotting line plot. Defaults to False.

    Returns:
        pyplot.Figure: figure object.
        axes.Axes: axes object.
    """    
    if iscus:
        temp_df = df.copy()
    else:
        ## make required dataframe using groupby clause
        temp_df = df.groupby(by=group)

        if func == "sum":
            if isline:
                temp_df = temp_df.sum()[value].reset_index().sort_values(group)
            else:
                temp_df = temp_df.sum().sort_values(value, ascending=False)[value].head(15).reset_index()
        elif func == "count":
            temp_df = temp_df.count().sort_values(value, ascending=False)[value].head(15).reset_index()

    ## make subplot
    fig, ax = plt.subplots(figsize=figsize, facecolor="#F0F0F0")
    ax.set_facecolor("#F0F0F0")

    ## set default fontfamily and fontcolor
    rcParams["font.family"] = "Liberation Serif"
    rcParams["text.color"] = "#121212"
    rcParams["xtick.labelsize"] = 16
    rcParams["ytick.labelsize"] = 16

    ## plot line plot
    ax.plot(temp_df[group].map(day_name), temp_df[value], zorder=2)

    ## add grid
    ax.grid()

    ## set labels and title
    ax.set_xlabel("Days", fontsize=18)
    ax.set_ylabel("Sales (in million)", fontsize=18)
    ax.set_title("Sales in each day", fontsize=20)

    if filename:
        fig.savefig(filename, dpi=500, bbox_inches="tight")

    return fig, ax
