#스마트 경진 대회 스디스 웹 서버

## 구축
```buildoutcfg
1. git에서 뚞딲뚞딲 플라스크를 받아온다.
     $ git clone https://github.com/agurimon/sds-server
         (만약 안된다면) $ sudo apt install git

2. python3, python3-pip, virtualenv을 설치한다.
     $ sudo apt install python3 python3-pip virtualenv

3. mysql-server libmysqlclient-dev
     $ sudo apt install mysql-server libmysqlclient-dev

3. 프로젝트에 venv(가상환경)을 만든다.
     $ virtualenv venv -p python3

4. venv을 활성화한다.
     $ source ./venv/bin/activate

5. 라이브러리를 설치한다.
     $ pip install -r requirements.txt

6. bower(웹 프론트엔드 패키지 관리자) 설치
     $ sudo npm install -g bower
         (만약 안된다면) $ sudo apt install nodejs, npm
     $ ln -s /usr/bin/nodejs /usr/local/bin/node

7. bower(프론트엔드 패키지 라이브러리 설치
     $ bower install
```


## 실행
```buildoutcfg
1. venv을 활성화한다.
     $ source ./venv/bin/activate

2.
     $ source .env  (.env안에 (1)이 포함되어 있음)

3-1. 실행한다.
     $ flask run

3-2. 포트번호를 바꾸고 싶다.
    - runserver.py에서 바꾼다.
     $ python runserver.py
```

## 오류
```buildoutcfg

```
