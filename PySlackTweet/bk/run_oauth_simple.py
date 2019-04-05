#coding: UTF-8
from requests_oauthlib import OAuth1Session

CK = "o46La2iGb7bIn41XyXqHyYw8A"
CS = "eTeaiw1nJ71KNgH2AwU6cQkgbByk6ZLfi58FEel6ENrsNAm5gR"
AK = "773885677507321856-bypmqmScqUcCPAuEQRuhRDllEqtXXeT"
AS = "pGq6OYipTDRzRtv8QXI0cdCZ2yWkXIYNLvv91fh8Cob61"

url = 'https://api.twitter.com/1.1/statuses/update.json'
# セッション取得
session = OAuth1Session(CK, CS, AK, AS)
params = {'status':u'投稿しますよ'}

res = session.post(url, params = params)

if res.status_code == 200:
    print('ok')
else:
    print('error: %d ' % res.status_code)
