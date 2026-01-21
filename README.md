## *🔍 Web 과제 🔍*
> FastAPI와 MVC 패턴을 기반으로 사용자 로그인 기능 구현 과제
---
## 👀 OVERVIEW 

 1. index.html 꾸미기
 2. user_service.py 작성
 3. user_router.py 작성

## 💻 index.html

? 어떤 요소 넣었는지 ?

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
> 크롬 부라우저 실행
> -> 리뷰 데이터 수집 - 'Older' 버튼 클릭하여 페이지 넘김
> -> 수집 데이터 csv 파일 저장
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
- review_and_merged 이미지 첨부
