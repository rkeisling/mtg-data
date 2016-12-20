from requests import get
from bs4 import BeautifulSoup
from time import sleep


def card(row):
    try:
        count = int(row.select_one('.inventory_count').text)
        name = row.select('td')[1].text.strip()
        set = row.select_one(
                    '.mtg_edition_container img')['data-title'].split('(')[0]
        is_foil = bool(row.select('img[data-title="Foil"]'))
        return (count, name, set, is_foil)
    except:
        return None


def fetch_page_cards(n):
    url = 'https://deckbox.org/sets/1029760?p=' + str(n)
    page = get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.select_one('.set_cards')
    card_rows = table.select('tr')
    return list(filter(None, map(card, card_rows)))


def fetch_cards():
    all_cards = []
    for n in range(1, 100):
        page_cards = fetch_page_cards(n)
        if page_cards:
            all_cards.extend(page_cards)
            sleep(1/4)
        else:
            break
    return all_cards


def main():
    the_file = open('inventory.txt', 'w')
    the_file.write(str(fetch_cards()))


if __name__ == '__main__':
    main()