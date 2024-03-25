from django.shortcuts import render, redirect, get_object_or_404 # for handling HTTP requests, redirecting, and retrieving objects while handling HTTP 404 errors gracefully.
from datetime import timedelta, date



from .models import *



def history(request): # takes an HTTP request object as its argument.
    acct = CustomUser.objects.filter(id = request.user.id) # retrieves the current user's record from the CustomUser model using their id.
    sorting_params = {
        'normal': 'id',
        'newest': '-id',
        'atoz': '-title'
    }
    sorting_param = next((param for param in sorting_params.keys() if param in request.GET), None) # It checks if the current request's query parameters (request.GET) include any of the sorting options defined in sorting_params. If found, it applies this sorting to the query that retrieves chat records.
    
    if sorting_param:
        questions = Chat.objects.filter(user=request.user.id).order_by(sorting_params[sorting_param])
    else:
        questions = Chat.objects.filter(user =  request.user.id)

    t_ques = questions.filter(created_at=date.today())
    y_ques = questions.filter(created_at=date.today() - timedelta(days=1))
    early_ques = questions.filter(created_at__lte=date.today() - timedelta(days=1), created_at__gte=date.today() - timedelta(days=6))
    s_ques = questions.filter(created_at=date.today() - timedelta(days=7))
    more_s_ques = questions.filter(created_at__lte=date.today() - timedelta(days=8))
        


    return {'t_ques':t_ques, 'y_ques':y_ques, 's_ques':s_ques, 'more_s_ques':more_s_ques, 'early_ques':early_ques, 'ques':questions, 'acct':acct}





