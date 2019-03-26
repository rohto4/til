import twitter

# --- Twitterへの接続 ---
CONSUMER_KEY = "r6iVfpCWyucomSZwvwNkpAErk"
CONSUMER_SECRET = "85Wh7O6l1taGCDrIPuPL6aZPbYBPJ7kj5fOl1935uk8XuB4H5b"
ACCESS_TOKEN = "773885677507321856-8WHG76HFADH6Zn2AmqS8pHdqs2b7d3k"
ACCESS_TOKEN_SECRET = "S6ckJpSOklNrVVEkBTHoUhF6JTCHxUcPvOfMgt1abk0Mh"
CK = CONSUMER_KEY
CS = CONSUMER_SECRET
AT = ACCESS_TOKEN
AS = ACCESS_TOKEN_SECRET
auth = twitter.OAuth(CK, CS, AT, AS)
# --- ---

# アクセス用インスタンスの生成
t = twitter.Twitter(auth)

# 指定のキーワードで検索した結果を出力する
apiresult = t.search.tweets(q='オンゲキ', la="ja", result_type="recent", count=100)
print(len(apiresult["statuses"]))

# twitterにメッセージを投稿する
status = "pythonからtwitterへの初投稿です"
t.statuses.update(status)
