import pandas as pd

"""
title: "CS5010 Project"
author: "Abhijeet Chawhan"
date: "5/9/2021"
output: Correlation calculations and Plots
"""


# This class reads zillow Home Index Dataset of Single Family Home
# having 1 / 2 / 3 / 4 / 5 bedrooms and
# creates dictionary (num_bed_hindex_dict) whose key is the bedroom number and value is the respective dataframe.
class ZillowHomeIndex:
    def __init__(self):
        self.num_bed_hindex_dict = {}

# The zillow home index dataset contains date as header name of the
# home index vaues of the respective area ( state / city / county / etc.)
# This method adds Date column and the respective home index
# as price_index column. In order to convert the columns to rows, Pandas.melt() method is used.
    def convert_column_to_rows(self,df):
        df_new = pd.melt(df, id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName',
           'State', 'City', 'Metro', 'CountyName'], var_name='Date', value_name='price_index')
        return df_new

# This method populates the num_bed_hindex_dict by reading the dataset
# based on the num_bed(Single Family Bedroom count) input.
# The dataset is read of it was not already read for this ZillowHomeIndex object.
    def get_hindex(self,num_bed, h_index_DS_group_id, h_index_DS_group_val, start_year, end_year=None):
        if self.num_bed_hindex_dict.__contains__(num_bed):
            return self.num_bed_hindex_dict

        if num_bed == '1':
            hindex_1b = self.get_hIndex_fr_year_melt_later("1", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
            self.num_bed_hindex_dict['1'] = hindex_1b
        elif num_bed == '2':
            hindex_2b = self.get_hIndex_fr_year_melt_later("2", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
            self.num_bed_hindex_dict['2'] =hindex_2b
        elif num_bed == '3':
            hindex_3b = self.get_hIndex_fr_year_melt_later("3", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
            self.num_bed_hindex_dict['3'] = hindex_3b
        elif num_bed == '4':
            hindex_4b = self.get_hIndex_fr_year_melt_later("4", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
            self.num_bed_hindex_dict['4'] = hindex_4b
        elif num_bed == '5':
            hindex_5b = self.get_hIndex_fr_year_melt_later("5", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
            self.num_bed_hindex_dict['5'] = hindex_5b
        elif num_bed.upper() == 'ALL':
            if not self.num_bed_hindex_dict.__contains__('1'):
                hindex_1b = self.get_hIndex_fr_year_melt_later("1", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
                self.num_bed_hindex_dict['1'] = hindex_1b
            if not self.num_bed_hindex_dict.__contains__('2'):
                hindex_2b = self.get_hIndex_fr_year_melt_later("2", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
                self.num_bed_hindex_dict['2'] = hindex_2b
            if not self.num_bed_hindex_dict.__contains__('3'):
                hindex_3b = self.get_hIndex_fr_year_melt_later("3", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
                self.num_bed_hindex_dict['3'] = hindex_3b
            if not self.num_bed_hindex_dict.__contains__('4'):
                hindex_4b = self.get_hIndex_fr_year_melt_later("4", h_index_DS_group_id, h_index_DS_group_val, str(start_year), end_year)
                self.num_bed_hindex_dict['4'] = hindex_4b
            if not self.num_bed_hindex_dict.__contains__('5'):
                hindex_5b = self.get_hIndex_fr_year_melt_later("5", h_index_DS_group_id,
                                                               h_index_DS_group_val, str(start_year), end_year)
                self.num_bed_hindex_dict['5'] = hindex_5b
        return self.num_bed_hindex_dict

# Reads dataset based on the num_bed(Single Family Bedroom count) input and generates the respective dataframe.
# This method also aggregates the generated dataframe with the provided column name (group_id) and the group value.
# The resulting dataframe is cleaned by removing empty data and also is filtered
# using the start_year and / or end_year values / value.
# The final dataframe is returned.

    def get_hIndex_fr_year_melt_later(self, num_bed, group_id, group_val, start_year, end_year=None):
        if int(start_year) > 2021 or int(start_year) < 2011:
            print("Date is out of range. Please provide Date between 2011 and 2021")
        if num_bed == '1':
            df = pd.read_csv(
                "/Users/abhijeet/Desktop/MSDS/CSSemProject/Zip_zhvi_bdrmcnt_1_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv")
        elif num_bed == '2':
            df = pd.read_csv(
                "/Users/abhijeet/Desktop/MSDS/CSSemProject/Zip_zhvi_bdrmcnt_2_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv")
        elif num_bed == '3':
            df = pd.read_csv(
                "/Users/abhijeet/Desktop/MSDS/CSSemProject/Zip_zhvi_bdrmcnt_3_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv")
        elif num_bed == '4':
            df = pd.read_csv(
                "/Users/abhijeet/Desktop/MSDS/CSSemProject/Zip_zhvi_bdrmcnt_4_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv")
        elif num_bed == '5':
            df = pd.read_csv(
                "/Users/abhijeet/Desktop/MSDS/CSSemProject/Zip_zhvi_bdrmcnt_5_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv")

        df_grp = df.groupby(group_id).get_group(group_val)
        df_new = self.convert_column_to_rows(df_grp)
        df_new['Year'] = pd.DatetimeIndex(df_new['Date']).year
        df_new['Month'] = pd.DatetimeIndex(df_new['Date']).month
        df_new['YearMonth'] = pd.to_datetime(df_new['Date']).dt.strftime('%Y-%m')
        if end_year is None:
            df_new = df_new[df_new['Year'] == int(start_year)]
        else:
            df_new = df_new[(df_new['Year'] >= int(start_year)) & (df_new['Year'] <= int(end_year))]
        df_new = df_new[df_new['Month'] != '.']
        df_new = df_new[df_new['price_index'] != 'NaN']
        df = df_new.dropna()
        return df