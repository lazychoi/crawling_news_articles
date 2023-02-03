import sys, requests, matplotlib
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class Crawling_joongangilbo:

    def __init__(self):
        try:
            self.keyword = input('검색어를 입력하세요 >> ')
            self.page_range = int(input('가져올 뉴스 페이지 개수를 숫자로 입력하세요 >> '))
        except:
            print('안내에 맞게 입력하세요.')

        self.font_name = 'NanumBarunGothic'
        self.URL_BEFORE_KEYWORD = 'https://www.joongang.co.kr/search/news?keyword='
        self.URL_BEFORE_PAGENUM = '&page='

        self.count = 0
        self.by_num = 0

    def get_link(self):
        '''키워드 검색 기사 링크 반환'''
        link = []

        for page in range(self.page_range):
            current_page = 1 + page * 10  # 네이버 뉴스 페이지 1, 11, 21, ... 형식
            crawling_url_list = self.URL_BEFORE_KEYWORD + self.keyword + self.URL_BEFORE_PAGENUM + str(current_page)

            res = requests.get(crawling_url_list)
            soup = BeautifulSoup(res.text, 'lxml')

            url_tag = soup.select('section.chain_wrap.col_lg9  h2.headline > a')
            for url in url_tag:
                link.append(url['href'])
            return link

    def get_article(self):
        '''
        1. get_link() 메서드를 이용
        2. article_title 리스트에는 기사의 제목을 저장
        3. article_body 리스트에는 기사의 본문을 저장
        '''
        print("데이터 불러오는 중....")
        link = self.get_link()
        article_title = []
        article_body = []

        for url in link:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'lxml')

            article_title.append(soup.select_one('h1.headline').text)
            article_body.append(soup.select_one('div.article_body.fs3').text)

        print(f'총 {len(article_title)}개의 기사가 검색되었습니다.')

        return article_title, article_body

    def wordcount(self):
        """뉴스 기사 파일(open_filename)을 열어 명사별 빈도수를 save_fiilname에 저장"""
        title, body = self.get_article()
        all_titles = ''
        all_bodys = ''
        for item in title:
            all_titles += item
        for item in body:
            all_bodys += item
        # print(all_bodys)

        # 명사만 추출
        engine = Okt()
        title_nouns = engine.nouns(all_titles)
        body_nouns = engine.nouns(all_bodys)
        # print(title_nouns)
        # print(body_nouns)

        # 본문에 나온 2글자 이상의 단어 개수
        # Counter 메서드 반환값 => {'드론': 72, '아이유': 55, '가수': 54, '기술': 48, '사람': 46, '도서관': 43, ... }
        count_title_nous = Counter([n for n in title_nouns if len(n) > 1])
        count_body_nouns = Counter([n for n in body_nouns if len(n) > 1])
        print(f'제목에 등장하는 명사 단어의 빈도수 >>> \n{count_title_nous}')
        print(f'본문에 등장하는 명사 단어의 빈도수 >>> \n{count_body_nouns}')

        return count_title_nous, count_body_nouns

    def wordcount_graph(self, title_or_body):
        """
        모든 단어와 단어의 개수를 막대그래프로 시각화하고 이미지를 저장
        기사 제목으로 빈도수 그래프를 만들려면 매개변수에 title을,
        기산 본문으로 빈도수 그래프를 만들려면 매개변수에 body를 입력
        """

        count_title_nous, count_body_nouns = self.wordcount()

        if title_or_body == 'title':
            show_nouns = count_title_nous
        elif title_or_body == 'body':
            show_nouns = count_body_nouns
        else:
            return print('title, body 중 하나를 입력하세요')

        print('그래프 생성 중.....')

        # 빈도수 상위 20개만 뽑기.
        # most_common() 메서드는 리스트로 반환 -> 다시 dict형으로 변환
        show_nouns = dict(show_nouns.most_common(20))

        fig = plt.gcf()
        fig.set_size_inches(20, 10)
        matplotlib.rc('font', family=self.font_name, size=10)
        plt.title('기사에 나온 전체 단어 빈도수', fontsize=30)
        plt.xlabel('기사에 나온 단어', fontsize=15)
        plt.ylabel('기사에 나온 단어의 개수', fontsize=15)
        plt.bar(show_nouns.keys(), show_nouns.values(), color='#6799FF')
        plt.savefig('frequent_words.jpg')
        plt.xticks(rotation=45)
        plt.show()
        print('단어 빈도수 그래프가 파일(frequent_words.jpg)로 저장되었습니다.')

    def wordcloud(self, title_or_body):
        '''
        기사 제목으로 워드클라우드를 만들려면 매개변수에 title을,
        기산 본문으로 워드클라우드를 만들려면 매개변수에 body를 입력
        '''
        count_title_nous, count_body_nouns = self.wordcount()

        if title_or_body == 'title':
            show_nouns = count_title_nous
        elif title_or_body == 'body':
            show_nouns = count_body_nouns
        else:
            return print('title, body 중 하나를 입력하세요')

        print('워드 클라우드 생성 중....')

        # 빈도수 상위 100개 추출
        tags = show_nouns.most_common(100)
        wc = WordCloud(font_path=self.font_name, background_color=(168, 237, 244), width=2500, height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))
        plt.imshow(cloud, interpolation='bilinear')
        plt.axis('off')  # 축 가리기
        plt.savefig('word_cloud.jpg')
        plt.show()

        print('word_cloud.jpg가 저장되었습니다.')


def main():
    news = Crawling_joongangilbo()
    news.wordcloud('title')


if __name__ == '__main__':
    main()
