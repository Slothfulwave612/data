"""
__author__: anmol_durgapal

Python module for input-output operations.
"""

## import necessary packages
import numpy as np
import pandas as pd

def per_null(df):
    """
    Function to find the percentage of null values 
    for a column in a dataframe.

    Args:
        df (pandas.DataFrame): required dataframe.

    Returns:
        pandas.Series: containing column name and percentage of NaN values.
    """ 
    ## init an empty dict
    percent_series = dict()

    ## fetch all the columns
    cols = df.columns

    ## iterate the column list
    for col in cols:
        ## for null assign 0 else assign 1
        null_values = np.where(df[col].isnull(), 1, 0)

        ## calculate the mean
        percent = null_values.mean()

        ## add to the dict
        percent_series[col] = percent

    return pd.Series(percent_series)

def get_time(time, time_format):
    """
    Function to get either hour or minute from a time-string.

    Args:
        time (str): time-string
        time_format (str): hour/min

    Returns:
        int: hour/minute
    """    
    if time_format == "hour":
        return int(time[0:2])
    elif time_format == "min":
        return int(time[3:5])
    elif time_format == "year":
        return int(time.year)
    elif time_format == "month":
        return int(time.month)
    elif time_format == "day":
        return time.weekday() + 1

def make_df(df_1, df_2):
    """
    Function to concat sales and date dataframe.

    Args:
        df_1, df_2 (pd.DataFrame): required dataframe.
    
    Returns:
        pandas.DataFrame: concatnated dataframe
    """    
    ## concat both the dataframes
    main_df = pd.concat([df_1, df_2], axis=1)

    ## add new columns

    ## add year to dataframe
    main_df["year"] = main_df["date"].apply(lambda x: get_time(x, "year"))

    ## add month to dataframe
    main_df["month"] = main_df["date"].apply(lambda x: get_time(x, "month"))

    ## add day_name
    main_df["day_name"] = main_df["date"].apply(lambda x: get_time(x, "day"))

    ## add hour to dataframe
    main_df["hour"] = main_df["time_of_day(hh:mm:ss)"].apply(lambda x: get_time(x, "hour"))

    ## add minute to dataframe
    main_df["minute"] = main_df["time_of_day(hh:mm:ss)"].apply(lambda x: get_time(x, "min"))

    ## add sales
    main_df["sales"] = main_df["quantity sold"] * main_df["unit price"]

    ## drop all unnecessary columns -- do not remove the space that's what the column name is
    main_df.drop(
        [
            "transaction timestamp", "timestamp              ", "date", "time_of_day(hh:mm:ss)", "month_of_year"
        ],
        axis=1, inplace=True
    )

    ## rearranging all the columns
    main_df = main_df[
        [
            "transaction id", "customer id", "product id", "product description", 
            "quantity sold", "unit price", "sales", "transaction country",
            "year", "month", "day_of_month", "day_name", "hour", "minute"
        ]
    ]

    return main_df

def customer_country(df):
    """
    Function to make dataframe for which customers spends the most.

    Args:
        df (pandas.DataFrame): required dataframe.
    
    Returns:
        pandas.DataFrame
    """    
    ## make groupy dataframe
    temp_df = df.dropna(axis=0).groupby(
        by="customer id"
    ).sum().sort_values("sales", ascending=False)["sales"].head(15).reset_index()

    ## change datatype
    temp_df["customer id"] = temp_df["customer id"].astype(int).astype(str)

    ## traverse the dataframe
    for row, data in temp_df.iterrows():
        ## fetch country name
        country = df.loc[
            df["customer id"] == float(data["customer id"]), "transaction country"
        ].unique()[0]

        ## add country name in customer id
        temp_df.loc[row, "customer id"] = temp_df.loc[row, "customer id"] + ', ' + country
    
    return temp_df
