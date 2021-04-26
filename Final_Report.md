# CS 5010 Final Report
By: Matt Litz, Abhijeet Chawal, Abhishek Bada

## Introduction
During the COVID pandemic we have all witnessed the housing market grow wildly, houses are selling sight unseen and $20,000 to $50,000 over asking price.  This market peaked our interest and drove us to see what relationships whether economically, socially , and even geographically affected the housing market.

For most Americans purchasing a home will be the largest financial decision they make in their entire lives. This analysis could give helpful insight to those purchasers and even investors on when and where to buy homes so their investment is safe.

## Goals

1. Evaluate how the performance of the S & P 500 is correlated to average house prices in each state and deduce which states housing markets are least affected by a downturn in the economy. 
1. Analyze correlations between unemployment, crime rate,  geographic location, and net domestic migration to deduce which predictors most heavily influence house price.
1. Explore seasonal trends of house prices to determine what time of year might have the best market for buyers and sellers. 


## Data Set

The team initially set out to web scrape housing price data however quickly ran into many websites that blocked web scraping or ip banned the user after they had made so many get requests.   In lieu of these obstacles we reversed course and looked for datasets on kaggle and government websites.  Unemployment Rate, Crime Rate, S&P 500, Net Migration, and Mortgage Rate.

### Predictors

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

* Mortgage Rate
  * % Mortgage Rate by month for 30-Year Fixed Mortgage from 2000 to 2020
  * 252 data values with no missing data
  * Quantitative continuous data with a range from 3.11 to 8.05 and mean of 5.09
  * Data Source: Freddiemac
