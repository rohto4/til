'''
Created on 2019/04/04

@author: Rohto
'''
from slackbot.bot import Bot
from slackbot.bot import respond_to
from requests_oauthlib import OAuth1Session
import json
import os
import collections as cl

def create_oauth_session():
    # セッション取得
    session = OAuth1Session(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'],\
                            os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
    return session

@respond_to('postTweet(.*)')
def post_tweet(message, post_word):
    # ポスト用URL
    post_url = 'https://api.twitter.com/1.1/statuses/update.json'
    # セッション取得
    session = create_oauth_session()
    params = {'status':post_word}
    
    res = session.post(post_url, params = params)
    
    # respons
    if res.status_code == 200:
        print('投稿したよ')
    else:
        print('error: %d ' % res.status_code)
    

@respond_to('searchTweet(.*)')
def search_tweet(message, search_word):
    # サーチ用URL
    search_url = 'https://api.twitter.com/1.1/search/tweets.json'
    # セッション取得
    session = create_oauth_session()
    params = {
        "q": search_word,
        "lang": "ja",
        "result_type": "recent",
        "count": "15"
    }
    
    # 検索リクエスト
    message.send('[' + search_word + ']でtweet検索するよ...')
    res = session.get(search_url, params=params)
    
    if res.status_code != 200:
        # 失敗
        print("Error code %d" % res.status_code)
    else:
        # 成功
        timeline = json.loads(res.text)
        statuses = timeline['statuses']
        
        for each in timeline['statuses']:
            print('--------------------')
            print(each['text'])
    
    message.send('結果の出力が完了しました。')
#    message.send('結果をjsonFileに保存しました。')

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
