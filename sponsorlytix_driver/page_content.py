from bs4 import BeautifulSoup


async def from_soup_async(url, session):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'identity',
        'Pragma': 'no-cache',
    }
    try:
        request = await session.request(
            'GET', url, timeout=50000, headers=headers)
        page = await request.text()
        return BeautifulSoup(page, 'html.parser')
    except Exception as error:
        print(f'ERROR WITH URL {url} ----- {error}')
