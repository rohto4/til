import requests as rq

r = rq.get('http://trio-ws.com/?cat=7')

print(r.headers)
print('----------')
print(r.encoding)
print('----------')
print(r.content)

