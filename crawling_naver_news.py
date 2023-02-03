import sys, requests, matplotlib
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class CrawlingNaverNews_anlaysis:

    def __init__(self, argv):
        if len(argv) != 3:
            print("'python crawling_naver_news.py 검색어 가져올_페이지_개수' 형식으로 입력하세요.")
            return

        self.keyword = argv[1]
        self.page_range = int(argv[2])

        self.font_name = 'NanumBarunGothic'
        self.URL_BEFORE_KEYWORD = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query='
        self.URL_BEFORE_PAGENUM = '&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=134&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start='

        self.count = 0
        self.by_num = 0

    def get_link(self):
        link = []

        for page in range(self.page_range):
            current_page = 1 + page * 10  # 네이버 뉴스 페이지 1, 11, 21, ... 형식
            crawling_url_list = self.URL_BEFORE_KEYWORD + self.keyword + self.URL_BEFORE_PAGENUM + str(current_page)

            res = requests.get(crawling_url_list)
            soup = BeautifulSoup(res.text, 'lxml')

            url_tag = soup.select('div.news_area > a')

            for url in url_tag:
                link.append(url['href'])

            return link

    def get_article(self, file='article.txt'):
        print("데이터 불러오는 중....")
        link = self.get_link()

        with open(file, 'w', encoding='utf8') as f:
            i = 1

            for url in link:
                article = Article(url, language='ko')

                try:
                    article.download()
                    article.parse()
                except:
                    print('-', str(i), '번째 URL은 크롤링할 수 없습니다.')
                    continue

                news_title = article.title
                news_content = article.text

                f.write('[' + str(i) + ']  ')
                f.write(news_title + '\n')
                f.write('-' * 50 + '\n')
                f.write(news_content)
                f.write('\n\n\n\n')

                i += 1

        print('- 네이버 뉴스 "' + self.keyword + '" 관련 뉴스 기사 ' + str(self.page_range) + '페이지(기사 ' + str(
            i - 1) + '개)가 저장되었습니다.')

    def wordcount(self, open_filename, save_filename):
        """뉴스 기사 파일(open_filename)을 열어 명사별 빈도수를 save_fiilname에 저장"""

        f = open(open_filename, 'r', encoding='utf8')
        g = open(save_filename, 'w', encoding='utf8')

        engine = Okt()
        data = f.read()
        all_nouns = engine.nouns(data)
        nouns = [n for n in all_nouns if len(n) > 1]

        count = Counter(nouns)
        by_num = OrderedDict(sorted(count.items(), key=lambda t: t[1], reverse=True))

        word = [i for i in by_num.keys()]
        number = [i for i in by_num.values()]

        for w, n in zip(word, number):
            final = '%s %d' % (w, n)
            g.write(final + '\n')

        print(f'- 단어 카운팅이 완료되었습니다. ({save_filename})\n')
        f.close(), g.close()

        return count, by_num

    def wordcount_graph(self, by_num):
        """모든 단어와 단어의 개수를 막대그래프로 시각화하고 이미지를 저장"""
        print('그래프 생성 중.....')

        for w, n in list(by_num.items()):
            if n <= 15:
                del by_num[w]

        fig = plt.gcf()
        fig.set_size_inches(20, 10)
        matplotlib.rc('font', family=self.font_name, size=10)
        plt.title('기사에 나온 전체 단어 빈도수', fontsize=30)
        plt.xlabel('기사에 나온 단어', fontsize=15)
        plt.ylabel('기사에 나온 단어의 개수', fontsize=15)
        plt.bar(by_num.keys(), by_num.values(), color='#6799FF')
        plt.xticks(rotation=45)
        plt.savefig('all_words.jpg')
        plt.show()
        print('- all_words.jpg가 저장되었습니다.')

    def top_10(self, count, save_filename):
        """가장 많이 나온 단어 10개 파일로 저장"""

        print('가장 많이 나온 단어 10개 추출 중....')

        f = open(save_filename, 'w', encoding='utf8')

        rank = count.most_common(10)

        global top

        top = dict(rank)
        word = [i for i in top.keys()]
        number = [i for i in top.values()]

        for w, n in zip(word, number):
            final2 = f'({w}, {n})'
            f.write(final2 + '\n')

        print('- 최다 빈출 단어 10개가 저장되었습니다. (top.txt)')
        f.close()

    # def top10():
    #     """wordcount.txt 파일 불러와 상위 10개 추출하여 top10.txt 파일에 저장"""
    #
    #     print('가장 많이 나온 단어 10개 추출 중....')
    #
    #     f = open('top10.txt', 'w', encoding='utf8')
    #     g = open('wordcount.txt', 'r', encoding='utf8')
    #     for i in range(10):
    #         tmp = g.readline()
    #         f.write(tmp)
    #
    #     print('- 최다 빈출 단어 10개가 저장되었습니다. (top10.txt)')
    #     f.close(), g.close()

    def wordcloud(self, wordcount_filename):
        print('워드 클라우드 생성 중....')

        with open(wordcount_filename, encoding='utf8') as f:
            data = f.read()

            engine = Okt()
            all_nouns = engine.nouns(data)

            nouns = [n for n in all_nouns if len(n) > 1]
            count = Counter(nouns)
            tags = count.most_common(100)
            print('tags 형식 -> ', tags[0])

            wc = WordCloud(font_path=self.font_name, background_color=(168, 237, 244), width=2500, height=1500)
            cloud = wc.generate_from_frequencies(dict(tags))
            plt.imshow(cloud, interpolation='bilinear')
            plt.axis('off')  # 축 가리기
            plt.savefig('cloud.jpg')
            plt.show()

        print('- cloud.jpg가 저장되었습니다.')


def main(argv):
    news = CrawlingNaverNews_anlaysis(argv)
    news_filename = 'iu.txt'
    wordcount_filename = 'iu_count.txt'
    wordcount_top10_filename = 'iu_count10.txt'

    news.get_article()
    news.get_article(news_filename)
    count, by_num = news.wordcount(news_filename, wordcount_filename)
    news.wordcount_graph(by_num)  # 메서드 단독으로 실행할 수 없는 문제 있음. wordcount()에서 반환하는 by_num 필요
    news.top_10(count, wordcount_top10_filename)  # 메서드 단독으로 실행할 수 없는 문제 있음. wordcount()에서 반환하는 count 필요
    news.wordcloud(wordcount_filename)  # 메서드 단독으로 실행할 수 없는 문제 있음. wordcount()에서 생성하는 wordcount 파일이 있어야함

    # 메서드 중 단독으로 실행할 수 없는 것을 단독으로 실행하게 하려면
    # 전제가 되는 메서드를 매개변수에 따라 결과를 파일로 저장하는 옵션과 변수로 저장하는 옵션으로 나누어 작성하고
    # 단독으로 실행할 수 없는 메서드 안에 결과를 변수로 저장하는 메서드를 호출하도록 함


if __name__ == '__main__':
    main(sys.argv)
