import re
from threading import Thread
import logging
from argparse import ArgumentParser
from urllib import request as urllib_request
import json


class Price:
    country_code = None
    country_name = None
    currency = None
    value = None

    def __init__(self, country_code, country_name):
        self.country_name = country_name
        self.country_code = country_code


COUNTRIES = {
    "US": "United States",
    "AR": "Argentina",
    "BS": "Bahamas",
    "BR": "Brazil",
    "CA": "Canada",
    "CL": "Chile",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "GL": "Greenland",
    "MX": "Mexico",
    "PA": "Panama",
    "VE": "Venezuela",
    "AL": "Albania",
    "AD": "Andorra",
    "AT": "Austria",
    "BE": "Belgium",
    "BA": "Bosnia and Herzegovina",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "EE": "Estonia",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HU": "Hungary",
    "IS": "Iceland",
    "IE": "Ireland",
    "IM": "Isle of Man",
    "IT": "Italy",
    "LV": "Latvia",
    "LI": "Liechtenstein",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MT": "Malta",
    "MD": "Moldova",
    "MC": "Monaco",
    "ME": "Montenegro",
    "NL": "Netherlands",
    "MK": "North Macedonia",
    "NO": "Norway",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "RS": "Serbia",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "ES": "Spain",
    "SE": "Sweden",
    "CH": "Switzerland",
    "TR": "Turkey",
    "UA": "Ukraine",
    "GB": "United Kingdom",
    "AU": "Australia",
    "BD": "Bangladesh",
    "KH": "Cambodia",
    "CN": "China",
    "HK": "Hong Kong SAR China",
    "IN": "India",
    "ID": "Indonesia",
    "JP": "Japan",
    "MY": "Malaysia",
    "MN": "Mongolia",
    "NZ": "New Zealand",
    "PH": "Philippines",
    "SG": "Singapore",
    "LK": "Sri Lanka",
    "TW": "Taiwan",
    "VN": "Vietnam",
    "DZ": "Algeria",
    "AM": "Armenia",
    "EG": "Egypt",
    "GE": "Georgia",
    "IL": "Israel",
    "KZ": "Kazakhstan",
    "MA": "Morocco",
    "NG": "Nigeria",
    "QA": "Qatar",
    "SA": "Saudi Arabia",
    "ZA": "South Africa",
    "AE": "United Arab Emirates"}

COUNTRY_PRICES = [Price(key, value) for key, value in COUNTRIES.items()]

logging.basicConfig(
    level=logging.INFO,
)


def extract_product_id(url):
    html = urllib_request.urlopen(url).read().decode('utf-8')
    raw_card_product = re.search(r"card-product=\"\d*\"", html).group()
    product_id = re.search(r"(\d+)", raw_card_product).group()
    logging.debug(f"raw product id: {raw_card_product}")
    logging.debug(f"product id: {product_id}")
    return product_id


def request_price(product_id, price, normalize=None):
    data = None
    url = f"https://api.gog.com/products/{product_id}/prices?countryCode={price.country_code}"
    if normalize:
        url += "&currency=USD"
    try:
        logging.debug(url)
        response = urllib_request.urlopen(url).read().decode('utf-8')
        data = json.loads(response)
        logging.debug(data)
        final_price = data['_embedded']['prices'][0]['finalPrice'].split(" ")
        final_price[0] = int(final_price[0]) / 100
        logging.debug(price)
        price.value = final_price[0]
        price.currency = final_price[1]
    except KeyError as no_key_error:
        logging.error(no_key_error)
        logging.error(data)


def request_prices(product_id, normalize=None):
    threads = []
    for price in COUNTRY_PRICES:
        t = Thread(target=request_price, args=(product_id, price, normalize))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def sort_prices():
    return sorted(COUNTRY_PRICES, key=lambda x: x.value, reverse=False)


def out_result(count, pretty=None):
    sorted_prices = sort_prices()
    count = min(abs(count), len(sorted_prices))
    out_string = ""
    if pretty:
        shift_country = 25
        shift_price = 10
        header = f"{'Country':<{shift_country}} {'Price':<{shift_price}} {'Currency'}\n"
        out_string += header
        out_string += "-" * (len(header)-1)
        for i, price in enumerate(sorted_prices):
            if i == count:
                break
            out_string += f"\n{price.country_name:<{shift_country}} {price.value:<{shift_price}} {price.currency}"
    else:
        for i, price in enumerate(sorted_prices):
            if i == count:
                break
            out_string += f"\n{price.country_name}: {price.value} {price.currency}"
    print(out_string)


def main():
    args = init_parser().parse_args()
    if "gogdb.org" in args.url:
        product_id = args.url.split("/")[-1]
    else:
        product_id = extract_product_id(args.url)
    request_prices(product_id, args.normalize)
    sort_prices()
    out_result(args.count, args.pretty)


def init_parser():
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", required=True, type=str, help="url to scrape")
    parser.add_argument("-n", "--normalize", action="store_true", help="normalize currencies to USD")
    parser.add_argument("-c", "--count", type=int, default=10, help="number of countries to show")
    parser.add_argument("-p", "--pretty", action="store_true", help="shows result as pretty table")
    return parser


if __name__ == "__main__":
    main()
