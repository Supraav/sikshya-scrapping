from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import json
from urllib.parse import urljoin
import time

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=40)
    data={"country":"India","course":[]}


    def get_data_by_facultyURL(href,faculty_name,course_data):  
        context = browser.new_context()
        coursepage = context.new_page()
        coursepage.goto(href)
        coursepage.wait_for_selector('#ACPWrapper')

        main_course_div=coursepage.query_selector('#ACPWrapper')
        inner_course_div=main_course_div.query_selector('#acp-tuples')
        responsive_course_div=inner_course_div.query_selector('#rspnsv-tpl')
        individual_divs=responsive_course_div.query_selector_all('.shadowCard.ctpCard.CLP')
        for individual_div in individual_divs:
            #name of course
            title = individual_div.query_selector('h3.instNamev2').inner_text()

            #duration of course 
            year = individual_div.query_selector('.inlineLabel').inner_text().strip('\xa0()') if individual_div.query_selector('.inlineLabel') else ""

            #for no of seats and total fee
            more_div=individual_div.query_selector('.contSec.acpContainer')

            # Extracting number of seats
            seats = more_div.query_selector('div:nth-child(1) > .valueTxt > div').inner_text() if more_div.query_selector('div:nth-child(1) > .valueTxt > div') else ""

            # Extracting total fees
            fee_element = more_div.query_selector('div:nth-child(2) > .valueTxt')
            fee = fee_element.inner_text() if fee_element else ""

            course_data.append({'Title': title, 
                                'Year': year,
                                'Faculty':faculty_name,
                                'seats':seats,
                                'fee':fee
                                })

        browser.close()


    
    

    
    faculty_data='MD'
    url='https://www.shiksha.com/university/jawaharlal-nehru-university-delhi-4225/courses/ma-bc'
    coz=get_data_by_facultyURL(url,faculty_data,data["course"]) 
    print(data)