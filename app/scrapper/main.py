#!/usr/bin/python

from scrapper import VascoScrapper
from simple_term_menu import TerminalMenu


def main():
    vs = VascoScrapper()
    all_news = vs.get_all_news()
    options = [d.get("title", None) for d in all_news]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    vs.get_news_data(all_news[menu_entry_index]["href"])
    vs.get_commentaries('/noticias/feminino-registros-do-treino-desta-quinta-27-394936.html')
    input()
    main()


if __name__ == "__main__":
    main()
