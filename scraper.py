import requests
import pandas as pd
import time 
import bs4
from bs4 import BeautifulSoup
# Based on this: https://github.com/tarunsinghal92/indeedscrapperlatest


# get soup object
def get_soup(text):
    return BeautifulSoup(text, "lxml", from_encoding="utf-8")


# extract company
def extract_company(div): 
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
        for b in company:
            return (b.text.strip())
    else:
        sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
        for span in sec_try:
            return (span.text.strip())
    return 'NOT_FOUND'


# extract job salary
def extract_salary(div): 
    try:
        div_two = div.find(name='div', attrs={'class':'salarySnippet holisticSalary'})
        div_three = div_two.find('span', {'class':'salaryText'})
        print(div_three.text.strip())
        return div_three.text.strip()
    except:
        return ('NOT_FOUND')
    return 'NOT_FOUND'


# extract job location
def extract_location(div):
    for divs in div.findAll('div', attrs={'class': 'location accessible-contrast-color-location'}):
        return (divs.text)
    return 'NOT_FOUND'


# extract job title
def extract_job_title(div):
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return (a['title'])
    return 'NOT_FOUND'


# extract jd summary
def extract_summary(div): 
    divs = div.findAll('div', attrs={'class': 'summary'})
    for div_1 in divs:
        return (div_1.text.strip())
    return 'NOT_FOUND'
 

# extract link of job description 
def extract_link(div): 
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        return (a['href'])
    return 'NOT_FOUND'


# extract date of job when it was posted
def extract_date(div):
    try:
        spans = div.findAll('span', attrs={'class': 'date'})
        for span in spans:
            return (span.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'


# extract full job description from link
def extract_fulltext(url):
    try:
        page = requests.get('http://www.indeed.com' + url)
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
        divs = soup.findAll('div', attrs={'class': 'jobsearch-jobDescriptionText'})
        for div in divs:
            return (div.text.strip())
    except:
        return 'NOT_FOUND'
    return 'NOT_FOUND'


# write logs to file
def write_logs(text):
    # print(text + '\n')
    f = open('log.txt','a')
    f.write(text + '\n')  
    f.close()


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
    
    # for each job role
    for job_qry in job_set:
        
        # count
        cnt = 0
        startTime = time.time()
        # dataframe
        df = pd.DataFrame(columns = ['unique_id', 'city', 'job_qry','job_title', 'company_name', 'location', 'summary', 'salary', 'link', 'date', 'full_text'])
    
        # for results
        for start in range(0, max_results_per_city, 10):

            # get dom 
            page = requests.get('http://www.indeed.com/jobs?q=' + job_qry +'&l=' + str(city) + '&start=' + str(start))

            #ensuring at least 1 second between page grabs                    
            time.sleep(1)  

            #fetch data
            soup = get_soup(page.text)
            divs = soup.find_all(name="div", attrs={"class":"row"})
            
            # if results exist
            if(len(divs) == 0):
                break

            # for all jobs on a page
            for div in divs: 
                #specifying row num for index of job posting in dataframe
                num = (len(df) + 1) 
                cnt = cnt + 1

                #job data after parsing
                job_post = [] 

                #append unique id
                job_post.append(div['id'])
                job_post.append(city)
                job_post.append(job_qry)
                job_post.append(extract_job_title(div))
                job_post.append(extract_company(div))
                #job_post.append(extract_location(div))
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

            #debug add
            write_logs(('Skipped =>') + '\t' + city  + '\t' + job_qry + '\t' + str(-1) + '\t' + str(-1) + '\t' + str(time.time() - startTime) + '\t' + ('file_' + str(file)))
        
        # increment file
        file = file + 1