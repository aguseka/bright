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

    def start_requests(self):
        yield scrapy.Request(
            url=self.login_url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods={
                    "fill": PageMethod(
                        "fill",
                        selector="html.fa-events-icons-failed body div#content_wrapper.bg-agent-login div.container div.content_wrapper div.row div.col-lg-12 form#form_login div.input-container",
                        value=c.username,  # type your username manually here
                    ),
                    "fill": PageMethod(
                        "fill",
                        selector="html.fa-events-icons-failed body div#content_wrapper.bg-agent-login div.container div.content_wrapper div.row div.col-lg-12 form#form_login div.input-container div.input-field input.custominput.inputformvisitor",
                        value=c.password,  # and here is your password
                    ),
                    "click": PageMethod(
                        "click",
                        selector="html.fa-events-icons-failed body div#content_wrapper.bg-agent-login div.container div.content_wrapper div.row div.col-lg-12 form#form_login button.btn.btn-block.btn-lg.btn-primary-custom",
                    ),
                    "goto": PageMethod("goto", url=self.start_urls),
                    "is_visible": PageMethod(
                        "is_visible",
                        selector="#fullBody.scroll-down div.footer div.container-fluid.px-3.grid-container div.wrapper-2 img.sertification-footer.d-block.mx-auto.px-2.py-1",
                    ),
                },
            ),
            # callback=self.parse,
        )
        # errback: self.errback

    async def parse(self, response):
        total_pages = response.css(
            "li.page-item.page-icon-attr.mx-1 a::attr(data-page)"
        ).getall()
        yield {"total_pages": total_pages[1]}

    async def errback(
        self, failure
    ):  # to ensure the page is closed when there is an error.
        page = failure.request.meta["playwright_page"]
        await page.close()


"""
    def start_requests(self):
        scrapy.Request(
            url=self.start_urls,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_chromium_launch=True,
                playwright_browser_headlessly=False,
                playwright_page_methods={
                    "is_visible": PageMethod(
                        "is_visible", selector=".sertification-footer"
                    ),
                },
            ),
            callback=self.parse,
        )

    async def parse(self, response):
        yield {"text": response.text}
        pass

    async def errback(
        self, failure
    ):  # to ensure the page is closed when there is an error.
        page = failure.request.meta["playwright_page"]
        await page.close()



# this one without playwright, only using scrapy.
def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass



class BrightspiderSpider(scrapy.Spider):
    name = "brightspider"
    allowed_domains = ["brighton.co.id"]
    start_urls = [
        "https://www.brighton.co.id/visitor/login/?BackURL=https://www.brighton.co.id/"
    ]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={"username": "balisunrise@gmail.com", "password": "dk3245uf"},
            callback=self.after_login,
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return
        else:
            yield {"text": response.text}
            """
