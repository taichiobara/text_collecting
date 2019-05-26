from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
from urllib.error import HTTPError,URLError
import unicodedata
import string
import pandas as pd
import copy


class Nikkei:
    info_lists_agent=[]
    info_lists_company=[]
    def __init__(self,top_url):
        #top_url='https://career.nikkei.co.jp/kyujin/sl_it-network/pg'
        url_list=[]
        for i in range(1,86):
            url = top_url + str(i)
            try:
                html=urlopen(url)
            except urllib.error.HTTPError as e:
                print(e.code)
                sleep(6)
            soup = BeautifulSoup(html, 'lxml')
            links2 = []
            for a in soup.find_all('a',class_='btnType04 w190'):
                links=a.get('href')
                links2.append(links)
            for i in links2:
                if (i is not None):
                    link='https://career.nikkei.co.jp/'+i
                    url_list.append(link)
        url_list = list(set(url_list))    
        url_list1 = copy.deepcopy(url_list)
        list1=[]
        url_list2 = []#jobdetailに変えたものを入れる
        for i in url_list1:
            if "jobdetail" in i:
                url_list2.append(i)
            else:
                try:
                    html=urlopen(i)
                except urllib.error.HTTPError as e:
                    print(e.code)
                    sleep(6)                    
                bsobj=BeautifulSoup(html,"lxml")
                items = bsobj.find_all('a',class_='tabType01In', text=re.compile("求人"))
                for i in items:
                    url_list2.append('https://career.nikkei.co.jp/'+i.get('href'))

        url_list3 = copy.deepcopy(url_list2)#url_list2のコピー
        url_list4=[]
        url_list5=[]
        for url3 in url_list3:
            if 'https://career.nikkei.co.jp//agent' in url3:
                url_list4.append(url3)
            else:
                url_list5.append(url3)
        print('urlリストが完成したよ！！！！！！！')


        #リスト(info_lists)の中にリスト(info_list)を入れていく。
        #info_lists_agent=[]
        #for url in url_list4:
        for url in url_list4:
            html=urlopen(url)
            bsobj=BeautifulSoup(html,"lxml")
            #会社名,仕事内容,給与詳細,勤務地、勤務時間,お問い合わせ
            info_list_agent={'company_name':'','work_content':'','salary':'','work_location':'','work_time':'','contact':'','recruit_type':'agent'}
            #company_name=bsobj.find('h2',class_=re.compile('titTxt.*')).text
            #info_list['会社名']=company_name
            #info_list_agent['recruit_type']='agent'
            items1 = bsobj.find_all('tr')
            for item in items1:
                th=str(item.find('th'))
                td=item.find('td')
                if '求人会社名' in th or '企業名' in th or '会社名' in th:
                    info_list_agent['company_name']=td.text
                elif '仕事内容' in th or '勤務内容' in th:
                    info_list_agent['work_content']=td.text
                elif '給与詳細' in th or '給与' in th or '給料' in th:
                    info_list_agent['salary']=td.text
                elif '勤務地' in th or '勤務場所' in th or '場所' in th:
                    info_list_agent['work_location']=td.text
                elif '勤務時間' in th:
                    info_list_agent['work_time']=td.text
                elif 'お問い合わせ'in th or 'お問いあわせ' in th:
                    info_list_agent['contact']=td.text
        

            self.info_lists_agent.append(info_list_agent)

        #リスト(info_lists)の中にリスト(info_list)を入れていく。
        #info_lists_company=[]
        #for url in url_list5:
        for url in url_list5[:2]:
            try:
                html=urlopen(url)
            except urllib.error.HTTPError as e:
                print(e.code)
                sleep(6)

            bsobj=BeautifulSoup(html,"lxml")
            #会社名,仕事内容,給与詳細,勤務地、勤務時間,お問い合わせ
            info_list_company={'company_name':'','work_content':'','salary':'','work_location':'','work_time':'','contact':'','recruit_type':'company'}
            #company_name=bsobj.find('h2',class_=re.compile('titTxt.*')).text
            #info_list['会社名']=company_name
            #info_list_company['recruit_type']='company'
            items1 = bsobj.find_all('tr')
            for item in items1:
                th=str(item.find('th'))
                td=item.find('td')
                if '求人会社名' in th or '企業名' in th or '会社名' in th:
                    info_list_company['company_name']=td.text
                elif '仕事内容' in th or '勤務内容' in th:
                    info_list_company['work_content']=td.text
                elif '給与詳細' in th or '給与' in th or '給料' in th:
                    info_list_company['salary']=td.text
                elif '勤務地' in th or '勤務場所' in th or '場所' in th:
                    info_list_company['work_location']=td.text
                elif '勤務時間' in th:
                    info_list_company['work_time']=td.text
                elif 'お問い合わせ'in th or 'お問いあわせ' in th:
                    info_list_company['contact']=td.text

            self.info_lists_company.append(info_list_company)

if __name__ == '__main__':
    top_url1='https://career.nikkei.co.jp/kyujin/sl_it-network/pg'
    nikkei=Nikkei(top_url1)
    import os
    #import sys
    #sys.path.append('../')
    import model
    #print(nikkei.info_lists_agent)
    #model.bulk_insert(nikkei.info_lists_company)
    model.bulk_insert(nikkei.info_lists_agent)