from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import json, time
from urllib.parse import urljoin

output_file = "collz_list.json"
college = {}

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=25)
    context = browser.new_context()
    topcolzpage = context.new_page()

    main_url = "https://www.careers360.com/colleges/india-colleges-fctp?page=118&entity_type=2&sort_by=1"

    while True:
        print('getting into page:', main_url)
        topcolzpage.goto(main_url)
        time.sleep(7)

        # Skipping the ad on the bottom right
        try:
            topcolzpage.wait_for_selector('.react-responsive-modal-container.react-responsive-modal-containerCenter')
            topcolzpage.query_selector('#common-signin-close').click()
        except:
            time.sleep(2)

            # Passing playwright content to bs4
            page_html = topcolzpage.content()
            soup = bs(page_html, 'lxml')

            section_divs = soup.find('section', class_='college_listing_page')
            undefined_div = section_divs.find('div', class_='undefined')
            cont_divs = undefined_div.find('div', class_='row')
            desktop_div = cont_divs.find('div', class_='desktop_right_side col-md-9')
            empty_divs = desktop_div.find_all('div', class_=None)
            for empty_div in empty_divs:
                h3_text = empty_div.find('h3', class_='college_name d-md-none')
                if h3_text:
                    link = h3_text.find('a')['href']
                    college[urljoin(main_url, link)] = False


            # Pagination
            page_div = desktop_div.find('div', class_='college_pagination')
            last_pagination_link = page_div.find('a', class_='pagination_list_last')
            if last_pagination_link:
                next_page_url = last_pagination_link['href']
                main_url = next_page_url 
            else:
                break

            # Save the data for all pages into the json file
            try:
                results={}
                with open(output_file, 'r') as file:
                    results = json.load(file)

                with open(output_file, 'w') as file:
                    results={**results,**college}
                    json.dump(results, file, indent=3)

            except Exception as e:
                print("Error opening file,", e)
                with open(output_file, 'w') as file:
                    json.dump(college, file, indent=3)

            print('finished')

    context.close()
    browser.close()
