"""
"""
# External packages
from datetime import datetime

# Constants
DATE_FORMAT_INPUT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_FORMAT_OUTPUT = "%d/%m/%Y à %Hh%Mm%Ss"

# Functions
def convert_raw_date(iso_date):
    date = datetime.strptime(iso_date, DATE_FORMAT_INPUT)
    return date.strftime(DATE_FORMAT_OUTPUT)

def process_job(job, predict_salary=True):
    # Difference between publication and now
    publication_date = datetime.strptime(job['datePosted'], DATE_FORMAT_INPUT)
    now = datetime.now()
    difference = now - publication_date
    job['dayDifference'] = difference.days
    job['hourDifference'] = difference.seconds // (60 * 60)
    job['minuteDifference'] = (difference.seconds // 60) % 60

    # Formal the salary
    if job['baseSalary'] is None:
        pass
    elif job['baseSalary'] > 9000:
        job['baseSalary'] = round(job['baseSalary'] / 12)
    elif job['baseSalary'] <= 500:
        job['baseSalary'] = None

    # Process the date format
    job['datePosted'] = convert_raw_date(job['datePosted'])

    # Add a special id
    job['html_id'] = 'a' + job['_id']    

    return job
