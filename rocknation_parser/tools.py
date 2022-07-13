from faker import Faker
import requests

# this request sessin.
session = requests.Session()
# fake user-agent
f = Faker()

agent = f.firefox()
session.headers = {
    'user-agent': agent,
    'accept': '*/*'
}
