'''
Created on 2019/04/04

@author: Rohto
'''
from slackbot.bot import Bot
from slackbot.bot import respond_to
from requests_oauthlib import OAuth1Session
import json
import os

def create_oauth_session():
    # セッション取得
    session = OAuth1Session(os.environ['CONSUMER_KEY'],os.environ['CONSUMER_SECRET'],\
                            os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
    print('consumer_key : ' + os.environ['CONSUMER_KEY'])
    return session

@respond_to('postTweet(.*)')
def post_tweet(message, word):
    # セッション取得
    session = create_oauth_session()
    
    tweet_url = 'https://api.twitter.com/1.1/statuses/update.json?'
    req = session.post(tweet_url, params={'status':word})
    
    # respons
    if req.status_code != 200:
        print('失敗 : %s', req.text)
        exit()
    else:
        print('投稿したよ')
    

@respond_to('searchTweet(.*)')
def search_tweet(message, search_word):
    # セッション取得
    session = create_oauth_session()
    
    search_url = 'https://api.twitter.com/1.1/search/tweets.json?'
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
        print("Error code %d" % res.status_code)
    
    tweets = json.loads(res.text)
    
    message.send('結果をjsonFileに保存しました。')
    return tweets
    

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
