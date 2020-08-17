import scrapy
import json

### crawler 1 page in BaoMOi and save to file .txt or file json
class VietnamnetCrawler(scrapy.Spider):
    name = "Vietnamnet"
    start_urls = ['https://vietnamnet.vn/vn/thoi-su/ngu-dan-thanh-hoa-nghe-an-hoi-ha-dua-tau-thuyen-vao-bo-tranh-bao-so-2-662825.html',
                  'https://vietnamnet.vn/vn/giai-tri/la-thanh-huyen-va-quynh-kool-tiet-lo-ve-thanh-son-va-nhan-phuc-vinh-661482.html',
                  'https://vietnamnet.vn/vn/kinh-doanh/tai-chinh/lai-suat-giam-manh-co-tien-ty-ngoi-nha-gui-tiet-kiem-online-huong-loi-cao-662134.html',
                    ]
    total_pages= set()

    def parse(self, response):

        data ={
        'Link': response.url,
        'Title' : response.css('h1::text').get(),
        'Content' : '\n'.join(response.css('div.ArticleContent p::text').getall()),
        'Tags' : '\n'.join(response.css('div.tagBoxContent li a::text').getall()),
        'Category' : response.css('div.top-cate-head-title a::attr("href")').get()
        }
        f = open('C:/Users/htc/PycharmProjects/Testscarpy/tutorial/tutorial/Output/Vietnamnet.txt', 'a+', encoding='utf-8')
        f.write(json.dumps(data, ensure_ascii=False))
        f.write('\n')
        next_links = response.css('div.clearfix.item a.w-240.thumb.left.m-r-20.m-t-5::attr(href)').getall()


        for link in next_links:
                if len(self.total_pages) <= 200:
                    self.total_pages.add(link)
                    yield scrapy.Request(
                    response.urljoin(link),
                    callback=self.parse
                    )



# Go to /spiders and run in command
# scrapy crawl Vietnamnet
