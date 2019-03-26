from requests_oauthlib import OAuth1Session
import sys

CK = "r6iVfpCWyucomSZwvwNkpAErk"
CS = "85Wh7O6l1taGCDrIPuPL6aZPbYBPJ7kj5fOl1935uk8XuB4H5b"
AT = "773885677507321856-8WHG76HFADH6Zn2AmqS8pHdqs2b7d3k"
AS = "S6ckJpSOklNrVVEkBTHoUhF6JTCHxUcPvOfMgt1abk0Mh"

session = OAuth1Session(CK, CS, AT, AS)

url = 'https://api.twitter.com/1.1/statuses/update.json'
res = session.post(url, params={'status':u'TwitterAPIを使用して投稿します'})

if res.status_code != 200:
    print("Twitter API Error: %d" % res.status_code)
    sys.exit(1)
