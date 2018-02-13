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
  * Capella (131 flavors)
  * The Flavor Apprentice (294 flavors)
  * Mt Baker Vapor (21 flavors)
  * AtmosLab (98 flavors)
  * LiquidBarn (44 flavors)
  * LorAnn (90 flavors) (Selenium required)
  * AzureVaping (255 flavors)
  * Bickford (138 flavors)
  * CupcakeWorld (107 flavors)
  * DarkSideVapor (3 flavors)
  * FlavourFog (23 flavors)
  * Molinberry (69 flavors)
  * EllasGourmet (76 flavors)
  * FlavorWest (367 flavors)
