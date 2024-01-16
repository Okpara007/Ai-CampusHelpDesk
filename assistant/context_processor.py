from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta, date



from .models import *



def history(request):
    today = date.today()
    yesday = date.today() - timedelta(days=1)
    seven_days_ago = date.today() - timedelta(days=7)
    eight_days_ago = date.today() - timedelta(days=8)
    
    questions = Chat.objects.filter(user=request.user.id)
    t_ques = questions.filter(created_at=today).order_by('-id')
    y_ques = questions.filter(created_at=yesday).order_by('-id')
    early_ques = questions.filter(created_at__gte=seven_days_ago, created_at__lte=yesday).order_by('-id')
    s_ques = questions.filter(created_at=seven_days_ago).order_by('-id')
    more_s_ques = questions.filter(created_at__gte=eight_days_ago, created_at__lte=seven_days_ago).order_by('-id')


    return {'t_ques':t_ques, 'y_ques':y_ques, 's_ques':s_ques, 'more_s_ques':more_s_ques, 'early_ques':early_ques}





