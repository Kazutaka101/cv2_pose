import requests

url = 'http://ipcheck.ieserver.net/'
res = requests.get('http://inet-ip.info/ip')

print(str(res.text))