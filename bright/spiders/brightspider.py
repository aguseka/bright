from gc import callbacks
import scrapy
from scrapy_playwright.page import PageMethod
from credentials import Credentials as c  # this module located in the venv root


class BrightspiderSpider(scrapy.Spider):
    name = "brightspider"
    allowed_domains = ["brighton.co.id"]
    custom_settings = {
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
    }
    login_url = (
        "https://www.brighton.co.id/visitor/login/?BackURL=https://www.brighton.co.id/"
    )

    start_urls = "https://www.brighton.co.id/cari-properti/?Keyword=&Transaction=&Type=&Certificate=&Province=Bali&Location=&Area=&KT=&KM=&PriceMin=&PriceMax=&LTMin=&LTMax=&LBMin=&LBMax=&OrderBy=5&page=1"
    x = 1

    def start_requests(self):
        yield scrapy.Request(
            url=self.login_url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod(
                        "is_visible",
                        selector="button.btn:nth-child(6)",
                    ),
                    PageMethod(
                        "fill",
                        selector="html.fa-events-icons-failed body div#content_wrapper.bg-agent-login div.container div.content_wrapper div.row div.col-lg-12 form#form_login div.input-container div.input-field input.custominput.inputformvisitor",
                        value=c.username,  # type your username manually here
                    ),
                    PageMethod(
                        "fill",
                        selector="div.input-container:nth-child(4) > div:nth-child(2) > input:nth-child(1)",
                        value=c.password,  # and here is your password
                    ),
                    PageMethod(
                        "click",
                        selector="button.btn:nth-child(6)",
                    ),
                    PageMethod(
                        "is_visible",
                        selector="html.fa-events-icons-failed body div.swal-overlay.swal-overlay--show-modal div.swal-modal div.swal-footer div.swal-button-container button.swal-button.swal-button--confirm",
                    ),
                    PageMethod(
                        "click",
                        selector="html.fa-events-icons-failed body div.swal-overlay.swal-overlay--show-modal div.swal-modal div.swal-footer div.swal-button-container button.swal-button.swal-button--confirm",
                    ),
                    PageMethod("goto", url=self.start_urls),
                ],
            ),
            callback=self.gen_urls,
        )

    # errback: self.errback
    def gen_urls(self, response):

        total_pages = int(
            response.css(
                "li.page-item.page-icon-attr.mx-1 a::attr(data-page)"
            ).getall()[1]
        )

        for self.x in range(2, 12):  # change the 6 here with total_pages
            url = f"https://www.brighton.co.id/cari-properti/?Keyword=&Transaction=&Type=&Certificate=&Province=Bali&Location=&Area=&KT=&KM=&PriceMin=&PriceMax=&LTMin=&LTMax=&LBMin=&LBMax=&OrderBy=5&page={self.x}"
            yield scrapy.Request(
                url=url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod(
                            "is_visible",
                            selector="div.containerDaftarProp",
                        ),
                    ],
                ),
                callback=self.parse,
            )

    def parse(self, response):
        list = response.css("div.col-12.col-md-6.col-lg-4.py-2.px-0.py-sm-2.px-md-2")
        not_page_1 = list.css(
            "div.card.card-properti-non-label > a.record-page-visitor::attr(href)"  # selector for pages other than page_1
        )
        for property in not_page_1:
            yield response.follow(property.get(), callback=self.detail_parse)

    def detail_parse(self, response):
        yield {"url": response.url}


"""
    async def errback(
        self, failure
    ):  # to ensure the page is closed when there is an error.
        page = failure.request.meta["playwright_page"]
        await page.close()
        
        
          total_pages = response.css(
            "li.page-item.page-icon-attr.mx-1 a::attr(data-page)"
        ).getall()
        yield {"total_pages": total_pages[1]}
"""
