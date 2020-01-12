import requests
import pandas as pd
import time 
import bs4
from bs4 import BeautifulSoup
from helper import *

# limit per city
max_results_per_city = 100

# db of city 
city_set = ['Chicago']

# job roles
job_set = ['data+scientist']

# file num
file = 1

# loop on all cities
for city in city_set:
    for job_qry in job_set:
        cnt = 0
        startTime = time.time()

        df = pd.DataFrame(columns = ['unique_id', 'city', 'job_qry','job_title', 'company_name', 'location', 'summary', 'salary', 'link', 'date', 'full_text'])
    
        for start in range(0, max_results_per_city, 10):
            page = requests.get('http://www.indeed.com/jobs?q=' + job_qry +'&l=' + str(city) + '&start=' + str(start))
            time.sleep(1)  

            #fetch data
            soup = get_soup(page.text)
            divs = soup.find_all(name="div", attrs={"class":"row"})
            
            if(len(divs) == 0):
                break

            # for all jobs on a page
            for div in divs: 
                #specifying row num for index of job posting in dataframe
                num = (len(df) + 1) 
                cnt = cnt + 1

                #job data after parsing
                job_post = [] 

                job_post.append(div['id'])
                job_post.append(city)
                job_post.append(job_qry)
                job_post.append(extract_job_title(div))
                job_post.append(extract_company(div))
                job_post.append(city)
                job_post.append(extract_summary(div))
                job_post.append(extract_salary(div))
                link = extract_link(div)
                job_post.append(link)
                job_post.append(extract_date(div))
                job_post.append(extract_fulltext(link))

                #appending list of job post info to dataframe at index num
                df.loc[num] = job_post
                
                #debug add
                write_logs(('Completed =>') + '\t' + city  + '\t' + job_qry + '\t' + str(cnt) + '\t' + str(start) + '\t' + str(time.time() - startTime) + '\t' + ('file_' + str(file)))

            #saving df as a local csv file 
            df.to_csv('jobs_' + str(file) + '.csv', encoding='utf-8')
        
        else:
            write_logs(('Skipped =>') + '\t' + city  + '\t' + job_qry + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(time.time() - startTime) + '\t' + ('file_' + str(file)))
        
        # increment file
        file = file + 1
