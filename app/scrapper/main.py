#!/usr/bin/python

from scrapper import VascoScrapper

def main():
    vs = VascoScrapper()
    vs.get_min_x_news(10)

    vs.get_page_data('/noticias/pedrinho-completa-6-meses-no-vasco-confira-os-proximos-desafios-397313.html')
    vs.get_page_data('/noticias/ntv-aborda-os-principais-motivos-para-as-lesoes-no-vasco-397315.html')
    print(vs.commentaries)

if __name__ == "__main__":
    main()
