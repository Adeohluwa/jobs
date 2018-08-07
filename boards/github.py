#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as Soup
import json


def validate(field):
    return field if field else 'N/A'


class Github:
    start_url = "https://jobs.github.com"
    first_page_url = f'{start_url}/positions'
    all_postings = []

    def get_postings(self, url=first_page_url):
        with requests.get(url) as response:
            if response.status_code == 200:
                soup = Soup(response.text, 'lxml')

                postings = soup.find_all('tr')

                next_page = soup.find('a', class_='js-paginate button')

                if next_page:
                    # remove next page <tr> element
                    postings.remove(postings[-1])

                for posting in postings:
                    posting_data = self.posting_details(posting)
                    self.all_postings.append(posting_data)

                if next_page:
                    next_page_href = next_page['href']
                    next_page_url = f'{self.start_url}{next_page_href}'
                    self.get_postings(url=next_page_url)

                return self.all_postings

    def posting_details(self, posting):

        job = posting.find('td', class_='title').find('h4').find('a')
        job_title = job.get_text()
        job_url = self.start_url + str(job['href'])

        company_name = posting.find('a', class_='company').get_text()
        company_url = self.start_url + str(
            posting.find('a', class_='company')['href'])
        contract_type = posting.find('strong', class_='fulltime').get_text()
        location = posting.find('span', class_='location').get_text()
        date_created = posting.find(
            'span', class_='location').find_next_sibling('span').get_text()

        if job_url:
            posting_response = requests.get(job_url)
            posting_response_soup = Soup(posting_response.text, 'lxml')

            job_description = str(
                posting_response_soup.find('div', class_='column main '))

            application = posting_response_soup.find(
                'div', class_='module highlighted').find('a')
            if application:
                application_link = application['href']
            else:
                application_link = ''

        posting = {
            'Job Title': validate(job_title),
            'Job URL': validate(job_url),
            'Company': validate(company_name),
            'Company URL': validate(company_url),
            'Contract Type': validate(contract_type),
            'Location': validate(location),
            'Job Description': validate(job_description),
            'Date Created': validate(date_created),
            'Application Link': validate(application_link)
        }

        return posting

    def output(self):
        data = self.get_postings()

        with open('github_jobs.json', 'a') as output_file:
            json.dump(data, output_file)


def main():
    if __name__ == '__main__':
        github = Github()
        github.output()


main()
