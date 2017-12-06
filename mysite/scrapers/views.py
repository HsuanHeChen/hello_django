import json, requests, re, random
from django.shortcuts import render
from dateutil.parser import parse
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup

from .forms import *

# Create your views here.

ACCESS_TOKEN = 'EAAZAZCjZBTehLsBAKzXAVZAj6ljo9BwvpkA83uWZBPOdKJ8jPpv9oL8N8QOey4ZAjSHRIHuWUhuQNg4Ii4OQDTaC5hrY3xFjoA2Jlg5LDFQGNZCCZB2bZC1jJ2YzqAuV8HRTW4KgKbIZCzmsKLVyzlQfmolZB0ZA4l1l59UZD'
VERIFY_TOKEN = "323"


def ecapp24(request):

    fanpages = {'112520726085483': '電商小幫',
                '10209804804028445': 'HsuanHe Chen'}

    information_list = []

    # part1: use requests
    # get posts with GraphApi
    for fanpage in fanpages:
        res = requests.get('https://graph.facebook.com/v2.11/{}/feed?limit=20&access_token={}'.format(fanpage, ACCESS_TOKEN))

        for information in res.json()['data']:
            if 'message' in information:

                res2 = requests.get('https://graph.facebook.com/v2.11/{}?fields=likes.limit(0).summary(True), shares&access_token={}'.format(information['id'], ACCESS_TOKEN))

                if 'likes' in res2.json():
                    likes = res2.json()['likes']['summary'].get('total_count')
                else:
                    likes = 0

                if 'shares' in res2.json():
                    shares = res2.json()['shares'].get('count')
                else:
                    shares = 0

                information_list.append({'id': information['id'],
                                         'author': fanpages[fanpage],
                                         'message': information['message'],
                                         'story': information['story'] if 'story' in information else '',
                                         'likes': likes,
                                         'shares': shares,
                                         'created_time': parse(information['created_time']).date()})

    return render(request, 'scrapers/ecapp24.html', {'data': information_list})


# Helper function
def post_fb_message(fbid, recevied_message):

    # get_token
    res = requests.get('https://graph.facebook.com/v2.11/me/accounts?access_token={}'.format(ACCESS_TOKEN))
    token = ''
    for ele in res.json()['data']:
        if ele['name'] == 'Momomolaimochi':
            token = ele['access_token']
            break

    # Remove all punctuations, lower case the text and split it based on space
    # tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()

    # user_details_url = "https://graph.facebook.com/v2.11/{}".format(fbid)
    # user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': token}
    # user_details = requests.get(user_details_url, user_details_params).json()
    # joke_text = 'Meow, {} {}.'.format(user_details['first_name'], user_details['last_name'])

    joke_text = random.choice(['Meow', 'Meow Meow', 'Meow Meow Meow','Meeeeeeow', 'meoooOW', 'MEOW'])

    post_message_url = 'https://graph.facebook.com/v2.11/me/messages?access_token={}'.format(token)
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    # print(status.json())
    print('=================Response message===================\n')


class PageWebHookView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        print('==================New message===================\n')
        print(incoming_message)
        print('\n')

        for entry in incoming_message['entry']:

            if 'messaging' not in entry:
                return HttpResponse('Error, no messaging.')
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    if 'text' in message['message']:
                      post_fb_message(message['sender']['id'], message['message']['text'])
                    elif 'attachments' in message['message']:
                      post_fb_message(message['sender']['id'], message['message']['attachments'])
        return HttpResponse()


class TaiwanLotteryView(generic.View):
    def get(self, request, *args, **kwargs):
        form = LotteryForm()
        return render(request, 'scrapers/lottery.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LotteryForm(request.POST)
        ball_greens = []
        ball_red = 0
        text = ''
        if form.is_valid():
            url = 'http://www.taiwanlottery.com.tw/'
            html = requests.get(url)
            sp = BeautifulSoup(html.text, 'html.parser')

            for element in sp.select('.contents_box02'):
                # only get contents_logo_02 data
                target = element.select('#contents_logo_02')
                if target:
                    ball_green = element.select('.ball_tx.ball_green')
                    ball_red = int(element.select('.ball_red')[0].text)
                    for ball in ball_green:
                        ball_greens.append(int(ball.text))

            ball_greens = sorted(set(ball_greens))
            get_green_num = 0
            get_red_num = 0
            params = request.POST
            text = 'ERROR, NO BALLS.'
            if ball_greens and ball_red:
                for field in ['no1', 'no2', 'no3', 'no4', 'no5', 'no6']:
                    if int(params[field]) in ball_greens:
                        get_green_num += 1
                if int(params['no7']) == ball_red:
                    get_red_num = 1

                if get_green_num == 6 and get_red_num == 1:
                    win_title = '頭獎'
                elif get_green_num == 6 and get_red_num == 0:
                    win_title = '貳獎'
                elif get_green_num == 5 and get_red_num == 1:
                    win_title = '參獎'
                elif get_green_num == 5 and get_red_num == 0:
                    win_title = '肆獎'
                elif get_green_num == 4 and get_red_num == 1:
                    win_title = '伍獎'
                elif get_green_num == 4 and get_red_num == 0:
                    win_title = '陸獎'
                elif get_green_num == 3 and get_red_num == 1:
                    win_title = '柒獎'
                elif get_green_num == 2 and get_red_num == 1:
                    win_title = '捌獎'
                elif get_green_num == 3 and get_red_num == 0:
                    win_title = '玖獎'
                elif get_green_num == 1 and get_red_num == 1:
                    win_title = '普獎'
                else:
                    win_title = 'nothing'

                text = 'You won the {}.'.format(win_title)

        return render(request,
                      'scrapers/lottery.html',
                      {'form': form,
                       'ball_greens': ball_greens,
                       'ball_red': ball_red,
                       'text': text})
