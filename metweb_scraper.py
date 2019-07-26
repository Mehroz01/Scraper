import scrapy
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
import re
import pandas as pd
import os
import time
import flask
import unicodedata

from flask import request, jsonify


class met_web(scrapy.Spider):
    name="metweb"

    weather={}
    def start_requests(self):

        #start_url=['http://www.matweb.com/search/QuickText.aspx?SearchText=AA7075']
        start_url=['http://www.matweb.com/search/QuickText.aspx?SearchText=AA2618']
        #start_url = ['http://www.matweb.com/search/QuickText.aspx?SearchText=AA5083']
        #start_url = ['http://www.matweb.com/search/QuickText.aspx?SearchText=AA7150']
        #start_url =['http://www.matweb.com/search/QuickText.aspx?SearchText=AA1235']
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)




    #'//div[@id='details']/div/div[@class='day muted']/div/div/h4'

    def parse(self, response):
        #start_url=['https://www.accuweather.com/en/pk/lahore/260622/daily-weather-forecast/260622?day=1']
        print('parse is checking')

        # material_name=response.xpath("//table[@id='tblResults']/tr/th[3]/a/text()").extract_first()
        # print('\n materials names :',material_name)
        #

        #####################Extract Composition######################################
        for resp in response.xpath("//table[@id='tblResults']/tr"):#//div[@id='feed-tabs']#//div[@id='details']/div/div[@class='day muted']
            #print(quote)


            composition_link=resp.xpath("td[3]/a/@href").extract_first()
            #print('\n composition  Row ',composition)


            if composition_link:

                composition_url='http://www.matweb.com'+composition_link
                print('\n URL is ',composition_url)
                start_url = [composition_url]

                for url in start_url:
                    yield scrapy.Request(url=url, callback=self.parse_2)

            else:
                print('empty cell', composition_link)
        #####################Extract Composition######################################



        # composition_link=response.xpath("//table[@id='tblResults']/tr/td[3]/a/@href").extract_first()
        # print('\n materials link :',composition_link)
        # composition_url='http://www.matweb.com'+composition_link
        # print(composition_url)
        # start_url = [composition_url]
        #
        # for url in start_url:
        #     yield scrapy.Request(url=url, callback=self.parse_2)

    def parse_2(self,response):
        print('#######Link 2 ########')
        url=response.request.url




        title=response.xpath("//table[@class='tabledataformat t_ableborder tableloose altrow']/tr/th/text()").extract_first()


        print('\n title is ',title)
        folder_path = os.getcwd()
        folder_path=folder_path+'/'+title
        os.mkdir(folder_path)
        folder_path=folder_path+'/'
        detail = {'URL': [url], 'Title': [title]}
        detail_file =pd.DataFrame(data=detail)
        detail_file.to_csv((folder_path+"Title_URL"),sep=',', encoding='utf-8',index=False)
        ####################Physical property header_end ########################################################
        d = {'col1': ['URL'], 'col2': [url], 'col3': ['Title'], 'col4': [title]}

        df = pd.DataFrame(data=d)
        save_table=False
        table_title=''
        table_title_reminder=True
        for resp in response.xpath("//table[@class='tabledataformat']/tr"):#//div[@id='feed-tabs']#//div[@id='details']/div/div[@class='day muted']
            header_ck=resp.xpath("th/text()").extract_first()


            if header_ck:

                print('header_contain : ',header_ck)
                if table_title_reminder==True:
                    table_title=header_ck
                    table_title_reminder=False


                if save_table== True:
                    time_stamp = time.time()
                    print('\n test property ',physical_property)
                    #file_name =folder_path+title+"_"+str(time_stamp)+".csv"
                    file_name = folder_path + table_title + ".csv"
                    print('\n file is saving',file_name)
                    print('\m data frame is ',df)
                    df.drop(df.index[0],inplace=True)
                    df.to_csv(file_name, sep=',',header=False,index=False)
                    df.drop(df.index, inplace=True)
                    d = {'col1': ['URL'], 'col2': [url], 'col3': ['Title'], 'col4': [title]}
                    table_title = header_ck

                    df = pd.DataFrame(data=d)

                physical_property=resp.xpath("th[1]/text()").extract_first()
                metrix = resp.xpath("th[2]/text()").extract_first()
                english = resp.xpath("th[3]/text()").extract_first()
                comments = resp.xpath("th[4]/text()").extract_first()
                if (metrix!='None' and english!='None'):
                    print('\n matrix_none_calling')
                    #print('\n physical property is ',physical_property,metrix,english,comments)
                    d = {'col1': physical_property, 'col2': metrix, 'col3': english, 'col4': comments}

                    df=df.append(d,ignore_index=True)

                save_table=True


            else:
                physical_property = unicodedata.normalize('NFKD', str(resp.xpath("td[1]/text()").extract_first())).encode('ascii', 'ignore').decode('utf8')

                #physical_property=
                #print('\n check002 : ',physical_property)
                physical_property_part = unicodedata.normalize('NFKD', str(resp.xpath("td[1]/a/text()").extract_first())).encode('ascii', 'ignore').decode('utf8')

                #physical_property_part=resp.xpath("td[1]/a/text()").extract_first()
                if physical_property_part!='None' :
                    if physical_property!='None' :
                        physical_property=physical_property_part+physical_property
                    else:
                        physical_property = physical_property_part




                metrix = unicodedata.normalize('NFKD', str(resp.xpath("td[2]/text()").extract_first())).encode('ascii', 'ignore').decode('utf8')
                metrix_part = unicodedata.normalize('NFKD', str(resp.xpath("td[2]/a/text()").extract_first())).encode('ascii', 'ignore').decode('utf8')

                #metrix = resp.xpath("td[2]/text()").extract_first()
                #metrix_part=resp.xpath("td[2]/a/text()").extract_first()
                if metrix_part!='None' :
                    if metrix!='None' :
                        metrix=metrix_part+metrix
                    else:
                        metrix = metrix_part


                english = unicodedata.normalize('NFKD', str(resp.xpath("td[3]/text()").extract_first())).encode('ascii', 'ignore').decode('utf8')
                english_part = unicodedata.normalize('NFKD', str(resp.xpath("td[3]/a/text()").extract_first())).encode('ascii', 'ignore').decode('utf8')

                #english = resp.xpath("td[3]/text()").extract_first()
                #english_part=resp.xpath("td[3]/a/text()").extract_first()
                if english_part :
                    if english!='None' :
                        english=english_part+english
                    else:
                        english = english_part



                comments = unicodedata.normalize('NFKD', str(resp.xpath("td[4]/text()").extract_first())).encode('ascii', 'ignore').decode('utf8')

                #comments = resp.xpath("td[4]/text()").extract_first()


                #print('\n physical property is ',physical_property,metrix,english,comments)
                if (metrix!='None' and english!='None'):
                    d = {'col1': physical_property, 'col2': metrix, 'col3': english, 'col4': comments}

                    df=df.append(d,ignore_index=True)



        print('\n ############### Dataframe is######################')
        file_name=title+".csv"
        print(df)
        file_name = folder_path+table_title+".csv"
        df.drop(df.index[0],inplace=True)
        df.to_csv(file_name, sep=',', header=False,index=False)


