import scrapy


class ZameenSpider(scrapy.Spider):
    name = "zameen"

    start_urls = [
        'https://www.zameen.com/Homes/Karachi-2-1.html',
        'https://www.zameen.com/Homes/Karachi-2-2.html'
    ]

    def parse(self, response):
        prop = response.css("div._1d4d62ed")
        def func(req,ind):
            if len(req)==2:
                return req[ind]
            else:
                return "Not Specified"
        for p in prop:
            yield {
                'price': p.css('span.f343d9ce::text').get(),
                'location':p.css('div._162e6469::text').get(),
                'bed': func(p.css('span._984949e5::text').getall(),0),
                'bath':func(p.css('span._984949e5::text').getall(),1),
                'size':p.css('span._984949e5 div div div span::text').get(),
            }
        next_page = response.css("a.b7880daf::attr(href)").getall()[-1]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            # shortcut
            yield response.follow(next_page,callback=self.parse)
            