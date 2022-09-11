from gc import callbacks
import scrapy
from scrapy_playwright.page import PageMethod
from credentials import Credentials as c  # this module located in the venv root

# logic:
# login dulu pada pada start_request, tunggu sampai selesai loading, kemudian paste Url yang sudah berisi
# seluruh listing yang ingin dicari
# baru kemudian crawl satu persatu


class BrightspiderSpider(scrapy.Spider):
    name = "brightspider"
    allowed_domains = ["brighton.co.id"]
    login_url = (
        "https://www.brighton.co.id/visitor/login/?BackURL=https://www.brighton.co.id/"
    )

    start_urls = "https://www.brighton.co.id/cari-properti/?Keyword=&Transaction=&Type=&Certificate=&Province=Bali&Location=&Area=&KT=&KM=&PriceMin=&PriceMax=&LTMin=&LTMax=&LBMin=&LBMax=&OrderBy=5&page=1"
    second_url = "https://www.brighton.co.id/"

    def start_requests(self):
        yield scrapy.Request(
            url=self.login_url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods={
                    # "wait_for_selector": PageMethod(
                    #    "wait_for_selector",
                    #    selector="button.btn:nth-child(6)",
                    # ),
                    "fill": PageMethod(
                        "fill",
                        selector="div.input-container:nth-child(3) > div:nth-child(2) > input:nth-child(1)",
                        value=c.username,  # type your username manually here
                    ),
                    "fill": PageMethod(
                        "fill",
                        selector="div.input-container:nth-child(4) > div:nth-child(2) > input:nth-child(1)",
                        value=c.password,  # and here is your password
                    ),
                    "click": PageMethod(
                        "click",
                        selector="button.btn:nth-child(6)",
                    ),
                    "goto": PageMethod("goto", url=self.start_urls),
                    "is_visible": PageMethod(
                        "is_visible",
                        selector="#fullBody.scroll-down div.footer div.container-fluid.px-3.grid-container div.wrapper-2 img.sertification-footer.d-block.mx-auto.px-2.py-1",
                    ),
                },
            ),
            callback=self.parse,
        )
        # errback: self.errback

    async def parse(self, response):
        total_pages = int(
            response.css(
                "li.page-item.page-icon-attr.mx-1 a::attr(data-page)"
            ).getall()[1]
        )
        # page = response.meta["playwright_page_methods"]['is_visible'].result
        # title = await page.title()
        # await page.context.close()  # close the context
        # await page.close()
        # add a loop here with total_pages as the maximum iteration
        # reprocess the start_urls again where the pages adding up until reach the total_pages
        list = response.css("div.col-12.col-md-6.col-lg-4.py-2.px-0.py-sm-2.px-md-2")
        properties = list.css("h2.nama-properti::text").getall()
        # add another loop here(inside the previous loop) to yield all of the data
        yield {
            "total_pages": total_pages,
            "listing_title": properties,
        }

    async def errback(
        self, failure
    ):  # to ensure the page is closed when there is an error.
        page = failure.request.meta["playwright_page"]
        await page.close()
