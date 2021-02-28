# -*- coding: utf-8 -*-
import scrapy
import string
import pandas as pd 

class FoxnewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['www.foxnews.com']
    #start_urls = ['https://www.foxnews.com/politics/biden-stresses-americans-shouldnt-go-back-to-work-until-its-safe-to-send-you-back']

    def start_requests(self):
        df = pd.read_csv("~/repo/StatMachLearn/NewsArticleClassification/data_to_group_copy.csv", header=0)
        domain_list =  list(set(df['domain'].values))
        #for domain in domain_list:
        #for domain in ["usatoday.com"]:
        #for domain in ["cnn.com"]:
        for domain in ["nbcnews.com"]:
        #for domain in ["washingtonpost.com"]:
        #for domain in ["nytimes.com"]:
        #for domain in ["abcnews.go.com"]:     
        #for domain in ["buzzfeed.com"]:     
        #for domain in ["cbsnews.com"]:     
        #for domain in ["edition.cnn.com"]: 
        #for domain in ["mmajunkie.usatoday.com"]:   
        #for domain in ["msnbc.com"]: 
        #for domain in ["wnewsj.com"]:
        #for domain in ["wsj.com"]:
            print(f"Trying for {domain}")
            df_domain = df[df["domain"]==domain]
            for index in df_domain.index:
              try:
                  url = df_domain.loc[index, "url"]
                  id_ = int(df_domain.loc[index, "id"])
                  print(f"{domain} {id_} {type(id_)}" )
                  yield scrapy.Request(url, callback=self.parse, meta={"id_": id_, "domain": domain} )
              except Exception as e:
                  print(f"Problem for {id_} {e}")
                  continue              

    def parse(self, response):
        id_ = response.meta.get("id_")
        domain = response.meta.get("domain")

        if domain == "foxnews.com":
            x_path_string = "//div[@class='article-body']/p/text()"
        elif domain == "usatoday.com":
            x_path_string = "//p[@class='gnt_ar_b_p']/text()"
        elif domain == "cnn.com":
            x_path_string = '//article[@class="sc-bwzfXH sc-kIPQKe jjVnED"][1]/div[@class="sc-bdVaJa post-content-rendered render-stellar-contentstyles__Content-sc-9v7nwy-0 erzhuK"]/p/text()'
        elif domain == "nbcnews.com":
            x_path_string = '//div[@class="LiveBlogCard article-body__content w-100 mh0 mb8 fn overflow-x-hidden card___2nUEE"][1]/p/text()'
        elif domain == "washingtonpost.com":
            x_path_string = '//div[@class="article-body"]//p[@class="font--body font-copy gray-darkest ma-0 pb-md "]/text()'
        elif domain == "nytimes.com":
            x_path_string = '//section[@name="articleBody"]//p[@class="css-axufdj evys1bk0"]/text()'
        elif domain == "abcnews.go.com":
            x_path_string = '//section[@class="Article__Content story"]/p/text()'
        elif domain == "buzzfeed.com":
            x_path_string = '//div[@class=" buzz--long"]//p/text()'
        elif domain == "cbsnews.com":
            x_path_string = '//section[@class="content__body"]/p[position() < last()]/text()'
        elif domain == "edition.cnn.com":
            x_path_string = '//article[@class="sc-bwzfXH sc-kIPQKe jjVnED"][1]/div[@class="sc-bdVaJa post-content-rendered render-stellar-contentstyles__Content-sc-9v7nwy-0 erzhuK"]/p/text()'
        elif domain == "mmajunkie.usatoday.com":
            x_path_string = '//div[@class="articleBody"]/p/text()'
        elif domain == "msnbc.com":
            x_path_string = '//div[@class="article-body__content"]/p/text()'
        elif domain == "wnewsj.com":
            x_path_string = "//div[@class='entry-content post_content']/article/p[position() <last()]/text()"
        elif domain == "wsj.com":
            x_path_string = '//div[@class="article-content  "]//p[position() < last()]/text()'
        else:
            raise ValueError("domain in specified domains")
        
        def get_xpath_string_backup(domain, ):
            if domain == "nbcnews.com":
                x_path_string = '//div[@class="article-body__section article-body__last-section"]//p/text()'
            elif domain == "cnn.com":
                x_path_string = '//div[@class="l-container"]//div[@class="zn-body__paragraph"]/text()'
            return x_path_string

        article_list = response.xpath(x_path_string).getall()
        article_text_string = " ".join(article_list)
        article_text = article_text_string.translate(str.maketrans('', '', string.punctuation))

        if article_text == "":
            x_path_string = get_xpath_string_backup(domain)
            article_list = response.xpath(x_path_string).getall()
            article_text_string = " ".join(article_list)
            article_text = article_text_string.translate(str.maketrans('', '', string.punctuation))

        yield {
          id_ : article_text
              }
    
