# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import re
import openpyxl


#각 크롤링 결과 저장하기 위한 리스트 선언 
title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]


#엑셀로 저장하기 위한 변수
now = datetime.now() #파일이름 현 시간으로 저장하기


#날짜 정제화 함수
def date_cleansing(test):
    try:
        #지난 뉴스
        #머니투데이  10면1단  2018.11.05.  네이버뉴스   보내기  
        pattern = '\d+.(\d+).(\d+).'  #정규표현식 
    
        r = re.compile(pattern)
        match = r.search(test).group(0)  # 2018.11.05.
        date_text.append(match)
        
    except AttributeError:
        #최근 뉴스
        #이데일리  1시간 전  네이버뉴스   보내기  
        pattern = '\w* (\d\w*)'     #정규표현식 
        
        r = re.compile(pattern)
        match = r.search(test).group(1)
        #print(match)
        date_text.append(match)

def crawler(maxpage,query,sort,s_date,e_date):

    s_from = s_date.replace(".","")
    e_to = e_date.replace(".","")
    page = 1  
    maxpage_t =(int(maxpage)-1)*10+1   # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지
    
    
    #네이버 기사
    while page <= maxpage_t:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
        
        response = requests.get(url)
        html = response.text
 
        #뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')
 
        #<a>태그에서 제목과 링크주소 추출
        atags = soup.select('.news_tit')
        for atag in atags:
            title_text.append(atag.text)     #제목
            link_text.append(atag['href'])   #링크주소
            
        #신문사 추출
        source_lists = soup.select('.info_group > .press')
        for source_list in source_lists:
            source_text.append(source_list.text)    #신문사
        
        #날짜 추출 
        date_lists = soup.select('.info_group > span.info')
        for date_list in date_lists:
            # 1면 3단 같은 위치 제거
            if date_list.text.find("면") == -1:
                date_text.append(date_list.text)
        

        #모든 리스트 딕셔너리형태로 저장
        dictionary = {"날짜" : date_text , "제목":title_text , "매체" : source_text,"링크":link_text }  
        print(page)
        
        page += 10

    return dictionary
    
    
def crawlerResult(dic):

    df = pd.DataFrame(dic)  #df로 변환
    
    # 새로 만들 파일이름 지정
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 뉴스 결과.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(outputFileName,sheet_name='sheet1')
        
    #엑셀의 링크 하이퍼링크 화
    wb = openpyxl.load_workbook(outputFileName)
    sheet = wb['sheet1']
        
    index = 1
        
    for cell in sheet["C"]:
        if(index > 1):
            cell.style = "Hyperlink"
            cell.hyperlink = sheet["E" + str(index)].value
        index+= 1
        
    for cell in sheet["E"]:
        cell.value = ""
            
    wb.save(outputFileName)
    wb.close()

    
def main():
    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
   
    query_list = list()
    
    queryLen = int(input("검색할 키워드 수를 입력하시오: "))

    for i in range(0, queryLen):
        query_list.append(input(str(i + 1) + "번 검색어 입력: "))

    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")
    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")    #관련도순=0  최신순=1  오래된순=2
    s_date = input("시작날짜 입력(2019.01.04):")  #2019.01.04
    e_date = input("끝날짜 입력(2019.01.05):")   #2019.01.05
    
    result = {}
    result_temp = {}
    
    result_date = result_title = result_company = result_link = []
    result_temp_date = result_temp_title = result_temp_company = result_temp_link = []
    
    result = crawler(maxpage,query_list[0],sort,s_date,e_date)
    result_date = list(result["날짜"])
    result_title = list(result["제목"])
    result_company = list(result["매체"])
    result_link = list(result["링크"])
    
    
    for i in range(1, queryLen):
        result_temp = crawler(maxpage,query_list[i],sort,s_date,e_date)
            
        result_temp_date = list(result_temp["날짜"])
        result_temp_title = list(result_temp["제목"])
        result_temp_company = list(result_temp["매체"])
        result_temp_link = list(result_temp["링크"])
        
        if(len(result_temp_link) <= 0):
            continue
        
        for j in range(0, len(result_date)):
            
                index = len(result_temp_link) - 1
            
                for k in range(0, len(result_temp["링크"])):
                    
                    if(index < 0):
                        break
                    
                    if(result_link[j] == result_temp_link[index]):
                        
                        del result_temp_date[index]
                        del result_temp_title[index]
                        del result_temp_company[index]
                        del result_temp_link[index]
                        
                    index -= 1
                        
            
        #결과 딕셔너리 합체
        result_date.extend(result_temp_date)
        result_title.extend(result_temp_title)
        result_company.extend(result_temp_company)
        result_link.extend(result_temp_link)
            
            
    
    result["날짜"] = result_date
    result["제목"] = result_title
    result["매체"] = result_company
    result["링크"] = result_link
    
    if(len(result["링크"]) <= 0):
       input("검색된 결과 없음!" + "\n" +"Enter 입력시 종료")
       return
       
    crawlerResult(result)
        
    input("작업 완료! - 결과값은 크롤러가 있는 폴더 안에 생성됩니다." + "\n" +"Enter 입력시 종료")
    return

main()

