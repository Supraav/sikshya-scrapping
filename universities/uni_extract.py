from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import json,time
from urllib.parse import urljoin

output_file='delhiunis3.json'
url_tracking = {}
url_tracking_file = 'url_tracking.json'
city={}

#writing the url_tracking file if not exists otherwise reading from it.
try:
    with open(url_tracking_file, 'r') as file:
        url_tracking = json.load(file)
except FileNotFoundError:
    # Create a new file if it doesn't exist
    with open(url_tracking_file, 'w') as file:
        json.dump(url_tracking, file)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=25)
    context = browser.new_context()
    topunipage = context.new_page()
    
    #main city urls to get all the links of the cities and append in a dictionary named city as {name of city:code of city}
    main_url='https://www.shiksha.com/science/ranking/top-universities-colleges-in-india/121-2-0-0-0'
    
    topunipage.goto(main_url)
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

    #dictionary created.

    #looping for the dictionaries
    for name, code in city.items():
        city_url=main_url+'?ct[]='+code
        citypage = context.new_page()
        citypage.goto(city_url)
        print('GETTING INTO CITY ' + name)

        time.sleep(2)

        colz_div=citypage.query_selector('#rankingTupleWrapper')

        #individual college div locator of each city
        substring='rp_tuple'
        div_elements = colz_div.query_selector_all('div[id*="{0}"]'.format(substring))

        data={"course":[]}

        #function for course data called below(called below)/*/*
        def get_colleges_from_faculty_url(course_href,faculty_name,course_data):
            context = browser.new_context()
            coursepage = context.new_page()
            try:
                coursepage.goto(course_href)
                time.sleep(2)
                coursepage.wait_for_selector('#ACPWrapper')

                main_course_div=coursepage.query_selector('#ACPWrapper')
                inner_course_div=main_course_div.query_selector('#acp-tuples')
                responsive_course_div=inner_course_div.query_selector('#rspnsv-tpl')
                individual_divs=responsive_course_div.query_selector_all('.shadowCard.ctpCard.CLP')
                
                for individual_div in individual_divs:
                    #name of course
                    colz_name = individual_div.query_selector('h3.instNamev2').inner_text()

                    #degree
                    degree =None
                    if 'master' or 'masters' or 'mpt' or 'mfa' or 'mot' or 'MVA' or 'l.l.m' or 'llm' or 'mba' or 'md' or 'm.' or 'm'  in colz_name.lower():
                        degree='Masters'
                    elif 'm.' and 'b.' in colz_name.lower():
                        degree='Masters'
                    elif 'bachelor' or 'bachelors' or 'bfa' or 'bpa' or 'bva' or 'bba' or 'ba' or 'b.a.' or 'b.' in colz_name.lower():
                        degree="Bachelors"
                    elif 'pg' in colz_name.lower():
                        degree='Diploma'
                    elif 'p.g.' in colz_name.lower():
                        degree='Diploma'
                    elif 'diploma' in colz_name.lower():
                        degree='Diploma'
                    elif 'ph.d.' in colz_name.lower():
                        degree='Doctorate'
                    elif 'certificate' in colz_name.lower():
                        degree='Certificate'
                    else:
                        pass

                    #duration of course 
                    year = individual_div.query_selector('.inlineLabel').inner_text().strip('\xa0()') if individual_div.query_selector('.inlineLabel') else ""

                    #for no of seats and total fee
                    more_div=individual_div.query_selector('.contSec.acpContainer')

                    #seats and fees
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

                    course_data.append({'name': colz_name,
                                        'degree':degree, 
                                        'Faculty':faculty_name,
                                        'Year': year,
                                        'seats':seats,
                                        'fee':fees
                                        })

                coursepage.close()
            except:
                pass

        #extracting all the college urls of a state(e.g. JNU, Vellore)
        url_list=[]
        for div_element in  div_elements:
            href_element=div_element.query_selector('.tuple-inst-info')
            a_element = href_element.query_selector('a.rank_clg')
            href = a_element.get_attribute('href')
            full_colz_url=urljoin(main_url,href)
            url_list.append(full_colz_url)
            if full_colz_url not in url_tracking:
                url_tracking[full_colz_url] = False

            #looping for all the university urls to extract necessary datas
        for url in url_list:
            if url_tracking[url]:
                print(f"Skipping scrapped URL: {url}")
                continue
            try:    
                print('getting into college:',url)
                collegedivpage = context.new_page()
                #collegedivpage is the URL of all individual div universities.
                collegedivpage.goto(url)
                time.sleep(1.5)

                #scrapping all the datas from individual divs
                #name
                name_list=url.split('/')[-1]
                name_split=name_list.split('-')
                uni_name=' '.join(name_split[:-1])
                data["name"]=uni_name
                # print(uni_name)

                #the main header div containing(logo,address,est date and org type)
                header_div=collegedivpage.query_selector('._224b79 ')

                #logo
                try:
                    div_element = header_div.query_selector('.c55b78')
                    img_element = div_element.query_selector('img')
                    logo = img_element.get_attribute('src')
                    data["logo"]=logo
                except:
                    pass
                # print(logo)

                #ADDRESS INITIALIZED containing (country_name, st_line_address, city, lati,longi)
                address={"country_name":"India"}

                #st_line_address
                try:
                    address_div=header_div.query_selector('.b82d61')
                    address_element=address_div.query_selector('._94eae8')
                    st_line_address=address_element.inner_text()
                    address["street_line_address"]=st_line_address
                except:
                    pass
                # print(st_line_address)

                #city
                address['city']=name

                #li element for type_of_org,org type and established date
                lower_header=header_div.query_selector('ul.e1a898')
                li_elements = lower_header.query_selector_all('li')

                if len(li_elements)>2:
                    #type_of_org(public/private)
                    type_of_org = li_elements[1].inner_text().split('University')[0].strip()
                    data["type_of_org"]=type_of_org
                    #established_date
                    est_date=li_elements[2].inner_text().split('Estd. ')[1].strip()
                    data["est_date"]=est_date

                elif len(li_elements)==2:
                    #type_of_org(public/private)
                    type_of_org = li_elements[0].inner_text().split('University')[0].strip()
                    data["type_of_org"]=type_of_org
                    #established_date
                    est_date=li_elements[1].inner_text().split('Estd. ')[1].strip()
                    data["est_date"]=est_date
                else:
                    pass


                #organizationtype(college/uni)
                data["organization_type"] = "UNIVERSITY"


                #about(need to change)
                body_section_div=collegedivpage.query_selector('#iulp_lhs_container')
                inner_section=body_section_div.query_selector('.paper-card.spacingVariation')
                about_div=inner_section.query_selector('._1003._58f5')
                aaaa=about_div.query_selector('.wikiContents._021e.collapsed.ca53._5333.a78b')
                about_inner_html=aaaa.inner_html()
                data["about"]=about_inner_html


                #longitude and latitude
                collegedivpage.wait_for_selector('#rhsWidgetv2')
                div_url=collegedivpage.query_selector('#rhsWidgetv2')
                try:
                    map_url=div_url.query_selector('.abad a')
                    if map_url:
                        href = map_url.get_attribute('href')
                    coordinates = href.split('?q=')[1].split(',')
                    latitude=coordinates[0]
                    longitude=coordinates[1]
                    address["latitude"]=latitude
                    address["longitude"]=longitude
                except:
                    pass
                # print(latitude,longitude)

                #address added to data
                data["address"]=address
                #address end 

                # /*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/

                #faculty and courses
                #coursepage is the course's page for individual university
                course_url=url+'/courses'
                coursepage = context.new_page()
                coursepage.goto(course_url)
                time.sleep(2)

                #getting into divs
                coursepage.wait_for_selector('section[data-tupletype="BAC"]')
                sections_main_div = coursepage.query_selector('section[data-tupletype="BAC"]')
                section_container_div=sections_main_div.query_selector('._subcontainer')
                section_individual_divs=section_container_div.query_selector_all('.shadowCard.ctpCard.BAC')
                
                #looping for faculty divs
                for colz_div in section_individual_divs:
                    #faculty_div
                    faculty_div=colz_div.query_selector('._5f3e')
                    a_tag = faculty_div.query_selector('a')
                    #faculty
                    faculty_data = a_tag.inner_text()
                    href = a_tag.get_attribute('href')
                    course_href=urljoin(city_url,href)
                    print(course_href)
                    #courses
                    get_colleges_from_faculty_url(course_href,faculty_data,data["course"])
                
                #saving into json
                try:
                    results = []
                    with open(output_file, 'r') as file:
                        results = json.load(file)
                    
                    with open(output_file,'w') as file:
                        results.append(data)
                        json.dump(results, file, indent=3)
                except Exception as e:
                    print("Error opening file(ignore this error, still creates the json)",e)
                    results=[]
                    with open(output_file, 'w') as file:
                        results.append(data)
                        json.dump(results, file, indent=3)

                coursepage.close()

                # Mark URL as scrapped if successful
                url_tracking[url] = True

                # Append URL to tracking file
                with open(url_tracking_file, 'w') as file:
                    json.dump(url_tracking, file, indent=3)

            except Exception as e:
                print(f"Error scraping URL: {url} - {e}")
            print('finished scrapping:',url)
            print('--------------------------------------------------------------------------------------------- \n')
        print("FINISHED FOR CITY:",name)
    # Update URL tracking status in a separate file
    with open(url_tracking_file, 'w') as file:
        json.dump(url_tracking, file, indent=3)

        