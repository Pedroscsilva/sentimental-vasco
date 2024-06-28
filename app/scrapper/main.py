#!/usr/bin/python

from scrapper import get_all_news, get_specific_new, get_commentaries
from simple_term_menu import TerminalMenu


def main():
    all_news = get_all_news()
    options = [d.get("title", None) for d in all_news]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    get_specific_new(all_news[menu_entry_index]["href"])
    get_commentaries('/noticias/doria-tem-contrato-com-o-santos-laguna-ate-2025-394971.html')
    input()
    main()


if __name__ == "__main__":
    main()
