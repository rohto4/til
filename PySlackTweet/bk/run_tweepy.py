from slackbot.bot import Bot
from slackbot.bot import respond_to
import tweepy
import os


@respond_to('searchTweet(.*)')
def search_tweet(message, word):
    # twitter access info
    auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
    auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)
    post_text = ''
    message.send('[' + word + ']でtweet検索するよ...')
    search_results = api.search(q=word, lang='ja', result_type='recent', count=100)
    
    # set search result
    result_dictionary = {}
    for result in search_results:
        user = result.user
        favorite_count = result.favorite_count
        tweet_link = 'https://twitter.com/' + user.screen_name + '/status/' + str(result.id)
        result_text = '\n' + user.name + '@(' + user.screen_name + ')\n' +\
                      result.text + '\n(' + str(favorite_count) + 'いいね' + tweet_link + '\n'
        result_dictionary.setdefault(result_text, result.favorite_count)
    
    if len(result_dictionary) == 0:
        message.send('ツイートが見つからないよ')
        return
    
    # get favorite desc
    loop_count = 0
    for k in sorted(result_dictionary.items(), key=lambda x: -x[1]):
        loop_count += 1
        post_text = post_text + '----------------------------------------' + k
        
        # stop to max 5tweet 
        if loop_count >= 5:
            break
    
    message.send(post_text)

def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
