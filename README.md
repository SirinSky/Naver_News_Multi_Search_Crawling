# Naver_News_Multi_Search_Crawling

'sbomhoo'님의 Python을 이용한 네이버 뉴스 리스트 크롤링 프로그램에, 여러 검색어를 검색할 수 있는 멀티서치 기능과 이에 중복되는 기사를 하나로 줄여주는 기능을 넣은 멀티 서치 크롤링 프로그램입니다.

------
 사용 라이브러리  
-------------
- BeautifulSoup
- requests
- pandas
- datetime (현 시간을 이름으로 저장하기 위함)
- re  (정규표현식)


 프로그램 소개 
 -------------
- select 연산자 사용 (find x)
- 크롤링 해오는 것 : 제목(링크),신문사,날짜
- 크롤링 결과 : 리스트 -> 딕셔너리 -> df -> 엑셀로 저장 

------
 실행 
-------------
<img width="734" alt="Multi_Search_1" src="https://user-images.githubusercontent.com/26783927/167356141-9867d079-83e7-4591-96a1-41d4690a525d.PNG">
<img width="413" alt="Multi_Search_2" src="https://user-images.githubusercontent.com/26783927/167356147-714784f2-3e54-47fe-8a7b-f41afc711269.PNG">
<img width="960" alt="Multi_Search_3" src="https://user-images.githubusercontent.com/26783927/167356152-96b14a14-3e5f-4f35-bc16-20932d96a7ae.PNG">
