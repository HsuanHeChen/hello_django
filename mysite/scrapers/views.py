from django.shortcuts import render
import requests
from dateutil.parser import parse
# Create your views here.


def ecapp24(request):

    token = 'EAACEdEose0cBAI7A01Uk9flZAHm1FwH4tK2TJG52wSwkEQvXSnwOWZC2aPPUHvIFXIufktma1pb5LsHKNBViTr7vTzrbXO4S4Ksr9JDRtlSBFDpLqyUkLWmlLn1BSpGR5DVpUMlbrjypzJSmSacXEAR2R3ZAnP5DlK00gSOp45HRt3qxoDCTxGCe5ZCZAznSdyd2ZBHzfGVwZDZD'

    fanpages = {'112520726085483': '電商小幫',
                '10202525865139522': 'HsuanHe Chen'}

    information_list = []

    # part1: use requests
    # get posts with GraphApi
    for fanpage in fanpages:
        res = requests.get('https://graph.facebook.com/v2.11/{}/feed?limit=10&access_token={}'.format(fanpage, token))

        for information in res.json()['data']:
            if 'message' in information:

                res2 = requests.get('https://graph.facebook.com/v2.11/{}?fields=likes.limit(0).summary(True), shares&access_token={}'.format(information['id'], token))

                if 'likes' in res2.json():
                    likes = res2.json()['likes']['summary'].get('total_count')
                else:
                    likes = 0

                if 'shares' in res2.json():
                    shares = res2.json()['shares'].get('count')
                else:
                    shares = 0

                information_list.append({'author': fanpages[fanpage],
                                         'message': information['message'],
                                         'story': information['story'] if 'story' in information else '',
                                         'likes': likes,
                                         'shares': shares,
                                         'created_time': parse(information['created_time']).date()})

    return render(request, 'scrapers/ecapp24.html', {'data': information_list})
