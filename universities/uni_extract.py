from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import json,time
from urllib.parse import urljoin
output_file='delhiunis.json'


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=25)
    context = browser.new_context()
    page = context.new_page()
    #only delhi college selected
    uni_url='https://www.shiksha.com/science/ranking/top-universities-colleges-in-india/121-2-0-0-0?rs[]=121&uaf[]=location&rf=filters&ct[]=10223'
    page.goto('https://www.shiksha.com/science/ranking/top-universities-colleges-in-india/121-2-0-0-0?rs[]=121&uaf[]=location&rf=filters&ct[]=10223')
    div_elemets=page.query_selector('#rankingTupleWrapper')
    time.sleep(2)
    substring='rp_tuple'
    div_elements = page.query_selector_all('div[id*="{0}"]'.format(substring))

    data={"course":[]}

    #function for course data called below
    def get_colleges_from_faculty_url(course_href,faculty_name,course_data):
        context = browser.new_context()
        coursepage = context.new_page()
        coursepage.goto(course_href)
        time.sleep(1.5)
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
            if 'master' in colz_name.lower():
                degree='Masters'
            elif 'masters' in colz_name.lower():
                degree='Masters'
            elif 'm.' in colz_name.lower():
                degree='Masters'
            elif 'm.' and 'b.' in colz_name.lower():
                degree='Masters'
            elif 'b.' and 'm.' in colz_name.lower():
                degree='Masters'
            elif 'bachelor' in colz_name.lower():
                degree='Bachelors'
            elif 'bachelors' in colz_name.lower():
                degree='Bachelors'
            elif 'b.' in colz_name.lower():
                degree='Bachelors'
            elif 'pg' in colz_name.lower():
                degree='Diploma'
            elif 'p.g.' in colz_name.lower():
                degree='Diploma'
            elif 'diploma' in colz_name.lower():
                degree='Diploma'
            elif 'ph.d.' in colz_name.lower():
                degree='Doctorate'
            else:
                pass

            #duration of course 
            year = individual_div.query_selector('.inlineLabel').inner_text().strip('\xa0()') if individual_div.query_selector('.inlineLabel') else ""

            #for no of seats and total fee
            more_div=individual_div.query_selector('.contSec.acpContainer')

            # Extracting number of seats
            try:
                seats = more_div.query_selector('div:nth-child(1) > .valueTxt > div').inner_text() if more_div.query_selector('div:nth-child(1) > .valueTxt > div') else ""
            except:
                pass
            # ************************************

            # Extracting total fees(error occurred)
            fee_element = more_div.query_selector('div:nth-child(2) > .valueTxt')
            fee = fee_element.inner_text() if fee_element else ""

            course_data.append({'name': colz_name,
                                'degree':degree, 
                                'Faculty':faculty_name,
                                'Year': year,
                                'seats':seats,
                                # 'fee':fee
                                })

        coursepage.close()



    #extracting all the college urls of a state
    url_list=[]
    for div_element in  div_elements:
        href_element=div_element.query_selector('.tuple-inst-info')
        a_element = href_element.query_selector('a.rank_clg')
        url = a_element.get_attribute('href')
        full_url=urljoin(uni_url,url)
        url_list.append(full_url)


    for url in url_list:
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
        div_element = header_div.query_selector('.c55b78')
        img_element = div_element.query_selector('img')
        logo = img_element.get_attribute('src')
        data["logo"]=logo
        # print(logo)

        #address dict initialized (country_name, st_line_address, city, lati,longi)
        address={"country_name":"India"}

        #st_line_address
        address_div=header_div.query_selector('.b82d61')
        address_element=address_div.query_selector('._94eae8')
        st_line_address=address_element.inner_text()
        address["street_line_address"]=st_line_address
        # print(st_line_address)

        #city
        #for city(put the same value for the selected location)

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


        #about
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
        course_url=url+'/courses'
        coursepage = context.new_page()
        coursepage.goto(course_url)

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
            course_href=urljoin(uni_url,href)
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
            print("Error opening file(ignore this error lmao, still creates the json),",e)
            results=[]
            with open(output_file, 'w') as file:
                results.append(data)
                json.dump(results, file, indent=3)

        print('finished scrapping:',url)
        print('--------------------------------------------------------------------------------------------- \n')
        # print(data)

        coursepage.close()

    


