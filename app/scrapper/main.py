#!/usr/bin/python

from scrapper import VascoScrapper

def main():
    vs = VascoScrapper()
    all_news = vs.get_min_x_news(10)
    print(all_news)
    vs.get_commentaries('/noticias/vasco-abriu-negociacao-com-pepe-que-nao-deseja-jogar-no-brasil-396336.html')
    input()
    main()


if __name__ == "__main__":
    main()
