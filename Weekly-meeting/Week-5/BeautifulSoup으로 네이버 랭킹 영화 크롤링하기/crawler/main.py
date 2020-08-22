from multiprocessing import Pool
import crawling
import pandas as pd


if __name__ == '__main__':
    pool = Pool(processes=4)
    data = list(pool.map(crawling.get_contents, crawling.get_movie_id()))

    columns = ['movie_id', 'title', 'main_link', 'img_link', 'pub_year', 'user_rating', 'directors', 'actors', 'summary', 'nation', 'genre']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('movie2.csv', index=False, encoding='euc-kr')

