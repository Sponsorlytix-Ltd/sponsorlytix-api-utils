from sponsorlytix_api_utils.sponsorlytix_country.database import countries_database

find_by_keys = ['name', 'code', 'continent_name', 'continent_code']


def find_country(search_value, find_by):
    if find_by in find_by_keys:
        filter_function = lambda country: search_value == country.get(find_by)
        return filter(filter_function, countries_database)
    raise ValueError(
        'find_by value is not valid, try to search by this values: name, code, continent_name, continent_code')


def find_continent(search_value, find_by):
    if find_by in find_by_keys:
        continent_filter_function = lambda country: search_value == country.get(find_by)
        continents = filter(continent_filter_function, countries_database)
        def continent_map(continent):
            continent_countries = find_country(continent.get('code'), 'continent_code')
            return continent.update({'country': continent_countries})
        return map(continent_map, continents)
    raise ValueError(
        'find_by value is not valid, try to search by this values: name, code, continent_name, continent_code')
