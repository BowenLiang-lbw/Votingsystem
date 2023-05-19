import argparse
import requests
import numpy as np

def sendVoteAndOpinion(vote):
    files = {'opinion': open('example.wav', 'rb')}
    data = {'key': 'bipvote', 'vote_or_opinion': '2', 'choice': vote, 'lang': 'En'}
    r = requests.post('http://127.0.0.1:8000/vote/', files=files, data=data)
    print(data)

def sendVote(vote):
    data = {'key': 'bipvote', 'vote_or_opinion': '0', 'choice': vote, 'lang': 'En'}
    r = requests.post('http://127.0.0.1:8000/vote/', data=data)
    print(data)

def sendOpinion():
    files = {'opinion': open('example.wav', 'rb')}
    print('File open ok!')
    data = {'key': 'bipvote', 'vote_or_opinion': '1', 'choice':'1', 'lang': 'En'}
    r = requests.post('http://127.0.0.1:8000/vote/', files=files, data=data)
    print(data)

def sendMultiple(r, t, vote):
    choices = ['1', '0']
    for i in range(r):
        if t == 0:
            sendVote(vote)
        elif t == 1:
            sendOpinion()
        elif t == 2:
            sendVoteAndOpinion(vote)

if __name__ == '__main__':
    r = 10  # 重复次数
    t = 0  # 动作类型: 0表示投票，1表示意见，2表示投票和意见
    c = 1  # 选择: 0表示"no"，1表示"yes"

    sendMultiple(r, t, c)
    sendMultiple(5, 0, 0)

