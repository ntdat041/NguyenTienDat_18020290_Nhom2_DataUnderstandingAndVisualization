import scrapy
import csv


class LaoDongSpider(scrapy.Spider):
    name = 'LaoDong'
    start_urls = ['https://laodong.vn/thoi-su/thu-tuong-tang-cuong-lien-ket-vung-di-dau-trong-phat-trien-kinh-te-so-825152.ldo']
    total_pages = set()
    csv_columns = ['Link', 'Title', 'Tags', 'Description', 'Keywords', 'Content']

    with open("/Users/htc/Untitled Folder/LaoDong.csv", mode="a+", encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=csv_columns)
        writer.writeheader()
    def parse(self, response):
            csv_columns = ['Link', 'Title','Tags','Description','Keywords','Content']
            dict = {
                'Link' :response.url,
                'Title':response.css('h1::text').get(),
                'Tags' :response.css('span.keywords a::text').getall(),
                'Description': response.css('p.abs::text').get(),
                'Keywords': [k.strip() for k in response.css('meta[name="keywords"]::attr("content")').get().split(',')],
                'Content': '\n'.join([''.join(c.css('*::text').getall())
                    for c in response.css('div.article-content > p')]),
                }

            with open("/Users/htc/Untitled Folder/LaoDong.csv" , mode="a+" , encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile , fieldnames = csv_columns , delimiter=',')
                writer.writerow(dict)
            next_links = response.css('article.article-small.N2 a::attr(href)').getall()
            for link in next_links:
                if len(self.total_pages) <= 200:
                    self.total_pages.add(link)
                    yield scrapy.Request(
                        response.urljoin(link),
                        callback=self.parse
                    )
# Go to /spiders and run in command
# scrapy crawl LaoDong

# Data Preprocessing with Python: https://www.analyticsindiamag.com/data-pre-processing-in-python
# Data Visualization with Python: https://towardsdatascience.com/introduction-to-data-visualization-in-python-89a54c97fbed
# https://towardsdatascience.com/the-next-level-of-data-visualization-in-python-dd6e99039d5e