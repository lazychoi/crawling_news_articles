# 중앙일보 뉴스 크롤링 후 단어 빈도수 출력

1. 파일명: crawling_joongangilbo.py
2. 코드 설명 
  - 클래스명: Crawling_joongangilbo
  - get_link() : 키워드와 가져올 페이지 개수를 입력하면 중앙일보 기사 링크를 리스트로 반환
  - get_article() : 기사 제목과 본문을 각각 리스트로 반환
  - wordcount() : 제목과 본문에 사용된 명사와 빈도를 Counter 객체로 반환
  - wordcount_graph(title or body) : 매개변수로 'title' 또는 'body'를 입력하면 제목이나 본문의 빈도수 상위 20개 명사를 막대 그래프로 표시하고 그림파일로 저장
  - wordcloud(title or body) : 매개변수로 'title' 또는 'body'를 입력하면 제목이나 본문의 빈도수 상위 20개 명사를 워드클라우드로 표시하고 그림파일로 저장


## 터미널 출력 내용

<img width="960" alt="image" src="https://user-images.githubusercontent.com/8787919/216497077-c0480e50-275b-4c5b-bde9-c44469347bef.png">

## 저장된 그림 파일

<img width="509" alt="image" src="https://user-images.githubusercontent.com/8787919/216497272-81f11f75-faf4-4369-868f-1af5d88a468d.png">
<img width="854" alt="image" src="https://user-images.githubusercontent.com/8787919/216497332-18ecae2e-c61b-4386-8af5-769a2d451c6f.png">
