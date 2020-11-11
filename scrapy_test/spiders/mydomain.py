import scrapy
from selenium import webdriver
from scrapy_test.items import Profile, Reviews
from scrapy.loader import ItemLoader


class MydomainSpider(scrapy.Spider):
    name = 'mydomain'
    allowed_domains = ['healthgrades.com']
    url_name = 'https://www.healthgrades.com/physician/dr-john-panuto-22cg8'
    start_urls = [url_name]

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def parse(self, response):

        page_info = response.css('div.body-content')
        print("*******************************************************")

        for rawdata in page_info:
            #profile data scrap
            loader = ItemLoader(item=Profile())
            loader.add_value('name', rawdata.css('div.summary-column h1::text').get(default='not-found'))
            loader.add_value('ratings', rawdata.css('button.star-reviews-count::text').get(default='not-found'))
            loader.add_value('profileImage', rawdata.css('img.summary-provider-image::attr(src)').get(default='not-found'))
            loader.add_value('speciality', rawdata.css('div.summary-column span[data-qa-target="ProviderDisplaySpeciality"]::text').get(default='not-found'))
            loader.add_value('gender', rawdata.css('div.summary-column span[data-qa-target="ProviderDisplayGender"]').get(default='not-found'))
            loader.add_value('age', rawdata.css('div.summary-column span[data-qa-target="ProviderDisplayAge"]').get(default='not-found'))
            #profile_data =''
            #for ui in (rawdata.css('div.summary-column h1+div span::text').getall()):
                #profile_data = (profile_data + ui) if ui else profile_data
            loader.add_value('profileInfo', rawdata.css('div.about-me-details span::text').get(default='not-found'))
            address1 = rawdata.xpath('//div[@aria-label="officeAddress"]/p[@class="location-practice"]/text()').get(default='not-found')
            address_list = rawdata.xpath('//div[@aria-label="officeAddress"]/address/text()').extract()
            address2 = ' '.join(map(str, address_list))
            address = address1 + ',' + address2
            loader.add_value('address', address)
            seleniumBasedData = self.getSeliniumBasedData(self.url_name)
            phone = seleniumBasedData.get('phone', '0')
            loader.add_value('phone', phone)

            #review data items
            reviewList = []
            for ui in (page_info.css('div.c-single-comment')):
                r_loader = ItemLoader(item=Reviews())
                r_loader.add_value('owner', rawdata.css('div.summary-column h1::text').get(default='not-found'))
                r_loader.add_value('reviewStar', ui.css('div.l-single-comment-container div.l-top-row div.c-single-comment__stars span.eXyw8').getall())
                reviewer_name = ui.css('div.l-single-comment-container div.c-single-comment__commenter-info span:nth-child(1)::text').get(default='not-found')
                r_loader.add_value('reviewerName', reviewer_name)
                review_date = ui.css('div.l-single-comment-container div.c-single-comment__commenter-info span:nth-child(2)::text').get(default='not-found')
                r_loader.add_value('reviewDate', review_date)
                review_comment = ui.css('div.l-single-comment-container div.c-single-comment__comment::text').get(default='not-found')
                r_loader.add_value('reviewComment', review_comment)
                reviewList.append(r_loader.load_item())
            loader.add_value('reviewItem', reviewList)
        yield loader.load_item()

    def getSeliniumBasedData(self, url):
        self.driver.get(url)
        return_data = {}

        while True:
            try:
                print("before clic -------------------------------------")
                next = self.driver.find_element_by_css_selector('div.summary-standard-button-row a[data-hgoname="displayed-summary-phone-number"]')
                next.click()
                print("after clic -------------------------------------")
                return_data['phone'] = self.driver.find_element_by_css_selector('div.summary-standard-button-row a').text
                next = self.driver.find_element_by_css_selector('div.about-me-details a.about-me-bio-read-more')
                next.click()
                return_data['reviewComment'] = self.driver.find_element_by_css_selector('div.l-single-comment-container div.c-single-comment__comment::text').text
            except:
                break

        self.driver.close()
        return return_data
