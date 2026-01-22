## *🔍 Web 과제 🔍*
> FastAPI와 MVC 패턴을 기반으로 사용자 로그인 기능 구현 과제
---
## 👀 OVERVIEW 

 1. index.html 꾸미기
 2. user_service.py 작성
 3. user_router.py 작성

## 💻 index.html

- 로그인 페이지의 사이트 화면을 깔끔한 파스텔 톤 파란색으로
- 사이트 가독성을 향상시키기 위해 배경과 어울리는 폰트를 지정
- 각 버튼의 역할에 맞는 색 지정 (Update는 파란색, Delete는 빨간색)
- 모든 요소들 가운데 정렬

## 💻 user_service.py

- 이메일을 찾지 못할 경우의 오류
- 비밀번호가 틀릴 경우의 오류
- 이메일이 존재할 경우의 오류

       #이메일이 존재할 경우 사용자 객체 정의
       exist_user = self.repo.get_user_by_email(new_user.email)
        
       if exist_user != None:
          raise ValueError("User already Exists.")

## 💻 user_router.py

- user의 register, delete, update password 기능을 구현
- 성공/에러 응답 반환

## *📑크롤링 과제📑*
> 크롤러를 통한 다양한 사이트의 리뷰 수집
---
## 👀 OVERVIEW 
주토피아1 리뷰 크롤링
## 🎬 RottenTomatoesCrawler
- 크롤링 링크: https://www.rottentomatoes.com/m/zootopia/reviews/all-audience
- 데이터 형식: rating(별 5개 기준, 1/2 가능), date, comment를 csv파일로 저장
- 데이터 개수: 1000개
> 크롬 브라우저 실행
> -> 날짜 문자열 파싱
> -> 리뷰 데이터 수집 - 'Load More' 버튼 클릭하여 페이지 넘김
> -> 수집 데이터 csv 파일 저장
## 🎬 LetterboxdCrawler
- 크롤링 링크: https://letterboxd.com/film/zootopia/reviews/
- 데이터 형식: rating(별 5개 기준, 1/2 가능), rating_raw, date, content를 csv파일로 저장
- 데이터 개수: 1000개
> 크롬 브라우저 실행
> -> 리뷰 데이터 수집 - 'Older' 버튼 클릭하여 페이지 넘김
> -> 수집 데이터 csv 파일 저장

> *타 사이트에 비해 리뷰 수가 현저히 많아서 newest 버전과 oldest 버전을 추출*
## 🎬 IMDbCrawler
- 크롤링 링크: https://www.imdb.com/title/tt2948356/reviews/
- 데이터 형식: rating(10점 기준), date, content를 csv파일로 저장
- 데이터 개수: 1000개
> 크롬 브라우저 실행
> -> 타겟 스크랩 개수 설정
> -> 리뷰 데이터 수집 - 'Load More' 버튼 클릭하여 페이지 넘김
> -> 수집 데이터 csv 파일 저장

## 📋EDA/FE📋
> 크롤링한 데이터 기반으로 사이트 간 비교분석 수행
---
## 📊 EDA
1. Rating Distribution
- Rotten Tomatoes

  <img width="690" height="290" alt="image" src="https://github.com/user-attachments/assets/3aa150ae-0e9e-46fc-a850-f8fb2c43086f" />
- IMDb

  <img width="690" height="290" alt="image" src="https://github.com/user-attachments/assets/d7202e3c-eabc-4291-bb87-63ade799eb8c" />
- Letterboxd

  <img width="690" height="290" alt="image" src="https://github.com/user-attachments/assets/847b5708-2126-47c6-9371-cd5231daa9c5" />
> 세 사이트의 별점 분포에 대한 그래프이다. IMDb는 10점 기준, Rotten Tomatoes와 Letterboxd는 5점 기준이며 1/2점이 존재한다. 10점 만점 기준 8점부터 급격히 비율이 상승하는 유사한 양상을 보인다.
2. Montly Count
- Rotten Tomatoes

  <img width="2990" height="990" alt="image" src="https://github.com/user-attachments/assets/5fbf3155-ed08-4f29-8d41-80b3ad6827fd" />
- IMDb

  <img width="2990" height="990" alt="image" src="https://github.com/user-attachments/assets/6c221f9d-ba6f-47dc-b9b1-588149dd9681" />
- Letterboxd

  <img width="2990" height="989" alt="image" src="https://github.com/user-attachments/assets/16ce0cd8-74bd-467d-a0ed-324de11c6838" />
> 세 사이트의 월별 리뷰수에 대한 그래프이다. ? 세 사이트 크롤링 날짜 기준 ?
3. Text length distribution
- Rotten Tomatoes

  <img width="690" height="290" alt="image" src="https://github.com/user-attachments/assets/0576e996-c958-44ae-9506-f6af28b5fb9d" />
- IMDb

  <img width="689" height="290" alt="image" src="https://github.com/user-attachments/assets/e3784495-c853-45c7-8a61-5536a5f4ee4b" />
- Letterboxd

  <img width="688" height="290" alt="image" src="https://github.com/user-attachments/assets/09afaffb-8668-46e8-83c5-c0b5d739373a" />
> 세 사이트의 리뷰 길이에 대한 그래프이다. 대체로 짧은 길이의 리뷰가 많은 비중을 차지하며, Letterboxd의 경우가 비교적 짧은 리뷰들이 주를 이룬다는 것을 알 수 있다.
## 📊 전처리/FE 결과 설명
1. 전처리
- 수집된 영화 리뷰 데이터는 사이트별로 형식과 품질이 달라, 분석에 앞서 공통 기준에 맞게 전처리를 수행

- 리뷰 내용이 비어 있거나 평점·날짜 정보가 누락된 데이터 제거
의미 있는 텍스트 분석을 위해 리뷰 단어 수가 지나치게 짧은 데이터 제외

- 리뷰 텍스트 소문자 변환, 특수문자 제거, 불용어 제거, lemmatization
=> 단어 형태를 통일

- langdetect를 활용하여 영어가 아닌 리뷰는 제거하여 언어 차이로 인한 분석 왜곡 방지

- 추가적으로 letterboxd의 경우 리뷰 수가 너무 많아서 oldest, newest 기준으로 1000개씩 추출 후 두 데이터 랜덤 추출해서 토탈 1000개 데이터 추출

2. F/E
- 분석 목적에 맞는 파생 변수 생성

- 리뷰 작성 시점의 월 단위 분석을 위해 date 컬럼을 기반으로 year_month 변수 생성
  => 시간 흐름에 따른 리뷰 특성 변화 분석

- 정제된 리뷰 텍스트의 단어 수를 나타내는 clean_word_count 변수 생성
=> 사이트별 리뷰 길이 차이 및 리뷰 스타일 비교 가능
## 📊 사이트 간 비교분석 결과

## *👥 GitHub 협업 과제 👥*
> Git 협업 규칙 설정하기
---
## 🪪 팀 소개
5조 안재후, 이근하, 변민주(조장)
- 안재후: 컴퓨터공학과 21
- 이근하: 도시공학과 22 
- 변민주: 인공지능학과 24

## 🪪 Git 설정
- branch_protection

  <img width="997" height="166" alt="image" src="https://github.com/user-attachments/assets/251c0cc7-be39-485e-8494-6f5275b0befc" />
- push_rejected

  <img width="868" height="351" alt="image" src="https://github.com/user-attachments/assets/f1318fe3-0fcf-4463-a3cd-a60223dcfca5" />
- review_and_merged
  
  <img width="569" height="709" alt="스크린샷 2026-01-22 134601" src="https://github.com/user-attachments/assets/e1c5a021-aee5-4312-a9b3-d8d403f619e5" />
