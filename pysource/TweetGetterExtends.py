from tinydb import TinyDB, Query
from requests_oauthlib import OAuth1Session
import json
import datetime, time, sys
from abc import ABCMeta, abstractmethod

CK = "r6iVfpCWyucomSZwvwNkpAErk"
CS = "85Wh7O6l1taGCDrIPuPL6aZPbYBPJ7kj5fOl1935uk8XuB4H5b"
AT = "773885677507321856-8WHG76HFADH6Zn2AmqS8pHdqs2b7d3k"
AS = "S6ckJpSOklNrVVEkBTHoUhF6JTCHxUcPvOfMgt1abk0Mh"

class TweetsGetterExtends(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.session = OAuth1Session(CK, CS, AT, AS)

    @abstractmethod
    def specifyUrlAndParams(self, keyword):
        '''
        :param keyword:
        :return:呼び出し先 URL, パラメータ
        '''

    @abstractmethod
    def pickupTweet(self, res_text, includeRetweet):
        '''
        :param res_text: json.loads(res.text)を設定
        :param includeRetweet: 不明
        '''

    @abstractmethod
    def getLimitContext(self, res_text):
        '''
        :param res_text:
        :return: 回数制限の情報（起動時）
        '''

    def collect(self, total = -1, onlyText = False, includeRetweet = False):
        '''
        ツイート取得を開始する
        '''

        # ----------------
        # 回数制限を確認
        # ----------------
        self.checkLimit()

        #----------------
        # URL、パラメータ
        #----------------
        url, params = self.specifyUrlAndParams()
        params['include_rts'] = str(includeRetweet).lower()
        # include_rts は statuses/user_timeline のパラメータ。search/tweets には無効

        #----------------
        # ツイート取得
        #----------------
        cnt = 0
        unavailableCnt = 0
        while True:
            res = self.session.get(url, params = params)
            if res.status_code == 503:
                # 503 : Service Unavailable
                if unavailableCnt > 10:
                    raise Exception('Twitter API error %d' % res.status_code)
                unavailableCnt += 1
                print ('Service Unavailable 503')
                self.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
                continue

            unavailableCnt = 0

            if res.status_code != 200:
                raise Exception('Twitter API error %d' % res.status_code)

            tweets = self.pickupTweet(json.loads(res.text))
            if len(tweets) == 0:
                # len(tweets) != params['count'] としたいが
                # count は最大値らしいので判定に使えない。
                # ⇒  "== 0" にする
                # https://dev.twitter.com/discussions/7513
                break

            for tweet in tweets:
                if(('retweeted_status' in tweet) and (includeRetweet is False)):
                    pass
                else:
                    if onlyText is True:
                        yield tweet['text']
                    else:
                        yield tweet

                    cnt += 1
                    if cnt % 100 == 0:
                        print('%d件 ' % cnt)

                    if total > 0 and cnt >= total:
                        return

            params['max_id'] = tweet['id'] - 1

            # ヘッダ確認 （回数制限）
            # X-Rate-Limit-Remaining が入ってないことが稀にあるのでチェック
            if('X-Rate-Limit-Remaining' in res.headers and 'X-Rate-Limit-Reset' in res.headers):
                if (int(res.headers['X-Rate-Limit-Remaining']) == 0):
                    self.waitUntilReset(int(res.headers['X-Rate-Limit-Reset']))
                    self.checkLimit()

            else:
                print('not found  -  X-Rate-Limit-Remaining or X-Rate-Limit-Reset')
                self.checkLimit()

    def checkLimit(self):
        '''
        回数制限を問合せ、アクセス可能になるまで wait する
        '''
        unavailableCnt = 0
        while True:
            url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
            res = self.session.get(url)

            if res.status_code == 503:
                if unavailableCnt > 10:
                    raise Exception('Twitter API error %d' % res.status_code)

                unavailableCnt += 1
                print ('Service Unavailable 503')
                self.waitUntilReset(time.mktime(datetime.datetime.now().timetuple())) + 30
                continue

            unavailableCnt = 0

            if res.status_code != 200:
                raise Exception('Twitter API error %d' % res.status_code)

            remaining, reset = self.getLimitContext(json.loads(res.text))
            if (remaining == 0):
                self.waitUntilReset(reset)
            else:
                break

    def waitUntilReset(self, reset):
        '''
        reset 時刻まで sleep
        '''
        seconds = reset - time.mktime(datetime.datetime.now().timetuple())
        seconds = max(seconds, 0)
        print('\n     =====================')
        print('     == waiting %d sec ==' % seconds)
        print('     =====================')
        sys.stdout.flush()
        time.sleep(seconds + 10)

    @staticmethod
    def bySearch(keyword):
        return TweetsGetterBySearch(keyword)

    @staticmethod
    def byUser(screen_name):
        return TweetsGetterByUser(screen_name)


class TweetsGetterBySearch(TweetsGetterExtends):
    '''
    キーワードでツイートを検索
    '''
    def __init__(self, keyword):
        super(TweetsGetterBySearch, self).__init__()
        self.keyword = keyword

    def specifyUrlAndParams(self):
        '''
        呼出し先 URL、パラメータを返す
        '''
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        params = {'q':self.keyword, 'count':100}
        return url, params

    def pickupTweet(self, res_text):
        '''
        res_text からツイートを取り出し、配列にセットして返却
        '''
        results = []
        for tweet in res_text['statuses']:
            results.append(tweet)

        return results

    def getLimitContext(self, res_text):
        '''
        回数制限の情報を取得 （起動時）
        '''
        remaining = res_text['resources']['search']['/search/tweets']['remaining']
        reset     = res_text['resources']['search']['/search/tweets']['reset']

        return int(remaining), int(reset)

# ------------------------------------------------
# -------------------- 未使用 --------------------
class TweetsGetterByUser(TweetsGetterExtends):
    '''
    ユーザーを指定してツイートを取得
    '''
    def __init__(self, screen_name):
        super(TweetsGetterByUser, self).__init__()
        self.screen_name = screen_name

    def specifyUrlAndParams(self):
        '''
        呼出し先 URL、パラメータを返す
        '''
        url = 'https://api.twitter.com/1.1/search/user_timeline.json'
        params = {'screen_name':self.screen_name, 'count':200}
        return url, params

    def pickupTweet(self, res_text):
        '''
        res_text からツイートを取り出し、配列にセットして返却
        '''
        results = []
        for tweet in res_text:
            results.append(tweet)

        return results

    def getLimitContext(self, res_text):
        '''
        回数制限の情報を取得 （起動時）
        '''
        remaining = res_text['resources']['statuses']['/search/user_timeline']['remaining']
        reset     = res_text['resources']['statuses']['/search/user_timeline']['reset']

        return int(remaining), int(reset)
# -------------------- 未使用 --------------------
# ------------------------------------------------

# メイン関数
if __name__ == '__main__':
    '''
    キーワードを指定して検索結果を取得
    '''
    getter = TweetsGetterExtends.bySearch(u'オンゲキ')

    '''
    ユーザを指定して取得
    '''
    # getter = TweetsGetter.byUser(u'pikoyama')

    # 最新のindexを取得
    # 別モジュール化 //TODO
    db = TinyDB('ongeki.json')
    tbl = db.table('search_ongeki')

    # 最後に追加された行のindexを取得
    que = Query()
    # 初期化
    index_cnt = 0
    cnt_res = tbl.search(que.last_insert_flg == '1')
    if cnt_res.last_insert_flg == '1':
        index_cnt = cnt_res.index

    for tweet in getter.collect(total=100):
        index_cnt += 1
        print('----- %d' % index_cnt)
        print('{} {} {}'.format(tweet['id'], tweet['created_at'], '@'+tweet['user']['screen_name']))
        print(tweet['text'])

    '''
    連想配列に一時格納
    '''

    '''
    検索ワードと紐づいたテーブルがないことを確認
    '''
    table_ck = False
    if table_ck == True:
        # 新しくTBLを作成
        print('新しくTBLを作成')
    else:
        # 既存のTBLに追記
        print('既存のTBLに追記')

    '''
    データをTBLに書き込み
    '''

    '''
    データの件数をdata.jsonに書き込み
    '''

    '''
    件数が一定以上であれば、Tikenizerを実行
    '''


    '''
    実行結果を基にxlsxファイルを作成
    '''



