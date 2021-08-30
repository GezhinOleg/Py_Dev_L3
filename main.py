import requests
from bs4 import BeautifulSoup as bs


KEYWORDS = {'дизайн', 'фото', 'web', 'python'}
BASEURL = 'https://habr.com/ru/all/'


def get_url_text(url):
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        return False
# проверяем ответ от сервера, если ответ поступил, продолжаем работу иначе возвращаем ложь и программа прекращает работу.

def main(url=BASEURL):
    text = get_url_text(url)
    soup = bs(text, features='html.parser')
    articles = soup.find_all('article')
    article_list = []
    for article in articles:
        article_time = article.find('span', class_='tm-article-snippet__datetime-published').text
        # Получаем время написания статьи
        article_title = article.find('a', class_='tm-article-snippet__title-link')
        # Получаем текст лежащий между тегами <a></a>
        article_title_link = article_title['href']
        # Получаем текст сокращенной ссылки
        hubs = [h.text.strip() for h in article.find_all('a', class_='tm-article-snippet__title-link')]
        st_list = hubs[0].lower().split()
        # Буквы полученного текста приводим к строчному представлению, чтобы не упустить слова из-за написания
        for st in st_list:
            if st in KEYWORDS:
                text = ''.join(hubs)
                article_list.append(f"{article_time} - {text} - https://habr.com{article_title_link}")
    return article_list


if __name__ == '__main__':
    output_list = []
    pages = int(input('Введите количество страниц: '))
    for page in range(pages):
        print(f'Обрабатываем страницу {page + 1} из {pages}')
        if page == 0:
            output_list += main()
        else:
            output_list += main(url=f'{BASEURL}page{page+1}/')
    print(*output_list, sep='\n')
