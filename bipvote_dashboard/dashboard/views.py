import os
import random
import string
from django.shortcuts import render
from django import forms
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Topic, VoteOpinion, VoiceOpinion
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import datetime

# Create the admin user
def create_admin_users():
    username = 'admin'
    password = '123456'
    user = User.objects.filter(username=username)

    if not user.exists():
        admin_user = User.objects.create_user(
            username=username, password=password)
        admin_user.is_staff = True
        admin_user.save()

    # Get all admin users
    users = User.objects.all()

    # Print the admin users
    for user in users:
        print(f"Username: {user.username}")
        print(f"Password: {user.password}")
        print("-----------------------")


# Performs a function to create an administrator user at application initialization
create_admin_users()

# Login to the vote system
@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(password)

        # Password authentication
        user = authenticate(request, username=username, password=password)

        # If the verification is successful, log in to the system
        if user is not None:
            login(request, user)
            return render(request, 'dashboard/index.html')
        else:
            # If the authentication fails, an error message is displayed
            error_message = "Invalid username or password."
            return render(request, 'dashboard/login.html', {'error_message': error_message})
    else:
        # If the request method is not post, the page is rendered directly
        return render(request, 'dashboard/login.html')

# Log out, redirect to the login page
@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# The index page, list all topics
def index(request):
    all_topics = Topic.objects.order_by('-pub_date')
    return render(request, 'dashboard/index.html', {'all_topics': all_topics})

# A form containing the data returned by VXML
class result_form(forms.Form):
    choice = forms.IntegerField(label='choice')
    key = forms.CharField(label='key', max_length=100)
    vote_or_opinion = forms.CharField(label='vote_or_opinion', max_length=100)
    opinion = forms.FileField(label="opinion", required=False)
    lang = forms.CharField(label="lang", required=True)

# save the opinion data
def save_opinion(f, file_name):
    with open("/bipvote/bipvote_dashboard/dashboard/opinion/" + file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

# Vote part
@csrf_exempt
def vote(request):
    if request.method == 'POST':
        form = result_form(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            key = form.cleaned_data['key']
            vote_or_opinion = form.cleaned_data['vote_or_opinion']
            opinion = form.cleaned_data['opinion']
            lang = form.cleaned_data['lang']

            if key == 'bipvote':
                # Get the latest topic, sorted by creation date in descending order
                latest_topic = Topic.objects.order_by('-pub_date').first()
                # The user choose to only vote
                if vote_or_opinion == '0':
                    # Store the user's voting choice in the database
                    vote_choice = VoteOpinion(
                        topic=latest_topic, vote_choice=choice, pub_date=timezone.now())
                    vote_choice.save()
                else:
                    # The user choose to only express opinion
                    if vote_or_opinion == '1':
                        opinion_file_name = "opinion" + "_" + \
                            timezone.now().strftime("%Y-%m-%d-%H-%M-%S") + random_char(16) + ".wav"
                        is_general = True
                    else:
                        opinion_file_name = "vote" + "_" + timezone.now().strftime("%Y-%m-%d-%H-%M-%S") + \
                            random_char(16) + ".wav"
                        is_general = False

                # Save the opinion file
                opinion = request.FILES['opinion']
                save_opinion(opinion, opinion_file_name)

                voice_opinion = VoiceOpinion(
                    vote_url="/opinions/" + opinion_file_name, is_general=is_general, pub_date=timezone.now())
                voice_opinion.save()

                # Vote and opinion
                if vote_or_opinion == '2':
                    item = VoteOpinion(voice_opinion=voice_opinion, topic=latest_topic,
                                    vote_choice=form.cleaned_data['choice'], pub_date=timezone.now())
                    item.save()

    return render(request, 'dashboard/ending.xml', content_type="text/xml")

def topic(request):
    return render(request, 'dashboard/topic.html')

# Create a form for the new theme
class TopicForm(forms.Form):
    topic_str = forms.CharField(label='topic_str', max_length=200)

# Create a new topic
@csrf_exempt
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = Topic()
            new_topic.topic_str = request.POST['topic_str']
            new_topic.save()
    return render(request, 'dashboard/topic.html')

# Get all topics exists
def get_all_topics(request):
    topics = Topic.objects.all()
    return render(request, 'dashboard/index.html', {'topic': topics})

# The detail page of the topic
def topic_detail(request, topic_id):
    latest_topic = Topic.objects.order_by('-pub_date').first()
    all_topics = Topic.objects.order_by('-pub_date')
    # If the current topic is not the latest one
    if (topic_id != latest_topic.id):
        context = {'pos_opinion': None, 'neg_opinion': None,
                   'latest_pos_opinion_nr': 0, 'latest_neg_opinion_nr': 0}
        # Then set the topic invalid
        return render(request, 'dashboard/invalid_vote.html', context)
    # Count the numbers of positive and negative opinions
    positive_counts = VoteOpinion.objects.filter(
        topic=topic_id, vote_choice=True).order_by('-pub_date').count()
    negative_counts = VoteOpinion.objects.filter(
        topic=topic_id, vote_choice=False).order_by('-pub_date').count()

    # Get the corresponding voive opinion
    positive_opinion = VoteOpinion.objects.exclude(voice_opinion__isnull=True).filter(
        topic=topic_id, vote_choice=True).order_by('-pub_date')[:10]
    negative_opinion = VoteOpinion.objects.exclude(voice_opinion__isnull=True).filter(
        topic=topic_id, vote_choice=False).order_by('-pub_date')[:10]

    # Get the general opinion
    general_opinion = VoiceOpinion.objects.exclude(is_general=False).order_by('-pub_date')[:10]

    context = {'pos_opinion': positive_opinion, 'neg_opinion': negative_opinion, 'latest_pos_opinion_nr': positive_counts,
               'latest_neg_opinion_nr': negative_counts, 'general_opinion': general_opinion, 'all_topics': all_topics}
    
    return render(request, 'dashboard/topic_detail.html', context)

# Collect the dtmf data from the VXML app (test)
@csrf_exempt
def collect_dtmf(request):
    if request.method == 'post':
        print('Success')
    return render(request, 'dashboard/thankyou_En.xml', content_type="application/xml")
