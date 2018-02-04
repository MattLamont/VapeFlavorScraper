# VapeFlavorScraper

## Start Crawler Debugging

`scrapy crawl [SpiderName]`

example: `scrapy crawl FlavourArt`

## Start Crawler and Write To Database

`scrapy crawl [SpiderName] -s USERNAME=[username] -s PASSWORD=[password] -s URL=[serverHost]`

example: `scrapy crawl FlavourArt -s USERNAME="myusername" -s PASSWORD="mypassword" -s URL="http://localhost:1337"`

## Supported Spiders

  * FlavourArt
  * NicVape
  * Capella
