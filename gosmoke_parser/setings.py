from fake_useragent import UserAgent

headers = {
    'user-agent': f'{UserAgent().random}',
    'accept': '*/*'
}

csv_headers = (
    'lot_link',
    'lot_name',
    'description',
    'volume / amount',
    'price',
    'img_link',
    'presence'
)
