# this code is not using scrapy. Only using playwright
from os import sync
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto(
        "https://www.brighton.co.id/visitor/login/?BackURL=https://www.brighton.co.id/"
    )
    page.fill(
        "div.input-container:nth-child(3) > div:nth-child(2) > input:nth-child(1)",
        "balisunrise@gmail.com",
    )
    page.fill(
        "div.input-container:nth-child(4) > div:nth-child(2) > input:nth-child(1)",
        "dk3245uf",
    )
    page.click("button.btn:nth-child(6)")
    page.goto(
        "https://www.brighton.co.id/cari-properti/?Keyword=&Transaction=&Type=&Certificate=&Province=Bali&Location=&Area=&KT=&KM=&PriceMin=&PriceMax=&LTMin=&LTMax=&LBMin=&LBMax=&OrderBy=5&page=1"
    )
    html = page.inner_html("#containerDaftarProp")
    print(html)
