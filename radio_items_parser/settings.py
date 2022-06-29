from fake_useragent import UserAgent

# Your path to chromedriver.
CHROME_DRIVER_PATH = \
    '/home/neuroo/projects/python-parsers/radio_items_parser/chromedriver'

url = 'http://japanparcel.com/catalogv2/Audio__video_equipment/Amplifiers?=&n=100&min=&max=&scroll=1&pg=2'

headers = {
    'user-agent': f'{UserAgent()}',
    'accept': '*/*'
}
