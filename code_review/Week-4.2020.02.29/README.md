# Week - 4
## 나만의 CLI 파이썬 패키지 만들기
- CLI : Command Line Interface의 줄임말로 터미널을 통해 사용자와 컴퓨터가 상호 작용하는 방식을 뜻함(ex: ls, cd )
- setup.py를 통해 나만의 CLI 패키지를 설치 할 수 있음
- **moim**이라는 이름의 패키지를 만들어 봄 
  - **moim clean** : 텍스트 데이터를 정제해주는 명령어
  - **moim stats** : 텍스트 데이터의 상위 n개의 단어 빈도수를 반환해주는 명령어 
- [참고사이트](https://sjquant.tistory.com/18)

## 설치 방법
**1. Git clone**
```
$ git clone https://github.com/MSWon/Python-dev-moim.git 
```
**2. moim 폴더로 디렉토리 이동**
```
$ cd ./Python-dev-moim/code_review/Week-4.2020.02.29/moim
```
**3. setup.py를 통한 패키지 설치**
```
$ python setup.py install
```
## CLI 커맨드 사용법
**1. 패키지 버전 확인**
```
$ moim --version
>> moim 1.0.0
```
**2. moim help 명령어 사용**
```
$ moim --help
>> usage: moim [-h] [--version] {clean,stats} ...

  positional arguments:
    {clean,stats}
      clean        package for cleaning text data
      stats        package for statistics of text data

  optional arguments:
    -h, --help     show this help message and exit
    --version, -v  show program's version number and exit
```
**3. moim clean 명령어 사용**
```
$ cd ../moim_test
$ moim clean --input_path ./train.en --output_path ./train.en.clean
>> cleaning finished
```
**4. moim stats 명령어 사용**
```
$ moim stats --input_path ./train.en.clean -n 10
>> statistics for top 10 frequent words in ./train.en.clean
         word  frequency
    1.    the     109162
    2.     to      53872
    3.     of      51106
    4.      a      46140
    5.     in      44386
    6.    and      42476
    7.    The      18581
    8.    for      17521
    9.     on      17098
    10.  that      16536
```
