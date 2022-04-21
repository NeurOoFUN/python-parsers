from fake_useragent import UserAgent

headers = {
    'user-agent': f'{UserAgent().random}',
    'accept': '*/*'
}
