# [ 8 회차 ] DB, Docker, AWS 과제

##### 발제자: 이하람

## 기간

##### 마감: 2월 5 일 23 시 59 분

##### 지각 제출: 2월 6 일 23 시 59 분

## intro

##### 이번 과제는 모두 팀플이니 팀원끼리 역할을 잘 분배해보세요!

##### 생각보다 설정에 시간이 오래걸릴 수 있으니 빠르게 시작하시는 걸 추천드립니다.

##### 이번 과제의 개요는 다음과 같습니다.

먼저, MySQL과 MongoDB를 활용해서 DB환경을 구축한 뒤, Docker 이미지를 생성합니
다. 이후, docker hub에 이미지를 업로드하고, AWS EC 2 에서 컨테이너를 실행합니다.
마지막으로 Github Action을 통해 CI/CD를 자동화까지 해봅시다!

물론 앞으로 와빅 프로젝트를 하면서 굳이 DB를 두개를 사용하거나, CI/CD를 자동화 하는
일은 거의 없을 것입니다. 그러나, 더 완성도 있는 프로젝트를 구성하기 위한 방법론들을 숙
지하고 있으면 좋을 것 같습니다

## 명세

과제를 시작하기 전, 가장 상위 디렉토리에 .env파일을 생성합시다. 또한 제공된 파일들을
아래 **제출방법** 레포 구조에 맞게 넣어주세요.

#### 1. DB

```
유저 정보를 MySQL에 저장하기
```
제공된 (^) mysql_connection.py 파일을 사용하여 사용자 정보를 MySQL에서 CRUD
하도록 (^) user_repository.py 의 함수들를 수정하세요.
이때, dependencies.py 파일을 잘 수정해서 활용해보세요! 여기에서 언급된 파일만
수정하세요.
test/test_user_repository.py 를 통과하세요!


```
MongoDB로 데이터 전처리 자동화
먼저, 크롤링한 데이터를 mongodb에 넣어주세요. 로컬에서는
mongodbcompass에서 가능합니다.
제공된 mongodb_connection.py 파일을 사용하여 preprocess API를 만들어서 데
이터 전처리를 자동화 하세요. API endpoint는 다음과 같습니다.
Method: POST /review/preprocess/{site_name}
{site_name}의 크롤링 데이터를 MongoDB에서 조회하여 앞선 과제에서 구
현한 전처리 클래스를 활용하여 전처리한 뒤 MongoDB에 저장하는 API입니
다.
응답은 자유롭게 설정하세요. 전처리클래스도 mongodb에 맞게 수정하세요!
```
**이때** , MySQL table **이름은 users로 만들어주세요**. **나머지는 상관없으니** , **팀별로 정해보세
요**!

#### 2. Docker

```
프로젝트에 대한 Dockerfile 을 작성하고, 이미지를 생성하여 docker hub에 push해
주세요. 이때, 제가 확인할 수 있도록 public으로 올려주세요!
이때, .env 같은 파일은 올리면 여러분들의 개인정보가 유출될 수 있으니, 반드시
dockerignore^ 파일을^ 생성하여^ 올리지^ 않도록^ 설정하세요!
```
#### 3. AWS

(aws 담당자는 pem 키를 팀원끼리 공유하여 팀원 모두가 인스턴스에 접속할 수 있도록 하
세요! )

```
AWS EC 2 로 인스턴스 생성 후 배포
인스턴스를 생성하여 docker hub에 올렸던 이미지를 pull받아 컨테이너를 생성
하세요.
클라우드 환경에서 디비를 호스팅
MySQL은 RDS로, MongoDB는 atlas를 사용하세요. 이때, 데이터 개수는 적게
하셔도 됩니다! 그냥 디비를 연결할 수 있다는 것만 인증하실 수 있으면 돼요.
디비 연결까지 완료된다면, swagger에서 다음과 같이 모든 API 실행 결과 ( 총 5 개 ) 를
캡쳐 하세요. 이때 반드시 ip 주소 와 endpoint, 성공 응답 이 보여야합니다. 예시 이미지
```
를 참고해주세요. 파일 이름은 (^) {api endpoint의 가장 마지막 부분}.png 로 해주시면 됩니
다. (/review/preprocess/{site_name} → preprocess.png)
register.png


#### 4. Github Action

```
위의 과정처럼 프로젝트 파일에 변경사항이 존재할 때마다 docker push를 통해 이미
지를 생성하고, ec 2 인스턴스에서 docker pull하여 컨테이너를 생성한 뒤, 서버에 반영
하는 과정을 수작업으로 수행하는 것은 비효율적입니다. 그러므로 이 과정을 github
action을 통해 자동화해봅시다.
먼저 .github/workflows/deploy.yaml 을 생성하세요. 이후, 두개의 job을 생성하세요. 첫
번째 job이름은 Build and Push Docker Image이고, 두번째 job이름은 Deploy to
EC 2 로 만들어주세요.말 그대로 첫번째 job에서는 docker 이미지를 빌드한 뒤
docker hub에 이미지를 푸시합니다. 두번째 job에서는 ec 2 에 접속하여 docker hub
로부터 이미지를 pull한 뒤 컨테이너를 생성하고, 실행하면 됩니다.
이때, 유출되면 큰일나는 정보들(docker id, password, ec 2 ip주소 등등..)은 당연히
그대로 작성하면 안되겠죠? github에서 settings> secrets and variables >
actions에서 repository secret들을 변수당 한개씩 생성하세요!
완료된 화면을 캡쳐해주세요! 반드시 status와 job이름들이 나타나야합니다.
```
github_action.png


#### 주의사항

**반드시** ec 2 **인스턴스는 종료** , RDS **에서 만든** DB **는 삭제하세요**! **과금을 청구하게 될 수도 있
습니다** ...

### 제출 방법

Docker hub 주소, aws 과제 수행시 사진 → README.md에 첨부해주세요.

이때, 사진들은 모두 aws 폴더 안에 넣어주세요.

변경 및 추가할 파일들은 주석을 달아놨으니 참고하세요!

```
YBIGTA_newbie_team_project
├── .github # 추가
│ └── workflows
│ └── deploy.yaml
├── .gitignore
├── Dockerfile # 추가
├── app
│ ├── __init__.py
│ ├── dependencies.py # 변경
│ ├── main.py # 변경
│ ├── responses
│ │ ├── __init__.py
│ │ └── base_response.py
│ ├── review # 추가
│ │ └── review_router.py # 추가
```

│ ├── static
│ │ └── index.html
│ └── user
│ ├── __init__.py
│ ├── user_repository.py # 변경
│ ├── user_router.py
│ ├── user_schema.py
│ └── user_service.py
├── aws # 추가, 폴더 안에 aws 및 github action 과제에서 캡
쳐한 사진들을 넣어주세요.
├── database
│ ├── mongodb_connection.py # 추가, 제공됨
│ ├── mysql_connection.py # 추가, 제공됨
│ └── ...
├── README.md # 변경, docker hub 레포 주소 및 캡쳐 사진들
나타내기
├── requirements.txt # 변경 가능
├── review_analysis
│ ├── __init__.py
│ ├── crawling
│ │ ├── __init__.py
│ │ ├── base_crawler.py
│ │ ├── example_crawler.py
│ │ ├── main.py
│ │ └── ...
│ └── preprocessing
│ ├── base_processor.py
│ ├── example_processor.py # 변경
│ ├── main.py
│ └── ...
├── test
│ ├── __init__.py
│ ├── test_user_repository.py # 추가, 제공됨
│ ├── test_user_router.py
│ └── test_user_service.py
└── ...


## 채점 기준

##### DB

```
pytest test_user_repository.py 통과(로컬에서 실행합니다)
데이터 전처리 자동화 api 생성
Docker
docker hub 주소 제출
Dockerfile 제출
AWS
총 6 개의 api endpoint 사진 첨부 및 응답 성공
github action 사진 첨부 및 status 성공
멋져요!
(이건 제출 기준 외이니 멋져요! 를 받고 싶으신 분들만 하시면 됩니다. 아래 기준 하나
만족 시 1 멋져요! - 모두 만족 시 3 멋져요!)
RDS 활용시 퍼블릭 엑세스를 허용하지 않고, VPC를 활용하여 보안 설정하기
(README에 이에 관해 간단한 설명 및 설정 화면 추가 필요)
로드 밸런서를 활용하여 포트를 외부에 노출시키지 않기 (README에 이에 관해 간단한
설명 및 설정 화면 추가 필요 / 다만, 로드 밸런서는 소량의 과금이 필요함에 유의하셔야 합
니다.)
프로젝트를 진행하며 깨달은 점, 마주쳤던 오류를 해결한 경험을 README에 작성하고
이와 관련된 개념 정리 (너무 짧으면 안되겠죠?)
```

