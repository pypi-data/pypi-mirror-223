# Databricks notebook source
import pyspark
import csv
import datetime
import os
from datetime import datetime ,timedelta
import pandas as pd
from databricks.sdk.runtime import *

def files_to_list(directory):
    dataframes=[]
    file_pat=[]
    current_date=datetime.now().date()
    for i in range(7):
        try:
            #current_date=datetime.datetime.now().strptime(current_date,"%Y-%m-%d")
            date= current_date-timedelta(days=i)
            directory_path=os.path.join(directory,date.strftime("%m"))
            internal_dir=os.path.join(directory_path,date.strftime("%d"))
            if dbutils.fs.ls(internal_dir):
                print(f"Loading files from {file_pat}:")
        
            # Iterate over file paths in the directory
                for file_info in dbutils.fs.ls(internal_dir):
                    file_path = file_info.path            
            # Load CSV file into a DataFrame
                    if file_path.endswith('.parquet'):
                        file_pat.append(file_path)
        except:
            print(f"No directory found for {date.strftime('%Y-%m-%d')}")
    print(file_pat)
    for file_name in file_pat:
        if file_name.endswith('.csv'):
            dataframe = spark.read.option("header",True).csv(file_name)
        elif file_name.endswith('.parquet'):
            dataframe = spark.read.option("header",True).parquet(file_name)
        elif file_name.endswith('.xlsx'):
            dataframe = spark.read.format("com.crealytics.spark.excel").option("header","true").load(file_name) 
        else:
            raise ValueError('Unsupported file format')
        dataframes.append(dataframe)
    pandas_df_list=[]
    for spark_df in dataframes:
        pandas_df=spark_df.toPandas()
        pandas_df_list.append(pandas_df)
        combined_df=pd.concat(pandas_df_list, ignore_index=True)
    return combined_df