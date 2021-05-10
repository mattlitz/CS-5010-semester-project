import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def convert_column_to_rows(df):
    df_new = pd.melt(df, id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName',
       'State', 'City', 'Metro', 'CountyName'], var_name='Date', value_name='price_index')
    return df_new


def get_hIndex_fr_year_melt_later(num_bed, group_id, group_val, year):
    if int(year) > 2021 or int(year) < 2011:
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
    df_new = convert_column_to_rows(df_grp)
    df_new['Year'] = pd.DatetimeIndex(df_new['Date']).year
    df_new['Month'] = pd.DatetimeIndex(df_new['Date']).month
    df_new['YearMonth'] = pd.to_datetime(df_new['Date']).dt.strftime('%Y-%m')
    df_new = df_new[df_new['Year'] == int(year)]
    df_new = df_new[df_new['Month'] != '.']
    df_new = df_new[df_new['price_index'] != 'NaN']
    df = df_new.dropna()
    df_grp_month = df.groupby('Month').mean()
    print('Home Index Data for '+str(group_id)+" with "+str(group_val))
    print(df_grp_month.head(12))
    return df_grp_month, year


def get_sp_data(year):
    if int(year) > 2021 or int(year) < 2011:
        print("Date is out of range. Please provide Date between 2011 3 and 2021 4")
    else:
        df = df_sp500[df_sp500['SP500'] != '.']
        df_tmp =df.groupby('DATE_YEAR').get_group(int(year))
        df_month = df_tmp.groupby('DATE_MONTH').mean()
        print("SP500 data")
        print(df_month.head(12))
        return df_month


def get_hindex_sp_corr_on_year(num_bed,year, group_id, group_val):
    sp_df = get_sp_data(year)
    # sp_df['SP500'] = sp_df.SP500.astype(float)
    if num_bed == '1':
        hindex_1b, year = get_hIndex_fr_year_melt_later("1", group_id, group_val, str(year))
        sp_hindex_1b_corr = sp_df['SP500'].corr(hindex_1b['price_index'])
        print('Correlation for 1 bed single family house with SP500 for the year '+str(year)+' is ' + str(sp_hindex_1b_corr))
    elif num_bed == '2':
        hindex_2b, year = get_hIndex_fr_year_melt_later("2", group_id, group_val, str(year))
        sp_hindex_2b_corr = hindex_2b['price_index'].corr(sp_df['SP500'])
        print('Correlation for 2 bed single family house with SP500 for the year '+str(year)+' is ' + str(sp_hindex_2b_corr))
    elif num_bed == '3':
        hindex_3b, year = get_hIndex_fr_year_melt_later("3", group_id, group_val, str(year))
        sp_hindex_3b_corr = sp_df['SP500'].corr(hindex_3b['price_index'])
        print('Correlation for 3 bed single family house with SP500 for the year '+str(year)+' is ' + str(sp_hindex_3b_corr))
    elif num_bed == '4':
        hindex_4b,year = get_hIndex_fr_year_melt_later("4", group_id, group_val, str(year))
        sp_hindex_4b_corr = hindex_4b['price_index'].corr(sp_df['SP500'])
        print('Correlation for 4 bed single family house with SP500 for the year '+str(year)+' is ' + str(sp_hindex_4b_corr))
    elif num_bed == '5':
        hindex_5b, year = get_hIndex_fr_year_melt_later("5", group_id, group_val, str(year))
        sp_hindex_5b_corr = hindex_5b['price_index'].corr(sp_df['SP500'])
        print('Correlation for 5 bed single family house with SP500 for the year '+str(year)+' is ' + str(sp_hindex_5b_corr))
    elif num_bed.upper() == 'ALL':
        hindex_1b, year = get_hIndex_fr_year_melt_later("1", group_id, group_val, str(year))
        hindex_2b, year = get_hIndex_fr_year_melt_later("2", group_id, group_val, str(year))
        hindex_3b, year = get_hIndex_fr_year_melt_later("3", group_id, group_val, str(year))
        hindex_4b, year = get_hIndex_fr_year_melt_later("4", group_id, group_val, str(year))
        hindex_5b, year = get_hIndex_fr_year_melt_later("5", group_id, group_val, str(year))

        sp_hindex_1b_corr = hindex_1b['price_index'].corr(sp_df['SP500'])
        sp_hindex_2b_corr = hindex_2b['price_index'].corr(sp_df['SP500'])
        sp_hindex_3b_corr = hindex_3b['price_index'].corr(sp_df['SP500'])
        sp_hindex_4b_corr = hindex_4b['price_index'].corr(sp_df['SP500'])
        sp_hindex_5b_corr = hindex_5b['price_index'].corr(sp_df['SP500'])

        print('Correlation for 1 bed single family house with SP500 for the year '+year+' is ' + str(sp_hindex_1b_corr))
        print('Correlation for 2 bed single family house with SP500 for the year '+year+' is ' + str(sp_hindex_2b_corr))
        print('Correlation for 3 bed single family house with SP500 for the year '+year+' is ' + str(sp_hindex_3b_corr))
        print('Correlation for 4 bed single family house with SP500 for the year '+year+' is ' + str(sp_hindex_4b_corr))
        print('Correlation for 5 bed single family house with SP500 for the year '+year+' is ' + str(sp_hindex_5b_corr))


def plot_trend_on_yr_multi_plot(group_id, group_name, year, bed_type):
    plt.figure(figsize=(80, 5))
    plt.subplot(121)
    if bed_type == '1':
        df_1b, column_name = get_hIndex_fr_year_melt_later('1', group_id, group_name, year)
        sns.lineplot(x='Month', y='price_index', data = df_1b, label = 'Single Family Home Index 1 bedroom')
    elif bed_type == '2':
        df_2b, column_name = get_hIndex_fr_year_melt_later("2", group_id, group_name, year)
        sns.lineplot(x='Month', y='price_index', data = df_2b, label='Single Family Home Index 2 bedroom')
    elif bed_type == '3':
        df_3b, column_name = get_hIndex_fr_year_melt_later("3", group_id, group_name, year)
        sns.lineplot(x='Month', y='price_index', data=df_3b, label='Single Family Home Index 3 bedroom')
    elif bed_type == '4':
        df_4b, column_name = get_hIndex_fr_year_melt_later("4", group_id, group_name, year)
        sns.lineplot(x='Month', y='price_index', data=df_4b, label='Single Family Home Index 4 bedroom')
    elif bed_type == '5':
        df_5b, column_name = get_hIndex_fr_year_melt_later("5", group_id, group_name, year)
        sns.lineplot(x='Month', y='price_index', data=df_5b, label='Single Family Home Index 5 bedroom')
    elif bed_type.upper() == 'ALL':
        df_1b, column_name = get_hIndex_fr_year_melt_later("1", group_id, group_name, year)
        df_2b, column_name = get_hIndex_fr_year_melt_later("2", group_id, group_name, year)
        df_3b, column_name = get_hIndex_fr_year_melt_later("3", group_id, group_name, year)
        df_4b, column_name = get_hIndex_fr_year_melt_later("4", group_id, group_name, year)
        df_5b, column_name = get_hIndex_fr_year_melt_later("5", group_id, group_name, year)
        sns.lineplot(x='Month', y='price_index', data=df_1b, label='Single Family Home Index 1 bedroom')
        sns.lineplot(x='Month', y='price_index', data=df_2b, label='Single Family Home Index 2 bedroom')
        sns.lineplot(x='Month', y='price_index', data=df_3b, label='Single Family Home Index 3 bedroom')
        sns.lineplot(x='Month', y='price_index', data=df_4b, label='Single Family Home Index 4 bedroom')
        sns.lineplot(x='Month', y='price_index', data=df_5b, label='Single Family Home Index 5 bedroom')
    plt.ylabel('Home Index of ' + str(group_name))
    plt.xlabel('Year - '+year)
    pos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lab = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.xticks(pos, lab)
    plt.legend()
    plt.grid()
    plt.subplot(122)
    sp_df = get_sp_data(year)
    sns.lineplot(x='DATE_MONTH', y='SP500', data=sp_df, label='SP500')
    plt.ylabel('S&P 500')
    plt.xlabel('Year - '+year)
    pos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lab = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    plt.xticks(pos, lab)
    plt.legend()
    plt.grid()
    plt.show()


df_sp500 = pd.read_csv("/Users/abhijeet/Desktop/MSDS/CSSemProject/SP500.csv")
df_sp500 = df_sp500[df_sp500['SP500'] != '.']
df_sp500['SP500'] = df_sp500.SP500.astype(float)
df_sp500['DATE'] = pd.to_datetime(df_sp500['DATE'])
df_sp500['DATE_YEAR'] = pd.DatetimeIndex(df_sp500['DATE']).year
df_sp500['DATE_MONTH'] = pd.DatetimeIndex(df_sp500['DATE']).month
df_sp500['YearMonth'] = pd.to_datetime(df_sp500['DATE']).dt.strftime('%Y-%m')

# get_hindex_sp_corr_on_year('3',2020, 'State', 'VA')
get_hindex_sp_corr_on_year('4',2017, 'RegionName', 75024)
# get_hindex_sp_corr_on_year('3',2017, 'State', 'VA')
plot_trend_on_yr_multi_plot('RegionName', 75024, '2017', '4')