from playwright.sync_api import sync_playwright
import json

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=25)
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://www.shiksha.com/science/ranking/top-universities-colleges-in-india/121-2-0-0-0')
    filter_element = page.query_selector('.fltlft.filter-area.ctp_sidebar')

    filter_block = filter_element.query_selector_all('div.filter-block >> text="Location"')

    location_text = filter_block[0].inner_text()
    print(location_text)

    page.wait_for_timeout(5000)

    filter_content_div = page.query_selector('.filter-content')

    # checkbox_elements = filter_content_div.query_selector('.fix-scroll')
    checkbox_li_elements = filter_content_div.query_selector_all('ul.sidebar-filter li.enable')

    for checkbox_li in checkbox_li_elements:
        checkbox = checkbox_li.query_selector('input.filter-chck')
        checkbox.wait_for_element_state("visible", timeout=5000)
        checkbox.wait_for_element_state("enabled", timeout=5000)
        checkbox.wait_for_element_state("stable", timeout=5000)
        
        checkbox.click()

        print(checkbox.inner_text())
        print('************************')

        checkbox.click()

    page.close()
    context.close()
    browser.close()
