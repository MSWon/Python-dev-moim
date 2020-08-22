import re
import requests
import time
from bs4 import BeautifulSoup


# 각 url 정보
RANKING_URL = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200810&page=' # 랭킹 URL
MAIN_URL = "https://movie.naver.com/movie/bi/mi/basic.nhn?code="                              # 영화의 주요정보 URL
IMG_URL = "https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode="                 # 영화의 이미지 URL
ACTOR_URL = "https://movie.naver.com/movie/bi/mi/detail.nhn?code="                            # 영화의 배우정보 URL


def get_movie_id() -> str:
    '''
    :return: get_movie_id 함수를 호출할 때마다, 그 다음번의 영화 id값을 문자열 타입으로 반환
    '''
    for i in range(1, 41):  # 1 ~ 41 페이지
        req = requests.get(RANKING_URL + str(i))
        if req.status_code == 200:
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            movies = soup.find_all('a',
                                   {'href': True, 'title': True, 'onclick': False, 'class': False, 'target': False})
            for movie in movies[1:]:
                yield re.search('[\d]{1,}', movie['href']).group()


def get_contents(movie_id:str) -> list:
    '''
    :param movie_id: 영화 고유 아이디(문자열)
    :return: 영화 제목, 개봉일, 줄거리 등의 정보(리스트)
    '''
    time.sleep(0.01)

    # 1. main_link (= 영화 주요 정보 주소)
    main_link = MAIN_URL + movie_id

    # 2. img_link(= 영화 이미지 주소)
    img_link = MAIN_URL + movie_id

    req = requests.get(main_link)
    if req.status_code == 200:
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        # 3. title
        try:
            title = soup.find('h3', {'class': 'h_movie'}).find('a', {'href': True}).text
            title = re.sub('[^0-9a-zA-Z가-힣,/. ]', '', title)
            # print()
        except:
            return [''] * 11

        # 4. user_rating
        try:
            user_rating = soup.find('a', {'id': 'pointNetizenPersentBasic'}).text
        except:
            user_rating = ''


        # 5.장르, 6.국가, 7.개봉년도 구하기
        try:
            info_spec = soup.find('dl', {'class': 'info_spec'})
            genre = []
            nation = []
            pub_year = ""
            for info in info_spec.find_all('a', {'href': True}):
                if 'genre' in info['href']:
                    genre.append(info.text)
                elif 'nation' in info['href']:
                    nation.append(info.text)
                elif 'open' in info['href']:
                    pub_year = info.text
                    break

            genre = ','.join(genre)
            nation = ','.join(nation)
            pub_year = pub_year.strip()
        except:
            genre = ''
            nation = ''
            pub_year = ''

        # 8. 줄거리
        try:
            summary = soup.find('div', {'class': 'story_area'}).find('p', {'class': 'con_tx'})
            summary = re.sub('[^\da-zA-Z가-힣/. ]', '', summary.text).strip()
        except:
            summary = ''

        # 9.배우, 10.감독
        actor_link = ACTOR_URL + movie_id
        req = requests.get(actor_link)
        if req.status_code == 200:
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            # 배우
            try:
                actors = []
                for p in soup.find('ul', {'class': 'lst_people'}).find_all('a', {'class': 'k_name'}):
                    actors.append(p['title'])
                actors = ','.join(actors)
            except:
                actors = ''

            # 감독
            try:
                directors = []
                for p in soup.find('div', {'class': 'director'}).find_all('a', {'class': 'k_name'}):
                    directors.append(p['title'])
                directors = ','.join(directors)
            except:
                directors = ''
    # 영화 id, 제목, link, 이미지link, 개봉일, 네티즌평점, 감독, 배우, 줄거리, 국가, 장르
    return [movie_id, title, main_link, img_link, pub_year, user_rating, directors, actors, summary, nation, genre]