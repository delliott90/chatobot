from django.shortcuts import render
from django.http import HttpResponse
from .bot import Bot

THE_BOT = Bot()

def index(request):
    query = ""
    if request.method == 'POST':
        query = request.POST.get('myinput')
    if not query:
        bot_response = ""
    else:
        bot_response = THE_BOT.query_bot(query)
    context = {'bot_response': bot_response}
    return render(request, 'chatwithapp/index.html', context)

def detail(request):
    if request.method == 'POST':
        train_tup = request.POST.get('traininput', "")
    else: 
        train_tup = "one:two"
    # bot_response = THE_BOT.train_bot(train_tup)
    bot_response = THE_BOT.train_bot_with_corpus()
    context = {'bot_response': bot_response}
    return render(request, 'chatwithapp/detail.html', context)



