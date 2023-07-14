from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs

def get_cities():
    city={} 
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=40)
        context = browser.new_context()
        topunipage = context.new_page()
        city_url='https://www.shiksha.com/science/ranking/top-universities-colleges-in-india/121-2-0-0-0'
        topunipage.goto(city_url)
        side_elements=topunipage.query_selector('.ranking_blocks')
        inner_side_elements=side_elements.query_selector('.fltlft.filter-area.ctp_sidebar')

        filter_blocks = inner_side_elements.query_selector_all('.filter-block')

        for filter_block in filter_blocks:
            p_tag = filter_block.query_selector('p')
            if p_tag.inner_text() == 'Location':
                filter_content = filter_block.query_selector('.filter-content')
                fix_scroll=filter_content.query_selector('.fix-scroll')

                enable_items=fix_scroll.query_selector_all('.enable')
                for enable_item in enable_items:
                    #city number
                    input_element = enable_item.query_selector('input')
                    input_id = input_element.get_attribute('id')
                    zzz=input_id.split('-')
                    city_number=zzz[-1]

                    #city name
                    city_name_element=enable_item.query_selector('label')
                    cityzzz=city_name_element.inner_text()
                    city_name=cityzzz.split(" (")[0].strip()
                    # print(city_name)
                    city[city_name]=city_number

    return city