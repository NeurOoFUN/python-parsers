from fake_useragent import UserAgent
import requests

url = 'http://rocknation.su/mp3/band-32/1'

session = requests.Session()
session.headers = {
    'user-agent': f'{UserAgent().random}',
    'accept': '*/*'
}
