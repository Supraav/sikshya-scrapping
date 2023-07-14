from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=40)
    data = {"country": "India", "course": []}

    def get_data_by_facultyURL(href, faculty_name, course_data):  
        context = browser.new_context()
        coursepage = context.new_page()
        coursepage.goto(href)
        coursepage.wait_for_selector('#ACPWrapper')

        main_course_div = coursepage.query_selector('#ACPWrapper')
        inner_course_div = main_course_div.query_selector('#acp-tuples')
        responsive_course_div = inner_course_div.query_selector('#rspnsv-tpl')
        # print(responsive_course_div.inner_html())
        individual_divs = responsive_course_div.query_selector_all('.shadowCard.ctpCard.CLP')
        for individual_div in individual_divs:
            # name of course
            title = individual_div.query_selector('h3.instNamev2').inner_text()

            # duration of course 
            year = individual_div.query_selector('.inlineLabel').inner_text().strip('\xa0()') if individual_div.query_selector('.inlineLabel') else ""

            # for no of seats and total fee
            more_div = individual_div.query_selector('.contSec.acpContainer')

            seats = None
            fees = None
            rows = more_div.query_selector_all('.flexRowEqual')
            for row in rows:
                label = row.query_selector('.blockLabel').inner_text().strip()
                value_div = row.query_selector('.valueTxt')
                value = value_div.inner_text().strip()
                if label == 'No. of Seats':
                    seats = value
                elif label == 'Total Tuition Fees':
                    fees = value.replace('Get Fee Details', '')


            course_data.append({
                'Title': title,
                'Year': year,
                'Faculty': faculty_name,
                'Seats': seats,
                'Total_Fees': fees
            })

        browser.close()
          
    faculty_data = 'MD'
    url = 'https://www.shiksha.com/university/jawaharlal-nehru-university-delhi-4225/courses/ma-bc'
    get_data_by_facultyURL(url, faculty_data, data["course"]) 
    print(data)
