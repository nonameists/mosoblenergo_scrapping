from bs4 import BeautifulSoup as soup
import requests
from datetime import datetime as dt


def parsing_date(text):
    for fmt in ('%d.%m.%Y', '%d/%m/%Y', '%d,%m.%Y', '%d,%m,%Y', '%d.%m,%Y'):
        try:
            return dt.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def prepare_values(raw_data):
    """
    Функция принимает на вход объект класса bs4.element.ResultSet
    Предобрабатывает данные и возвращает список кортежей вида:
    [(дата_начала_работ, время начала_работ, дата_окончания_работ, время_оконачания, адрес, причина_отлючения)]

    :param raw_data: <class 'bs4.element.ResultSet'> object
    :return: List of tuples
    """
    result = []
    for row in raw_data:
        row = row.find_all('td')
        start_date, start_hour = row[1].text.split()[:2]
        end_date, end_hour = row[2].text.split()[:2]

        start_date = parsing_date(start_date)
        end_date = parsing_date(end_date)

        address = row[4].text.strip()
        # remove extra spaces between words
        address = " ".join(address.split())
        reason = row[5].text.strip()
        # remove extra spaces
        reason = " ".join(reason.split())

        values = (start_date, start_hour, end_date, end_hour, address, reason)
        result.append(values)

    return result


def main():
    city = ''
    payload = {
        'arrFilter_pf[potr1]': city,
        'set_filter ': 'Фильтр',
        'set_filter': 'Y'
    }

    url = f'https://www.mosoblenergo.ru/users/off/p-off.php'

    page_source = requests.get(url, params=payload)

    if page_source.status_code == 200:
        data = soup(page_source.content, 'html.parser')
        table_data = data.findAll('tr', {'style': 'font-size: 12px;'})
        return prepare_values(table_data)

    return False


if __name__ == "__main__":
    main()

