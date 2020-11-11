# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime


class ScrapyTestItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

def extract_rate(text):
    # extract the rate
    text = text[0]
    return int(text)

def extract_gender(text):
    returnData = text
    if(returnData != 'not-found'):
        x = returnData.replace('<span data-qa-target=\"ProviderDisplayGender\"> <!-- -->','')
        y = x.replace('<!-- --> </span>','')
        returnData = y.strip()
    return returnData

def extract_age(text):
    returnData = text
    if(returnData != 'not-found'):
        x = returnData.replace('<span data-qa-target="ProviderDisplayAge">• Age <!-- -->','')
        y = x.replace('</span>','')
        returnData = y.strip()
    return returnData

def extract_reviewerName(text):
    returnData = text.strip()
    if(returnData != 'not-found'):
        returnData = returnData[:-1]
        print(returnData)
    return returnData.strip()

class Profile(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    ratings = scrapy.Field(input_processor=MapCompose(extract_rate), output_processor=TakeFirst())
    address = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    phone = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    profileInfo = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    profileImage = scrapy.Field(output_processor=TakeFirst())
    speciality = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    gender = scrapy.Field(input_processor=MapCompose(extract_gender), output_processor=TakeFirst())
    age = scrapy.Field(input_processor=MapCompose(extract_age), output_processor=TakeFirst())
    last_updated = scrapy.Field(serializer=str)
    reviewItem = scrapy.Field()

class Reviews(scrapy.Item):
    owner = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    reviewerName = scrapy.Field(input_processor=MapCompose(extract_reviewerName), output_processor=TakeFirst())
    reviewStar = scrapy.Field()
    reviewComment = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    reviewDate = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    last_updated = scrapy.Field(serializer=str)


def remove_quotes(text):
    # strip the unicode quotes
    text = text.strip(u'\u201c'u'\u201d')
    return text


def convert_date(text):
    # convert string March 14, 1879 to Python date
    return_date = datetime.strptime(text, '%B %d, %Y')
    return return_date


def parse_location(text):
    # parse location "in Ulm, Germany"
    # this simply remove "in ", you can further parse city, state, country, etc.
    return text[3:]


class QuoteItem(Item):
    quote_content = Field(
        input_processor=MapCompose(remove_quotes),
        # TakeFirst return the first value not the whole list
        output_processor=TakeFirst()
        )
    author_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    author_birthday = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    author_bornlocation = Field(
        input_processor=MapCompose(parse_location),
        output_processor=TakeFirst()
    )
    author_bio = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    tags = Field()