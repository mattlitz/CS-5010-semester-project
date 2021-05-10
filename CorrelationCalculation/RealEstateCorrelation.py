import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sp500cspdsdata
import zillow_home_index

"""
title: "CS5010 Project"
author: "Abhijeet Chawhan"
date: "5/9/2021"
output: Correlation calculations and Plots
"""

# This class calculates correlation between Zillow home Index with S&P,
# Zillow Home Index with Unemployment Rate and Zillow Home Index with Crime Rate
# of a State / City / County / Area (Zip Code)
# This class also plots the above correlations over a range of years or a specific year for the correlation with S&P,
# plots line graph of Home Index values of State / City / County / Area(Zip Code) for a year and a range of years,
# plots line graph of S&P for a year and a range of years, plots line graph of unemployment
# and crime rates for a range of years,


class RealEstateCorrelation:
    def __init__(self):
        self.num_bed_lst = ['1', '2', '3', '4', '5']
        self.corr_lst_fr_1_bed = []
        self.corr_lst_fr_2_bed = []
        self.corr_lst_fr_3_bed = []
        self.corr_lst_fr_4_bed = []
        self.corr_lst_fr_5_bed = []
        self.sp_cspds_data = sp500cspdsdata.Sp500CspdsData()
        self.zhomeIndex = zillow_home_index.ZillowHomeIndex()

# This method returns home index dictionary generated based
# on the input parameters - num_bed(bedroom count of the single family home),
# h_index_DS_group_id (eg. State / City / County / Region (Zip Code)),
# h_index_DS_group_val ( group value - VA / Ashburn / Fairfax / 20148) and
# start_year (2012 to 2020)
    def get_raw_hindex(self,num_bed, h_index_DS_group_id, h_index_DS_group_val, start_year):
        yr = int(start_year)
        if yr > 2011:
            hindex_df_dict = self.zhomeIndex.get_hindex(num_bed, h_index_DS_group_id, h_index_DS_group_val,'2011', start_year)
        return hindex_df_dict

# This method returns correlation value between Home Index of the provided
# single family bedroom count and S&P, home index dataframe mean on 'Month'
# aggregate and S&P dataframe
    def get_hindex_sp500_corr_for_num_bed(self, num_bed, h_index_DS_group_id, h_index_DS_group_val, start_year):
        sp_data = self.sp_cspds_data.get_sp_data(start_year, None)
        hindex_df_dict = self.zhomeIndex.get_hindex(num_bed, h_index_DS_group_id, h_index_DS_group_val, start_year)
        hindex_df = hindex_df_dict.get(num_bed)
        df_mean = hindex_df.groupby('Month').mean()
        corr_val = round(df_mean['price_index'].corr(sp_data['SP500']), 3)
        print('Correlation between ' + num_bed + ' bed single family house with SP500 for the year ' + str(
            start_year) + ' is ' + str(corr_val))
        return corr_val, df_mean, sp_data

# This method returns the list of Correlation values between home index of the
# single family bedroom count with S&P, home index dataframe
# dictionary( key = bedroom count, value = resepective dataframe) and S&P dataframe
# This method utilizes get_hindex_sp500_corr_for_num_bed(....)
# in populating the correlation list, home index dataframe dictionary and S&P dataframe.
# This also populates correlation list of the respective bedroom count.
# These lists are used in plotting the correlation graphs

    def get_hindex_sp500_corr(self, num_bed, h_index_DS_group_id, h_index_DS_group_val, start_year):
        corr_lst = []
        hIndex_df_dict = {}
        if num_bed.upper() == 'ALL':
            for item in self.num_bed_lst:
                corr_val, hIndex_df_mean, sp_data = self.get_hindex_sp500_corr_for_num_bed(item, h_index_DS_group_id,
                                                                                      h_index_DS_group_val, start_year)
                if str(item) == '1':
                    self.corr_lst_fr_1_bed.append(corr_val)
                elif str(item) == '2':
                    self.corr_lst_fr_2_bed.append(corr_val)
                elif str(item) == '3':
                    self.corr_lst_fr_3_bed.append(corr_val)
                elif str(item) == '4':
                    self.corr_lst_fr_4_bed.append(corr_val)
                elif str(item) == '5':
                    self.corr_lst_fr_5_bed.append(corr_val)
                hIndex_df_dict[item] = hIndex_df_mean
        else:
            corr_val, hIndex_df_mean, sp_data = self.get_hindex_sp500_corr_for_num_bed(num_bed, h_index_DS_group_id,
                                                                                  h_index_DS_group_val, start_year)
            corr_lst.append(corr_val)
            hIndex_df_dict[num_bed] = hIndex_df_mean
        return corr_lst, hIndex_df_dict, sp_data

# This method returns correlation list over a range of years (2011 to start_year),
# bedroom count - correlation list dictionary, home index dataframe of start_year
# and S&P dataframe of start_year

    def get_hindex_sp_corr_fr_yrs(self,num_bed, h_index_DS_group_id, h_index_DS_group_val, start_year):
        self.corr_lst_fr_1_bed.clear()
        self.corr_lst_fr_2_bed.clear()
        self.corr_lst_fr_3_bed.clear()
        self.corr_lst_fr_4_bed.clear()
        self.corr_lst_fr_5_bed.clear()
        corr_lst = []
        yr = int(start_year)
        hIndex_df = None
        sp_df = None
        num_bed_corr_lst_dict = {}
        while yr >= 2011:
            corrs, hIndex_df_mean, sp_data = self.get_hindex_sp500_corr(num_bed, h_index_DS_group_id, h_index_DS_group_val,
                                                                   yr)
            if yr == int(start_year):
                hIndex_df = hIndex_df_mean
                sp_df = sp_data
            if num_bed.upper() != 'ALL':
                corr_lst.extend(corrs)
            yr -= 1
        num_bed_corr_lst_dict.clear()
        if num_bed.upper() == 'ALL':
            num_bed_corr_lst_dict['1'] = self.corr_lst_fr_1_bed
            num_bed_corr_lst_dict['2'] = self.corr_lst_fr_2_bed
            num_bed_corr_lst_dict['3'] = self.corr_lst_fr_3_bed
            num_bed_corr_lst_dict['4'] = self.corr_lst_fr_4_bed
            num_bed_corr_lst_dict['5'] = self.corr_lst_fr_5_bed
        return corr_lst, num_bed_corr_lst_dict, hIndex_df, sp_df

# This method prints correlation value between home index of the
# single family with bedroom count (num_bed) with Unemployment rate and crime rate.
# It also returns cspds dataframe which contains unemployment rate,
# crime rate of State, City, County
    def get_hindex_cspds_corr_fr_num_bed(self, num_bed, h_index_DS_group_id, h_index_DS_group_val, data_grp_id, data_grp_val,
                                         start_year, end_year):
        cspds_data = self.sp_cspds_data.get_unemp_crime_data(data_grp_id, data_grp_val, start_year, end_year)
        hindex_df_dict = self.zhomeIndex.get_hindex(num_bed, h_index_DS_group_id, h_index_DS_group_val, start_year, end_year)
        hindex_df = hindex_df_dict.get(num_bed)
        hindex_df = hindex_df[(hindex_df['Year'] >= int(start_year)) & (hindex_df['Year'] <= int(end_year))]
        df_mean = hindex_df.groupby('Year').mean()

        unemp_corr_val = round(df_mean['price_index'].corr(cspds_data['Unemployment Rate']),3)
        crime_corr_val = round(df_mean['price_index'].corr(cspds_data['Crime Rate']), 3)

        print(
            'Correlation between ' + num_bed + ' bed single family house ' + 'of ' + h_index_DS_group_val + ' with Unemployment Rate from the year ' + str(
                start_year) + ' to ' + str(end_year) + ' is ' + str(unemp_corr_val))
        print(
            'Correlation between ' + num_bed + ' bed single family house ' + 'of ' + h_index_DS_group_val + ' with Crime Rate from the year ' + str(
                start_year) + ' to ' + str(end_year) + ' is ' + str(crime_corr_val))
        return cspds_data

# This method returns cspds dataframe which contains unemployment rate,
# crime rate of State, Coty, County and prints correlation values of
# home index with unemployment rate and crime rate.
# It utilizes get_hindex_cspds_corr_fr_num_bed(...)
# for calculating the correlation and retrieving the dataframe
    def get_hindex_cspds_corr(self, num_bed, h_index_DS_group_id, h_index_DS_group_val, data_grp_id, data_grp_val, start_year,
                              end_year):
        if num_bed.upper() == 'ALL':
            for item in self.num_bed_lst:
                cspds_df = self.get_hindex_cspds_corr_fr_num_bed(item, h_index_DS_group_id, h_index_DS_group_val,
                                                            data_grp_id,
                                                            data_grp_val, start_year, end_year)
        else:
            cspds_df = self.get_hindex_cspds_corr_fr_num_bed(num_bed, h_index_DS_group_id, h_index_DS_group_val, data_grp_id,
                                                        data_grp_val, start_year, end_year)
        return cspds_df

# This method plots line graphs of home Index, S&P,
# Unemployment Rate, Crime Rate, Correlations between
# Home index with S&P over a range of years.
    def plot_trend_on_yr_multi_plot(self, group_name, hIndex_df_dict_on_year, sp_data_on_year, corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df, cspds_df,
                                    start_year, cspds_start_yr, cspds_end_yr):
        plt.figure(figsize=(20, 6))
        plt.subplot(121)
        for key in hIndex_df_dict:
            df = hIndex_df_dict.__getitem__(key)
            sns.lineplot(x='Month', y='price_index', data=df,
                         label=key + ' bedroom')
        plt.ylabel('Home Index of ' + str(group_name))
        plt.xlabel('Year - ' + start_year)
        pos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        lab = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        plt.xticks(pos, lab)
        # plt.legend()
        plt.grid()
        plt.subplot(122)
        sns.lineplot(x='DATE_MONTH', y='SP500', data=sp_df, label='SP500')
        plt.xlabel('Year - ' + start_year)
        pos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        lab = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        plt.ylabel('S & P')
        plt.suptitle('Monthly Home Index Value and S&P Value')
        plt.xticks(pos, lab)
        plt.legend()
        plt.grid()
        ax1 = plt.subplots(1, 1, figsize=(20, 6))
        plt.subplot(121)
        for key in hIndex_df_dict_on_year:
            hindex_df = hIndex_df_dict_on_year.get(key)
            df_mean = hindex_df.groupby('Year').mean()
            sns.lineplot(x='Year', y='price_index', data=df_mean,
                         label=key + ' bedroom')
        plt.ylabel('Mean Home Index of ' + str(group_name))
        plt.xlabel('Year')
        hIndex_start_year = 2011
        hIndex_start_years = []
        while hIndex_start_year <= int(start_year):
            hIndex_start_years.append(hIndex_start_year)
            hIndex_start_year += 1
        pos = hIndex_start_years
        lab = hIndex_start_years
        plt.xticks(pos, lab)
        plt.legend()
        plt.grid()
        plt.subplot(122)
        sns.lineplot(x='DATE_YEAR', y='SP500', data=sp_data_on_year, label='SP500')
        plt.xlabel('Year')
        pos = hIndex_start_years
        lab = hIndex_start_years
        plt.ylabel('S & P')
        plt.suptitle('Yearly Mean Home Index Value and S&P Value')
        plt.xticks(pos, lab)
        # plt.legend()
        plt.grid()
        ax2 = plt.subplots(1, 1, figsize=(20, 6))
        plt.subplot(121)
        sns.lineplot(x='Year', y='Unemployment Rate', data=cspds_df, label='Unemployment Rate of ' + group_name)
        cspds_yr = int(cspds_start_yr)
        cspds_yrs = []
        while cspds_yr <= int(cspds_end_yr):
            cspds_yrs.append(cspds_yr)
            cspds_yr += 1
        # yrs = cspds_df['Year']
        pos = cspds_yrs
        lab = cspds_yrs
        plt.xticks(pos, lab)
        plt.legend()
        plt.grid()
        plt.ylabel('Unemployment Rate')
        plt.xlabel('Year')

        plt.subplot(122)
        sns.lineplot(x='Year', y='Crime Rate', data=cspds_df, label='Crime Rate of ' + group_name)
        plt.xticks(pos, lab)
        plt.legend()
        plt.grid()
        plt.ylabel('Crime Rate')
        plt.xlabel('Year')
        plt.suptitle('Yearly Unemployment and Crime Rates')
        ax3 = plt.subplots(1, 1, figsize=(10, 6))
        yr = int(start_year)
        if len(num_bed_corr_lst_dict) == 0:
            tmp = yr - len(corr_lst) + 1
            pos_lst = []
            while tmp <= yr:
                pos_lst.append(tmp)
                tmp += 1
            pos = pos_lst
            lab = pos_lst
            plt.xlabel('Year - ' + str(tmp) + " to " + start_year)
            corr_lst = corr_lst[::-1]
            corr_df = pd.DataFrame(list(zip(corr_lst, pos_lst)), columns=['Corr', 'Year'])
            sns.lineplot(x='Year', y='Corr', data=corr_df,
                         label='Correlation between ' + key + ' Bedroom Single Family Home Index of ' + group_name + ' and S&P')
        else:
            for key in num_bed_corr_lst_dict:
                corr_lst_1 = num_bed_corr_lst_dict.get(key)
                tmp = yr - len(corr_lst_1) + 1
                init = tmp
                pos_lst_1 = []
                while tmp <= yr:
                    pos_lst_1.append(tmp)
                    tmp += 1
                pos = pos_lst_1
                lab = pos_lst_1
                # print(corr_lst_1)
                corr_lst_1 = corr_lst_1[::-1]
                # print(pos_lst_1)
                plt.xlabel('Year - ' + str(init) + " to " + start_year)
                corr_df_1 = pd.DataFrame(list(zip(corr_lst_1, pos_lst_1)), columns=['Corr', 'Year'])
                sns.lineplot(x='Year', y='Corr', data=corr_df_1)
                             # label=' Home Index of ' + group_name + ' with ' + key + ' Bedroom Single Family Home - S&P Correlation')

        plt.ylabel('Correlation')
        plt.suptitle('Correlation between Home Index of '+group_name+' and S&P')
        plt.xticks(pos, lab)
        plt.legend()
        plt.grid()
        ax4 = plt.subplots(1, 1, figsize=(20, 8))
        plt.subplot(221)
        for key in hIndex_df_dict_on_year:
            hindex_df = hIndex_df_dict_on_year.get(key)
            df_mean = hindex_df.groupby('Year').mean()
            sns.lineplot(x='Year', y='price_index', data=df_mean,
                         label= key + ' bedroom')
        plt.ylabel('Mean Home Index of ' + str(group_name))
        plt.xlabel('Year')
        hIndex_start_year1 = 2011
        hIndex_start_year1s = []
        while hIndex_start_year1 <= int(start_year):
            hIndex_start_year1s.append(hIndex_start_year1)
            hIndex_start_year1 += 1
        pos = hIndex_start_year1s
        lab = hIndex_start_year1s
        plt.xticks(pos, lab)
        plt.legend()
        plt.grid()
        plt.subplot(222)
        sns.lineplot(x='Year', y='Unemployment Rate', data=cspds_df, label='Unemployment Rate of ' + group_name)
        cspds_yr = int(cspds_start_yr)
        cspds_yrs = []
        while cspds_yr <= int(cspds_end_yr):
            cspds_yrs.append(cspds_yr)
            cspds_yr += 1
        # yrs = cspds_df['Year']
        pos = cspds_yrs
        lab = cspds_yrs
        plt.xticks(pos, lab)
        plt.legend()
        plt.grid()
        plt.subplot(223)
        sns.lineplot(x='Year', y='Crime Rate', data=cspds_df, label='Crime Rate of ' + group_name)
        plt.suptitle('Yearly Home Index Mean, Unemployment Rate and Crime Rate')
        plt.xticks(pos, lab)
        plt.legend()
        plt.grid()
        plt.show()
        plt.tight_layout()

# To run the program provide the inputs below
real_estate_corr = RealEstateCorrelation()
cspds_df = real_estate_corr.get_hindex_cspds_corr('All', 'State', 'NY', 'State', 'New York', '2011', '2021')
corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df = real_estate_corr.get_hindex_sp_corr_fr_yrs("All", 'State', 'NY', '2021')
hIndex_df_dict_on_year = real_estate_corr.get_raw_hindex('All', 'State', 'NY', '2021')
sp_data_on_year = real_estate_corr.sp_cspds_data.get_sp_data('2011', '2021')
real_estate_corr.plot_trend_on_yr_multi_plot('NY', hIndex_df_dict_on_year, sp_data_on_year, corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df, cspds_df, '2021', '2011', '2021')

# For additional states uncomment and run the application
#
# cspds_df = real_estate_corr.get_hindex_cspds_corr('All', 'State', 'VA', 'State', 'Virginia', '2011', '2020')
# corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df = real_estate_corr.get_hindex_sp_corr_fr_yrs('ALl', 'State', 'VA', '2020')
# hIndex_df_dict_on_year = real_estate_corr.get_hindex_mean_on_col('All', 'State', 'VA', '2020', 'Year')
# sp_data_on_year = real_estate_corr.sp_cspds_data.get_sp_data('2011', '2020')
# real_estate_corr.plot_trend_on_yr_multi_plot('VA', hIndex_df_dict_on_year, sp_data_on_year, corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df, cspds_df, '2020', '2011', '2020')
#
# cspds_df = real_estate_corr.get_hindex_cspds_corr('All', 'State', 'TX', 'State', 'Texas', '2011', '2020')
# corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df = real_estate_corr.get_hindex_sp_corr_fr_yrs('ALl', 'State', 'TX', '2020')
# hIndex_df_dict_on_year = real_estate_corr.get_hindex_mean_on_col('All', 'State', 'TX', '2020', 'Year')
# sp_data_on_year = real_estate_corr.sp_cspds_data.get_sp_data('2011', '2020')
# real_estate_corr.plot_trend_on_yr_multi_plot('TX', hIndex_df_dict_on_year, sp_data_on_year, corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df, cspds_df, '2020', '2011', '2020')
# #
# cspds_df = real_estate_corr.get_hindex_cspds_corr('All', 'State', 'CA', 'State', 'California', '2011', '2020')
# corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df = real_estate_corr.get_hindex_sp_corr_fr_yrs('ALl', 'State', 'CA', '2020')
# hIndex_df_dict_on_year = real_estate_corr.get_hindex_mean_on_col('All', 'State', 'CA', '2020', 'Year')
# sp_data_on_year = real_estate_corr.sp_cspds_data.get_sp_data('2011', '2020')
# real_estate_corr.plot_trend_on_yr_multi_plot('CA', hIndex_df_dict_on_year, sp_data_on_year, corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df, cspds_df, '2020', '2011', '2020')
#
# cspds_df = real_estate_corr.get_hindex_cspds_corr('All', 'State', 'IL', 'State', 'Illinois', '2011', '2020')
# corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df = real_estate_corr.get_hindex_sp_corr_fr_yrs('ALl', 'State', 'IL', '2020')
# hIndex_df_dict_on_year = real_estate_corr.get_hindex_mean_on_col('All', 'State', 'IL', '2020', 'Year')
# sp_data_on_year = real_estate_corr.sp_cspds_data.get_sp_data('2011', '2020')
# real_estate_corr.plot_trend_on_yr_multi_plot('IL', hIndex_df_dict_on_year, sp_data_on_year, corr_lst, num_bed_corr_lst_dict, hIndex_df_dict, sp_df, cspds_df, '2020', '2011', '2020')

# plt.show()
# plt.tight_layout()