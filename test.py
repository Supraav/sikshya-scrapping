from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import json,time
from urllib.parse import urljoin



output_file='delhiunis3.json'

city={}

#writing the url_tracking file if not exists otherwise reading from it.


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=70)
    context = browser.new_context()
   
    #main city urls to get all the links of the cities and append in a dictionary named city as {name of city:code of city}
    main_url='https://www.shiksha.com/science/ranking/top-universities-colleges-in-india/121-2-0-0-0'

    data={"course":[]}

    test_url='https://www.shiksha.com/university/delhi-university-du-24642'    
    print('getting into college:',test_url)
    testdivpage = context.new_page()
    #collegedivpage is the URL of all individual div universities.
    testdivpage.set_default_timeout(0)
    testdivpage.goto(test_url)
    
    time.sleep(3)
    testdivpage.wait_for_selector('#iulp_lhs_container')

    #about(need to change)
    body_section_div=testdivpage.query_selector('#iulp_lhs_container')
    inner_section=body_section_div.query_selector('.paper-card.spacingVariation')
    about_div=inner_section.query_selector('._1003._58f5')
    aaaa=about_div.query_selector('.wikiContents._021e.collapsed.ca53._5333.a78b')
    aaaa.locator('._5ee4').click()
    # bbbb.locator('._5ee4').click()

        # data["about"]=about_inner_html

