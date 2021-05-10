CS 5010 Project
05.09.2021
─
Matthew Litz, Abhijeet Chawhan, Abhishek Bada





# Introduction
During the COVID pandemic, the size of the US housing market increased dramatically as buyers were enticed by record lower interest rates.  This market piqued our interest and drove us to see what relationships whether economically, socially , and even geographically affected the housing market.
For most Americans purchasing a home will be the largest financial decision they make in their entire lives. This analysis could give helpful insight to those purchasers and even investors on when and where to buy homes so their investment is safe.
##Github link 
https://github.com/mattlitz/CS-5010-semester-project

# Goals
Analyze correlations between our predictor variables and "Price" to establish which ones most heavily influence house prices.​
To convert House Index Data into useful information and subsequently into knowledge to find correlation and prediction factors.  ​
Explore the influence from COVID and other factors on the House price index in the granularity of geography.
Predict future prices using the predictors selected

# Project Scope
The goal of this project is to give the stakeholders an idea of the correlation that exists between various predictors that affect the house price.  How the statistical correlation changes from County/City to State levels and How the relationship of these said predictors interacts with the Price factor.  Check to see how geographic granularity affects the accuracy of our predictive models. Give users a user interface (UI) to visualize the data so they make better informed choices during their house purchase journey. Overall, we would like to provide insight to customers so they make data driven decisions on what is most likely the largest purchase of their lives.
Data Set
The team initially set out to web scrape housing price data however quickly ran into many websites that blocked web scraping or ip banned the user after they had made so many get requests.   In lieu of these obstacles we reversed course and looked for datasets on kaggle and government websites.  Unemployment Rate, Crime Rate, S&P 500, Net Migration, and Mortgage Rate.

## Response
* Price 
    * Home Price 
    * 8 million rows of data
    * Quantitative discrete data 
    * Data Source: Kaggle
    
## Predictors 
* Bedrooms
    * Number of bedrooms for each house
    * 8 millions rows of data 
    * Quantitative discrete data with a range from 1 to 5
    * Data Source: Kaggle

* Unemployment Rate    
    * % unemployment per county from the years 2000 to 2020
    * 67599 data values with no missing data
    * Quantitative continuous data with a range from 0.0% to 29.4% and mean of 6.23%
    * Data Source: Geo FRED

* Crime Rate
    * Crime rate per 100,000 in each state from the years 2000 to 2020
    * 1050 data values with no missing data - 50 crime rates by state for 21 years
    * Quantitative continuous data with a range from 78.2 to 891.7 and mean of 385.7
    * Data Source: Crime Data Explorer

* Number of Bedrooms
    * Number of data values by bedroom size
    * Over 8 million values
    * Quantitative discrete data with a range from 1 to 5  
    * Data Source: Kaggle 

* S&P 500
    * Market index average for each month from 2000 to 2020
    * 252 data values with no missing data
    * Quantitative continuous data
    * Data Source: Yahoo Finance

The following predictors were selected due to their influence on Federal Reserve monetary policy.  To join with the housing price data, the data was resampled on a monthly basis and averaged.
* M2 Money Stock​
* S&P/Case-Shiller U.S. National Home Price Index​
* Consumer Price Index for All Urban Consumers: All Items in U.S. City Average​
* Effective Federal Funds Rate​
* 10-Year Treasury Constant Maturity Rate​
* US Unemployment Rate​
* Crime Rates​
* 30-Year Fixed Rate Mortgage Average in the United States​
* Personal Saving Rate of US Households​
* Crude Oil Prices: West Texas Intermediate (WTI)​
* Commercial and Industrial Loans, All Commercial Banks​
* Moody's Seasoned Aaa Corporate Bond Yield

# Data Cleaning 

Most of our data sets came from government agencies and were often reporting at the state/county level so there was rarely if ever a missing value in these data sets. The “Unemployment data set'' had a different column for each data hence the pandas function melt() was needed to collapse all of the dated columns into one date column.  The crime data set consisted of 50 csv files for each of the states and the glob library was very useful to iterate through all the files and concatenate them into one file.  Our housing data had many missing rows that had to be removed. Ultimately all the data sets were combined into one data set using the pandas merge function on the attributes “CountyName”, “State”, and “Date”.
Software Design

Our approach to analyzing this data set consisted of 3 stages.  First we would import and explore the dataset with our user interface that utilizes multi-predictor pair plots and correlations to identify predictors of interest.  Next after potential predictors are identified, we further explored their relationship to housing prices by performing an in-depth linear regression analysis.  Finally we developed machine learning methods to predict future prices of house given a set of predictors.

Our team developed an application that focuses on exploratory data analysis of the data set for users to examine regions of the United States. With so many potential predictors by which to predict future housing prices, the first step presents a pairplot (“PairPlot” tab) to examine pairwise relationships in the whole dataset.  A second graph is provided to perform a more extensive analysis of the relationship between two predictors in the “Correlation Line Plot” tab.  The python system output is routed to  the “Output” field in the main screen for users to review the Pearson Correlation coefficient of the two data series analyzed.  Dropdown menus are provided to select the start and stop periods of the timeframe under analysis.  The granularity of this application currently goes to the US county level.  PyQt was selected as the API to build the user interface.  In the future, this application would combine the regression analysis into the application. 

    In the second stage, we calculated the Pearson correlation between S&P500 and Zillow House Price Index (ZHPI) for a particular year and for a particular State, Zip, City or County. Correlation was also calculated between the Crime Rate and (ZHPI) and Unemployment rate and (ZHPI) for the last decade. The correlation calculation was accompanied with several plots to visualize the behavior of the correlation. The datasets were converted to data frames , aggregated, filtered, and list of values were deducted to get the list of values from two dataframes and the correlation was calculated. The python packages of Pandas, Matplotlib and seaborn were utilized to perform data processing and visualization. 
    
In the third stage we have a linear regression, multilinear regression, and machine learning function.  The linear regression takes our 5 predictors and creates a linear regression equation for each. The multilinear regression equation allows the user to choose the county that the equation outputs to as well as needing the inputs so it can predict the house value of those inputs.  Finally the machine learning model uses a training/test data set to check accuracy of predictions.

Figure 1: Screenshot of Housing Sector Exploratory Data Analysis user interface.

# Case Study 
At the onset of the COVID pandemic, there were several media reports (Marte, 2020) that people were migrating from large metropolitan areas to lower population regions.  The rationale for their relocation was to reduce the potential for COVID infection.  As a result, the combined reduction in population could increase housing inventory in the real estate market and thus lower prices since the supply is high and demand is lower.  To test this hypothesis, we utilized our user interface to examine the trends for New York County and compare it against Oswego County, a rural county in upstate New York.  Our expectation would be to see a relative drop in price during the time of the pandemic in New York County whereas we would see a price increase in rural areas like Oswego County.

## Stage 1:  Exploratory Data Analysis

Our first step was to explore the predictors using our Exploratory Data Analysis tool (Figure 2).  The predictor with an apparent correlation that we selected for further analysis was the S&P 500.  This index is a broad indicator on the health of the US stock market and could have a major influence on house prices.

Figure 2: Screenshot of the pairplot for New York County.

With our predictor of interest identified, we then utilized the Correlation Line Chart to analyze how the time series interact over the time period of the COVID pandemic.  The line plots and Pearson coefficient suggest a negative correlation between price and the S&P 500 and Housing Prices for New York County.  This is consistent with the first part of our hypothesis.

Figure 3: Screenshot of the correlation plot of House Price and S&P 500 for New York County.
Next we selected a rural county in New York (Oswego County) and reviewed the correlation between the S&P 500 and House Price.  The results showed a positive correlation which is also consistent with our hypothesis.


Figure 4: Screenshot of the correlation plot of House Price and S&P 500 for Oswego County.

## Stage 2:  Correlation Analysis

Correlation Calculation
 
Correlation can be calculated between data available in Time series format. The Pearson correlation calculates the relation between two quantities on what effect does a quantity which increases causes on another. 
 
We calculate the correlation between the Zillow House Price Index (ZHPI) of One Bedroom, Two Bedrooms, Three Bedrooms, Four Bedrooms and Five Bedrooms Single Family homes across the country and S&P 500 data over the years from 2010 till 2021. 
 
Correlation Calculation Features

Over the years from 2011 till 2021 between Zillow House Price Index (ZHPI) and S&P500 index for a particular State, County, City, Zip Code.
For a particular year, Ex. 2016, between Zillow House Price Index (ZHPI) and S&P500 index for a particular State, County, City, Zip Code.
Both the options mentioned in #1 and #2 also features One Bedroom, Two Bedrooms, Three Bedrooms, Four Bedrooms and Five Bedrooms Single Family Houses Price Index.
An option with an input of ‘All’ calculates the correlation between these quantities in a single plot and a single run. 
Over the years from 2011 till 2021, between the Zillow House Price Index (ZHPI) for all kinds of Bedrooms and Crime Rate in a particular state. 
Over the years from 2011 till 2021, between the Zillow House Price Index (ZHPI) for all kinds of Bedrooms and Unemployment Rate in a particular state.
 
 
 Solution Design, Class structure and Important Methods/Steps
Class ZillowHomeIndex
 
 
Figure 5: Read House Price Index dataset and create dataframe
 
The ZillowHomeIndex class contains methods to read and web scrape data to create dataframes. The data frame once constructed is aggregated based on the input of either City, State, County, Zip, etc.  
Once the data frames are aggregated, because the data present is columnar and time series data is required, the columns are converted into rows for the filter which is the ‘year’ that is input for the correlation calculation. 
A dictionary is created with the number of bedrooms as the key and the respective dataframe as the value. 
 
Highlight
 
The pandas melt () function helps in converting the columns to rows. It keeps all the required columns as they are in the original dataframe and creates rows out of the columns which are provided as input. In this case it is ‘Date’. 

 
 
Class Sp500CspdsData
 
This Sp500CspdsData class has a constructor that reads the SP500 data, Unemployment data and Crime data from the csv files. The constructor initializes by reading the SP500, Unemployment and Crime data. The dataframe is also aggregated on the yearly basis. 
 
Class RealEstateCorrelation
 
Algorithm and process Flow for Correlation Calculation
 
Figure 6: Correlation calculation
 
 
The S&P 500 dataset consists of rows on daily basis and hence it is aggregated on the monthly basis for the year given in the input. Two columns are added extra in the dataframe namely month-year and year. The mean values for each month’s S&P500 index over a year and over the years from 2011 till the year that is provided as input is persisted into a list. The house price index dataset is also read and a separate dataframe is created for each of the house price index based on the bedrooms. Because the price index is present in the columnar format for each of the months for each year, the columns are converted into rows for the year that is provided in the input. Then the dataframe is aggregated on State, Zip, or City and the value of index for each months and year is persisted into the list. The correlation calculation is performed at the end using both lists, list of values containing S&P500 and housing price index (for monthly basis). The correlation is also calculated for the mean value of the housing price index over the years from 2011 till the year that is provided as input. 
 
All the data that gets created out of dataframe aggregation on year, State is used for plotting as well. Various plots are created out of correlation data to display the changes in the correlation over the years for all kinds of bedrooms. 
 
The algorithm and design that is used for the correlation between the House price index and S&P500 is leveraged for the construction of plots between House price index values and crime rate and House price index and Unemployment rate.
 
Correlation Plots
Plots are created using the Seaborn and Matplotlib libraries of python plotting. The plots were created to display the analysis of our study and the plots show similar findings. A generic plot function ‘plot_trend_on_yr_multi_plot’ creates several plots based on the input provided. The plots are created using the data stored in the dictionary created out of the dataframe. The dataframe that is created for correlation calculations is utilized for plotting purposes. No separate read of dataframe is required. All the features of plotting viz, legend, grid, label, ticks subplots are utilized in the plotting functionality. 
 

Highlights:
 

 
 


Plots and Correlation Analysis                          Case Study 1 Contd...
 
Even though the correlation between the S&P500 and house price index for the New York county for the year 2020 showed negative correlation, the same correlation for the Oswego county showed a positive correlation indicating that the house price index went up when the S&P500 index went up.  However, when the correlation is calculated at the State level for all the bedrooms for the year 2020, the correlation is found to be positive. The same trend about correlation has been seen on the correlation values and plots in other metropolitan areas where in the correlation for some counties in the state between house price index and S&P500 show negative correlation but shows a positive correlation for that state for the same year. The plots present below demonstrate the correlation between HPI and S&P500 over the years. 
 
 
Figure 7: For the year 2020, positive correlation between S&P500 and Zillow house price index.
  
Figure 8: Calculation of correlation value between two quantities.
 

Figure 9: Mean price index for houses of all types of bedrooms in NY over the years, S&P500 index over the years
 
 


Figure 10: Correlation calculation between crime rate and House price index for NY. Crime Rate, Unemployment rate over the years from 2011 till 2021 for NY. 
 
Operational Procedure to Calculate correlation
All the steps to run the application to calculate the correlation calculation is present at the link below. 
ReadMe.docx

        Case Study 1 Contd…

Correlation Inference and Introduction to Linear Regression
The correlation calculations between the Zillow House Price Index and Unemployment Rate and Zillow House Price Index and Crime Rate also showed the negative correlation over the last decade as per the plots. This negative correlation between house price index and some of the common factors influencing the price index and the positive correlation between these two quantities at the state level led us to investigate further and come up with a model that would predict the house price and hence we built a multilinear regression model to predict the price of house. 

## Stage 3:  Prediction Model
Single Linear Regression Model
    We wanted to initially see how each of the predictors affected the “Price”.  Whether there was a negative or positive correlation across all the data covering the entire USA.  Below the linear regression model.



### Linear Regression Analysis per  Predictor:
* S&P 500
   * Y = 162248 + 38X
   * The predictor and the response have a direct relationship
* Bedrooms
   * Y = 4536 + 68705X
   * The predictor and the response have a direct relationship
* 30 Year Mortgage Rate
   * Y = 241703 - 467X
   * The predictor and the response have an inverse relationship
* Crime Rate
   * Y= 315113 -12238X
   * The predictor and the response have an inverse relationship
* Unemployment Rate
   * Y=187650 + 146X
   * The predictor and the response have a direct relationship

All of our predictors had the expected relationship except “Unemployment Rate”.  One would expect as the “Unemployment Rate” increases the housing prices would go down.   This will need further analysis however a possible explanation could be that if the rate goes up people are less likely to move hence decreasing the supply of houses on the market causing an increase in the price. It should be noted that the coefficient is very small.
Multi Linear Regression Model
    Below is the multilinear regression model equation for the entire USA. As you can see that several of the coefficients for each of the predictors do not emulate single linear regression equations.  This requires further investigation 
    Price= -3768341 Bedrooms -2.4 SP500 +14830 Rate -14126 Unemployment +209 Crime

    Using our model generated specifically for New York County and using the inputs State: NY, Bedrooms: 4, Mortgage Rate: 2.98%, S&P 500: 4140.71, Crime Rate: 7098, and Unemployment rate: 5.1% we got an output prediction price for $6,366,422. The zillow data says for this input and area the avg home price is $6-$8 million so our prediction is right within our range.

### Machine Learning Model
For the machine learning model a simple code set was used to evaluate test/train data with an 80/20 split of the data.  Below you can see as the granularity for the machine learning model was increased the clf score increased significantly almost a 10X increase in evaluation accuracy.   
All models are inaccurate at some point.  This saying is very accurate to the housing market where it is incredibly difficult to predict housing prices in America as the nation geographically is very large, with various industries, and ultimately has very large urban areas vs vast rural areas.

Machine Learning Test/Train Coefficient​
USA – 0.0394​
New York - 0.0461​
New York County-  0.3680

##Functional/Non-Functional Requirements

The following table presents the functional/non-functional requirements for this application

Functional
Non-Functional
The correlation values that gets calculated should be between 0 and 1
User interface responds fast enough with the changes in the county, state, City
The plots should correspond to the values calculated with correlation.
Correlation calculation, plots get executed under 30 seconds
The linear regression model should output the values for coefficients of the model equation.
The dataframe creation does not cause OutOfMemory exceptions. 
The UI should display the pair plot and the line plot for the year and county selected.
The plots, files and any temporary data gets deleted once the application shuts down gracefully. 




             








## Testing
We did some basic testing to make sure that our dataset had no zeros, missing data, duplicate values, and no NaN values.
 

 
## Beyond the original specifications
UI created to visualize various graphs see “Stage 1: Exploratory Analysis” Page 6
Explored linear regression analysis and machine learning analysis see    “Stage 3: Prediction Model” Page 14.
Conclusions
This application is a robust tool for assisting investors or future home buyers to identify influential predictors for housing in a county or state of interest and predict future prices.  This software is very-open ended when defining a hypothesis and users must make regional considerations for their analysis decisions.  
Results from our Case Study and general observations are as follows:

S&P 500 and House Price Index correlations are not affected by quantity of bedrooms.​
Machine learning analysis demonstrated that regions affect house prices.​
The analysis can be used by the secondary mortgage and real estate marketing companies to advertise efficiently. ​
Federal Reserve Monetary Policy affect Housing Prices​
Affected predictors: M2, Federal Funds Rate, 10-Year Treasury, 30-Year Mortgage Rate​
We have determined it is possible to build predictive models for US House Prices through our analysis of house index price data by converting into information(data frame manipulation) and subsequently into knowledge (regression model).

## Next Steps
In the next iteration of this project, the team would like to add multiple improvements across the entire project from scope to predictor variables.

Increase granularity of data to county level for all predictors​
Embed Multilinear-regression and machine learning into the  UI​
Use One-Hot encoding for the states categorical predictor​
Add interactive choropleth map to user interface
Statistical analysis of linear regression models​
Increase the number of predictors​
Social: Schools, Hospitals and Parks​
Economic: NASDAQ, Average Household Income​
Geographic: Close to busy roads

### Data Set References

*Housing Price/Bedroom - https://www.zillow.com/research/data/ 
*Crime Rate - https://crime-data-explorer.fr.cloud.gov/pages/explorer/crime/crime-trend
*Unemployment Rate - https://geofred.stlouisfed.org/map/
*Mortgage Rates - http://www.freddiemac.com/pmms/pmms30.html
*S&P 500 - https://finance.yahoo.com/quote/%5EGSPC/ 

###R eferences
*Marte, J. (2020, December 15). Fleeing New Yorkers resulted in an estimated $34 billion in lost income -study. Reuters. Fleeing New Yorkers resulted in an estimated $34 billion in lost income -study

*Richardson, B. (2021, January 26). Housing Market Gains More Value In 2020 Than In Any Year Since 2005. Forbes. https://www.forbes.com/sites/brendarichardson/2021/01/26/housing-market-gains-more-value-in-2020-than-in-any-year-since-2005/?sh=4b4ac55f4fe0


###Appendices
 Data Set for Correlation, Regression, and Machine Learning Analysis
