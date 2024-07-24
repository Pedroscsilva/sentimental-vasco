#!/usr/bin/python

from scrapper import VascoScrapper


def main():
    vs = VascoScrapper()
    vs.get_min_x_news(10)

    hrefs = vs.hrefs['hrefs']

    for href in hrefs:
        vs.get_page_data(href)

    vs.commentaries.to_csv('commentaries.csv', index=False)
    vs.obtained_page.to_csv('pages.csv')


if __name__ == "__main__":
    main()
