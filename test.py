from playwright.sync_api import sync_playwright

output_file = "delhiunis3.json"

city = {}

# writing the url_tracking file if not exists otherwise reading from it.
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False, slow_mo=70)
    context = browser.new_context()

    # main city urls to get all the links of the cities and append in a dictionary named city as {name of city:code of city}
    main_url = "https://www.shiksha.com/science/ranking/top-universities-colleges-in-india/121-2-0-0-0"

    data = {"course": []}

    test_url = "https://www.shiksha.com/university/jamia-millia-islamia-delhi-843"
    print("getting into college:", test_url)
    test_div_page = context.new_page()
    # college div page is the URL of all individual div universities.
    test_div_page.set_default_timeout(0)
    test_div_page.goto(test_url)

    # about(need to change)
    body_section_div = test_div_page.query_selector("#iulp_lhs_container")
    inner_section = body_section_div.query_selector(".paper-card.spacingVariation")
    about_div = inner_section.query_selector("._1003._58f5")
    about_div = about_div.query_selector(".wikiContents._021e.collapsed.ca53._5333.a78b")
    read_more = about_div.query_selector("._5ee4")
    read_more.scroll_into_view_if_needed()
    read_more.click()
    about_div = test_div_page.query_selector(".wikiContents._2d3b.ca53._5333.a78b")
    inner_about_div=about_div.query_selector(".faq__according-wrapper p")
    print(inner_about_div.inner_text())
