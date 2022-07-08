from fake_useragent import UserAgent

url = 'http://rocknation.su/mp3/band-32/1'

headers = {
    'user-agent': f'{UserAgent().random}',
    'accept': '*/*'
}
