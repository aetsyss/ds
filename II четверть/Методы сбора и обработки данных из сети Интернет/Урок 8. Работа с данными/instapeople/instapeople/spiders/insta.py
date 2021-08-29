import scrapy
from scrapy.http import HtmlResponse
import re
import json
from instapeople.items import InstapeopleItem
from urllib.parse import urlencode
from copy import deepcopy

class InstaSpider(scrapy.Spider):
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']

    insta_login = 'aetsyss'
    insta_pass = '#PWD_INSTAGRAM_BROWSER:10:1630247314:AUpQAMvS7sFbEZMym7uZXSiZGIU/bTxfrwOG46v76fAkNXIU7vzwuhC4n8JPN6Ei/meEHTXd1rYAI0dFdkS3C+zdxqyY7Ac21g/w67dAU/KU+4oN8dEdeuk+VNSn1q3LcJPsV2AP8UAbPjYtydFHem0='

    insta_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    accounts = ['aetsyss', 'lkirillove']

    api_url = 'https://i.instagram.com/api/v1/'

    def parse(self, response):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.insta_login_link,
                                 method='POST',
                                 callback=self.user_login,
                                 formdata={'username': self.insta_login,
                                           'enc_password': self.insta_pass},
                                 headers={'X-CSRFToken': csrf})

    def user_login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body['authenticated']:
            for account in self.accounts:
                yield response.follow(f'/{account}',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'account': account})

    def user_data_parse(self, response: HtmlResponse, account):
        account_id = self.fetch_user_id(response.text, account)
        params = {
            'count': 12
        }

        # Followers
        url_followers = f'{self.api_url}friendships/{account_id}/followers/?{urlencode(params)}'

        yield response.follow(url_followers, callback=self.user_friendships_parse, cb_kwargs={
            'type': 'followers',
            'account_id': account_id,
            'params': deepcopy(params)
        })

        # Following
        url_following = f'{self.api_url}friendships/{account_id}/following/?{urlencode(params)}'

        yield response.follow(url_following, callback=self.user_friendships_parse, cb_kwargs={
            'type': 'following',
            'account_id': account_id,
            'params': deepcopy(params)
        })

    def user_friendships_parse(self, response: HtmlResponse, type, account_id, params):
        if response.status == 200:
            j_data = response.json()

            if 'next_max_id' in j_data:
                params['max_id'] = j_data['next_max_id']
                url_followers = f'{self.api_url}friendships/{account_id}/{type}/?{urlencode(params)}'

                yield response.follow(url_followers, callback=self.user_friendships_parse, cb_kwargs={
                    'type': type,
                    'account_id': account_id,
                    'params': deepcopy(params)
                })

            users = j_data['users']
            for user in users:
                yield InstapeopleItem(account_id=account_id,
                                      type=type,
                                      id=user['pk'],
                                      name=user['username'],
                                      full_name=user['full_name'],
                                      photo=user['profile_pic_url'])

    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')