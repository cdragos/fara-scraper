from datetime import datetime
import string

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def _load_url(value, loader_context):
    return loader_context['response'].urljoin(value)


def _clean_country(value):
    return ''.join([
        char for char in value
        if char in string.ascii_letters or char in string.whitespace])


def _convert_date_to_iso(value):
    return datetime.strptime(value, '%m/%d/%Y').isoformat()


class ActiveForeignPrincipalLoader(ItemLoader):

    url_in = MapCompose(str.strip, _load_url)
    url_out = TakeFirst()

    country_in = MapCompose(str.strip, _clean_country)
    country_out = TakeFirst()

    state_in = MapCompose(str.strip)
    state_out = TakeFirst()

    reg_num_in = MapCompose(str.strip)
    reg_num_out = TakeFirst()

    address_in = MapCompose(str.strip)
    address_out = TakeFirst()

    foreign_principal_in = MapCompose(str.strip)
    foreign_principal_out = TakeFirst()

    foreign_principal_reg_date_in = MapCompose(str.strip, _convert_date_to_iso)
    foreign_principal_reg_date_out = TakeFirst()

    registrant_in = MapCompose(str.strip)
    registrant_out = TakeFirst()

    reg_date_in = MapCompose(str.strip, _convert_date_to_iso)
    reg_date_out = TakeFirst()

