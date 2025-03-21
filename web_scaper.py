import pandas as pd # For data processing
from bs4 import BeautifulSoup # For data extraction
import requests # For web interaction
import datetime
from datetime import date, datetime, time


# Get HTML content
def get_data(url):
    r = requests.get(url)
    if r.status_code == 200:
        print('Connection Successful!')
    else:
        print(f'Conncetion was unsuccessful. Status code: {r.status_code}')
    soup = BeautifulSoup(r.text, 'html.parser')
    print('Data Successfully Extracted!')
    return soup


# Process data
def transform_data(soup) -> dict:
    job_title = [job.text.strip() for job in soup.find_all('h2', class_= 'title is-5')]
    print('\'Job Title\' data successfully retrieved!')
    company_name = [company.text.strip() for company in soup.find_all('h3', class_='subtitle is-6 company')]
    print('\'Company Name\' data successfully retrieved!')
    city = [location.text.strip().split(',')[0] for location in soup.find_all('p', class_='location')]
    print('\'Job City\' data successfully retrieved!')
    state = [location.text.strip().split(',')[1].strip() for location in soup.find_all('p', class_='location')]
    print('\'Job State\' data successfully retrieved!')
    date_posted = [date.text.strip() for date in soup.find_all('time')]
    print('\'Job Date Posted\' data successfully retrieved!')
    date_obj = [datetime.strptime(date, '%Y-%m-%d') for date in date_posted]
    print('\'Job Date Object\' data successfully retrieved from \'Date Posted\'.')
    day_of_week = [d_o_w.strftime('%A, %d %B') for d_o_w in date_obj]
    print('\'Job Day_of_Week Posted\' data successfully retrieved from \'Date Object\'.')
    year = [y.strftime('%Y') for y in date_obj]
    print('\'Job Year Posted\' data successfully retrieved from \'Date Object\'.')
    print('Transforming data to dataframe...')
    transformed_data = {
        'job_title': job_title,
        'company_name': company_name,
        'city': city,
        'state': state,
        'day_of_week_posted': day_of_week,
        'year_posted': year
    }
    print('Column data successfully retreived and transformed!')
    return transformed_data


# Store process data in csv format
def load_to_csv(transformed_data, file_name='job_listings_data') -> None:
    df = pd.DataFrame(transformed_data)
    record_no = df.shape[0]
    df.to_csv(f'{file_name}.csv')
    print(f'{record_no} number of records successfully loaded to csv!')


if __name__ == '__main__':
    url = 'https://realpython.github.io/fake-jobs/'

    soup = get_data(url)
    print('Commencing column data retrieval and transformation...')

    transformed_data = transform_data(soup)
    print('Loading data to csv...')

    load_to_csv(transformed_data)
