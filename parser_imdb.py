import json
from bs4 import BeautifulSoup
import httpx
from fake_useragent import UserAgent

data = {"films": {},
        "tv": {}}

type_video = input("movie or tv: ")

url = f'https://www.imdb.com/calendar/?region=CA&type={type_video.upper()}&ref_=rlm'
response = httpx.get(url, headers={'User-Agent': UserAgent().random})

soup = BeautifulSoup(response.text, 'lxml')

if type_video[0] == 'm' or type_video[0] == 'M':
    if response.status_code == 200:
        title_films = soup.find_all('a', class_='ipc-metadata-list-summary-item__t')
        for title_film in title_films:
            films_share = 'https://www.imdb.com/' + title_film.get('href')
            # print(title_film.text, ' | ', films_share)
            data['films'][title_film.text] = films_share

        with open("imdb.json", "w") as file:
            json.dump(data['films'], file, indent=4)


elif type_video[0] == 't' or type_video[0] == 'T':
    if response.status_code == 200:
        title_tv_serials = soup.find_all('a', class_='ipc-metadata-list-summary-item__t')
        for title_tv_serial in title_tv_serials:
            data['tv'][title_tv_serial.text] = title_tv_serial.text

        with open("imdb.json", "w") as file:
            json.dump(data['tv'], file, indent=4)

else:
    print(f'imdb url Error: {response.status_code}')

