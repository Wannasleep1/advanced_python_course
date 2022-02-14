from collections import namedtuple
from typing import List, Optional, Tuple
import bs4
import requests as req
from bs4 import BeautifulSoup


class HabrArticlesParser:
    BASE_URL = r"https://habr.com"
    URL = BASE_URL + r"/ru/all/"
    HEADERS = {
        'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415;'
                  ' _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2;'
                  ' __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        'sec-ch-ua-mobile': '?0'}

    def __init__(self, keywords: List[str]):
        self.keywords = [kw.lower() for kw in keywords] if keywords else keywords
        self.text: str = self._get_page(self.URL)
        self.soup: BeautifulSoup = self._get_soup(self.text)
        self.articles: Optional[bs4.element.ResultSet] = None
        self.filtered_articles: Optional[bs4.element.ResultSet] = None
        self.articles_meta_info: list = []

    @staticmethod
    def _get_soup(text: str) -> bs4.BeautifulSoup:
        return BeautifulSoup(text, features="html.parser")

    @staticmethod
    def _get_page(url):
        return req.get(url, headers=HabrArticlesParser.HEADERS).text

    def __get_all_articles(self) -> bs4.element.ResultSet:
        self.articles = self.soup.find_all(name="article")
        return self.articles

    @staticmethod
    def __get_link(article: bs4.element.Tag) -> str:
        return article.find(name="a", class_="tm-article-snippet__readmore").attrs.get("href")

    @staticmethod
    def __get_text_from_article(sp: BeautifulSoup) -> str:
        text_blocks = sp.find(class_="tm-article-body").find_all(name="p")
        return " ".join([elem.text.lower() for elem in text_blocks])

    def __check_content(self, articles: bs4.element.ResultSet) -> List[bool]:
        in_article = []
        for elem in articles:
            link = self.__get_link(elem)
            article_content = self._get_page(self.BASE_URL+link)
            sp = self._get_soup(article_content)
            article_text = self.__get_text_from_article(sp)
            is_mentioned = any([word in article_text for word in self.keywords])
            in_article.append(is_mentioned)

        return in_article

    @staticmethod
    def __get_preview_info(article: bs4.element.Tag) -> Tuple[str, str, str, str]:
        author = article.find(class_="tm-user-info tm-article-snippet__author").text.lower().strip()
        title = article.find(class_=["tm-article-snippet__title tm-article-snippet__title_h2"]).text.lower()
        hubs_lst = article.find_all(class_="tm-article-snippet__hubs")
        hubs = "".join([hub.text.lower() for hub in hubs_lst])
        text_body = article.find(class_=["article-formatted-body article-formatted-body_version-2",
                                         "article-formatted-body article-formatted-body_version-1"]).text.lower()

        return author, title, hubs, text_body

    def __is_mentioned_in_article_preview(self, info: Tuple[str, str, str, str]) -> bool:
        return any([kw in elem for kw in self.keywords for elem in info])

    def __check_preview(self, articles: bs4.element.ResultSet) -> List[bool]:
        in_preview = []
        for elem in articles:
            preview_info = self.__get_preview_info(elem)
            is_mentioned = self.__is_mentioned_in_article_preview(preview_info)
            in_preview.append(is_mentioned)

        return in_preview

    @staticmethod
    def __get_checked_articles(articles: bs4.element.ResultSet, in_content: List[bool]) -> List[bs4.element.Tag]:
        filtered_articles = []
        for i in range(len(in_content)):
            if in_content[i]:
                filtered_articles.append(articles[i])

        return filtered_articles

    def __fill_in_articles_meta_info(self) -> None:
        MetaInfo = namedtuple("MetaInfo", ["date", "title", "link"])
        for elem in self.filtered_articles:
            date = elem.find(name="time").attrs.get("datetime").split("T")[0]
            title = elem.find(class_=["tm-article-snippet__title tm-article-snippet__title_h2"]).text
            link = self.__get_link(elem)
            self.articles_meta_info.append(MetaInfo(date, title, link))

    def get_articles(self, content_search: bool = False) -> List[bs4.element.Tag]:
        if type(content_search) != bool:
            raise TypeError("content_search attribute has to have bool type!")
        articles = self.__get_all_articles()
        preview_check = self.__check_preview(articles)
        if not self.keywords:
            self.filtered_articles = articles
        elif content_search:
            content_check = self.__check_content(articles)
            united_checks = [any([preview_check[i], content_check[i]]) for i in range(len(preview_check))]
            self.filtered_articles = self.__get_checked_articles(articles, united_checks)
        else:
            self.filtered_articles = self.__get_checked_articles(articles, preview_check)
        self.__fill_in_articles_meta_info()

        return self.filtered_articles

    def __str__(self):
        string = ""
        for elem in self.articles_meta_info:
            string += f"{elem.date} - {elem.title} - {self.BASE_URL + elem.link}\n"

        return string.rstrip()


def main() -> HabrArticlesParser:
    keywords = list(input("Enter words divided by space to search by: ").split())
    # Для тестирования
    # keywords = ['дизайн', 'фото', 'web', 'python']
    parser = HabrArticlesParser(keywords)
    return parser


if __name__ == "__main__":
    habr_parser = main()
    habr_parser.get_articles(content_search=True)
    print(habr_parser)
