## Indeed Job Scraper

Majority of the code credited to this repo: https://github.com/tarunsinghal92/indeedscrapperlatest

Simple and updated python script that gets job data for cities and job titles.

To run the main logic:
```
python3 scraper.py
```

This repo isn't configurable with another file so queries, cities, and number of jobs to be scraped should be modified in the scraper.py source code.

To change results per city modify the following:
```
max_results_per_city = 100
```

To add jobs or change the existing set, modify the following:
```
job_set = ['software+engineer']
```
NOTE: make sure to add the '+' between separate words.

To add cities or change the existing set, modify the following:
```
city_set = ['Chicago']
```
NOTE: there is a full_city_set which has a bunch of major cities and the proper formatting required.

The result should be in a properly indexed CSV file.