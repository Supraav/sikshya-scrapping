from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import json, time , requests
from urllib.parse import urljoin

url='https://www.careers360.com/colleges/school-of-open-learning-university-of-delhi-delhi?icn=college_page&ici=clg_16489_college_listing_tuple'
data={}
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=25)
    context = browser.new_context()
    topcolzpage = context.new_page()
    topcolzpage.goto(url)
    time.sleep(4)

    #playwright to bs4
    page_html = topcolzpage.content()
    soup = bs(page_html, 'lxml')

    address={'country':'India'}

    section_class=soup.find('section',{'data-test-id':"college-detail-banner"})
    banner_class=section_class.select_one('.banner_outer.banner_outer_new')


    #college name
    banner_name=section_class.find('nav',{'aria-label':"breadcrumb"})
    li_content=banner_name.find('li',{'aria-current':"page"}).text
    name=li_content.split(',')[0]
    data["college_name"]=name
    # print(name)

    #logo
    topcolzpage.wait_for_selector('.banner_collge_image .college_logo img')
    banner_image=banner_class.find('div',class_='banner_collge_image')
    college_logo=banner_image.find('div',class_='college_logo').img['src']
    data['logo']=college_logo
    # print(college_logo)
    
    #streetline address,ownership_type,affiliation
    banner_address=banner_class.find('div',class_='banner_collge_info')
    banner_tags=banner_address.find_all('div',class_='bannerTags')
    if banner_tags:
        location_tag=banner_tags[0]
        st_line_address=location_tag.text.replace('\xa0','')
        address["st_line_address"]=st_line_address
        # print(st_line_address)

        state=st_line_address.split(',')[1]
        address['state']=state
        # print(state)

        #Ownership (type of org: private/public),   affiliation
        college_info=banner_tags[2]

        #ownership type
        ownership_type=college_info.find('span').text.strip()
        data['ownership_type']=ownership_type
        # print(ownership_type)

        #affiliation_type
        affiliation = college_info.find('a').text.strip()
        data['affiliation']=affiliation
        # print(affiliation)

    #type of organization(college)
    data['organization_type']='COLLEGE'


    #longitude and latitude
    

    data['Address']=address
    print(data)