from sponsorlytix_api_utils.sponsorlytix_country.database import countries_database

find_by_keys = ['name', 'code', 'continent']


def find_country(search_value, find_by):
    valid_find_by = ['code', 'name', 'continent']
    if find_by in valid_find_by:
        filter_function = lambda country: search_value == country.get(find_by)
        return list(filter(filter_function, countries_database))
    raise ValueError(
        'find_by value is not valid, try to search by this values: name, code, continent')


def find_continent(search_value, find_by):
    valid_find_by = ['code', 'name']
    if find_by in valid_find_by:
        continent_filter_function = lambda continent: search_value == continent.get(find_by) and continent.get('type') == 'continent'
        continents = filter(continent_filter_function, countries_database)
        def continent_map(continent):
            continent_countries = find_country(continent.get('name'), 'continent')
            return {
                'name': continent.get('name'),
                'code': continent.get('code'),
                'country': continent_countries
            }
        return list(map(continent_map, list(continents)))
    raise ValueError(
        'find_by value is not valid, try to search by this values: name, code')

def all_country_database():
    filter_continent_function = lambda value: value.get('type') == 'continent'
    filter_country_function =  lambda value: value.get('type') == 'country'
    continents = list(filter(filter_continent_function, countries_database))
    countries = list(filter(filter_country_function, countries_database))
    return {
        'world': countries_database[0],
        'continents': continents,
        'countries': countries
    }
