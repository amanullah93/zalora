# zalora
# zalora_case_study
Given a dataset here https://storage.googleapis.com/zalora-interview-data/bitstampUSD_1-min_data_2012-01-01_to_2020-09-14.csv that has the bitcoin prices from 2012 to 2020, can you spot as many successful trades as possible. 

The Solution requirements : 

You can download the dataset for exploration first if you want, but the solution should call an api to download the file first and load it somewhere in your system.

After the data is loaded you can do all the possible transformations needed to help you get the successful trades .

Once you have the successful trades please load the results into your own choice of storage. (CSV, RDBMS, NoSQL, .. etc) .

Every trade should have the following columns: 
Buying date 
Buy price 
Selling date 
Sell price 
ROI percentage  ( return on investment)  for example if the trader buys bitcoin with 1 USD and sells it for 2 USD then the ROI percentage would be 100% return.

The data has the bitcoin price per minute, we don’t need that short traders, we need trades on the day level so instead of buying bitcoin on 2020-01-01 01:00:00 and sell it on 2020-01-01 02:00:00, the result should have something like buying bitcoin on 2020-01-01 and selling on 2020-01-05 for example.  

The pipeline should do all of the above steps automatically, you can use your prefered programming language, tools, .. etc 

# Solution:

Install required libraries using requirements.txt
Please run below command to execute the code.

python bitcoin.py >> output.txt

Final report will be generated in statistics_report.csv file

Overall runtime of the code including reading data directly using pandas is 13 minutes.
Using different interval in number of days, successful trade count has been generated in the output file 'statistics_report.csv'
