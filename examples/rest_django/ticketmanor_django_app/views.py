from django.http.response import Http404
from django.http import HttpResponse, JsonResponse
from .models import Question

def get_user(request, email):
    # user_list = Person.objects.get(email=email)
    user_list = Question.objects.filter(question_text__startswith=email)
    if not user_list:
        raise Http404("User '{}' is not in the database".format(email))
    user = user_list[0]
    user = {
        "first_name": "Miles",
        "last_name": "Davis",
        "email": email,
    }
    return JsonResponse(user)

def add_user(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([p.question_text for p in latest_question_list])
    return HttpResponse(output)
    # return HttpResponse("add_user()")

def get_news(request, news_type):
    news = { "news_type": news_type,
   "news_items": [
     { "title": "The Othello of Soul Music - Wall Street Journal",
       "date_time": "Fri, 29 May 2015 18:14:00 GMT",
       "image_url": "https://t0.gstatic.com/images?q=tbn:...",
       "content": "Otis Redding is the Othello of soul music..." } ] }
    return JsonResponse(news)

