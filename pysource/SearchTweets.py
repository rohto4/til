from requests_oauthlib import OAuth1Session
import json
import datetime
import time
import sys

CONSUMER_KEY = "r6iVfpCWyucomSZwvwNkpAErk"
CONSUMER_SECRET = "85Wh7O6l1taGCDrIPuPL6aZPbYBPJ7kj5fOl1935uk8XuB4H5b"
ACCESS_TOKEN = "773885677507321856-8WHG76HFADH6Zn2AmqS8pHdqs2b7d3k"
ACCESS_TOKEN_SECRET = "S6ckJpSOklNrVVEkBTHoUhF6JTCHxUcPvOfMgt1abk0Mh"
CK = CONSUMER_KEY
CS = CONSUMER_SECRET
AT = ACCESS_TOKEN
AS = ACCESS_TOKEN_SECRET

session = OAuth1Session(CK, CS, AT, AS)

url = 'https://api.twitter.com/1.1/search/tweets.json'
res = session.get(url, params={'q' : u'オンゲキ', 'count' : 100})

# ステータスコードの確認
if res.status_code != 200:
    print("Twitter API Error: %d" % res.status_code)
    sys.exit(1)

# ヘッダー部出力
print('アクセス可能回数 : %s' % res.headers['X-Rate-Limit-Remaining'])
print('リセット時間     : %s' % res.headers['X-Rate-Limit-Reset'])
sec = int(res.headers['X-Rate-Limit-Reset'])\
      - time.mktime(datetime.datetime.now().timetuple())
print('リセット時間     : %s' % sec)

# テキスト部出力
res_text = json.loads(res.text)
for tweet in res_text['statuses']:
    print('-----')
    print(tweet['created_at'])
    print(tweet['text'])


