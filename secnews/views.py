import logging
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseBadRequest

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import SecnewsItem

# Create your views here.

def index(request):
    secnews_list = SecnewsItem.objects.values('pub_date').order_by('-pub_date').distinct()[:5]
    context = {'title': '搜索安全动态', 'secnews_list': secnews_list}
    return render(request, 'secnews/index.html', context)

def date_view(request, y, m, d):
    secnews_list = SecnewsItem.objects.filter(pub_date__year=y,
                                              pub_date__month=m,
                                              pub_date__day=d).order_by('-pub_date','id')
    current_date = datetime(int(y), int(m), int(d))
    one_day = timedelta(days=1)
    url_format = '/secnews/%Y/%m/%d/'
    context = { 'title': '搜索结果',
                'secnews_list': secnews_list,
                'previous_day': datetime.strftime(current_date - one_day, url_format),
                'next_day': datetime.strftime(current_date + one_day, url_format)}
    return render(request, 'secnews/result.html', context)

def search(request):
    try:
        keyword = request.GET['q']
        search_type = request.GET['type']
    except KeyError:
        return HttpResponseBadRequest('<h1>Bad Request</h1>')

    if search_type == 'content':
        result_list = SecnewsItem.objects.filter(cn_text__icontains=keyword).order_by('-pub_date','id')
    elif search_type == 'tag':
        result_list = SecnewsItem.objects.filter(tag__icontains=keyword).order_by('-pub_date','id')
    else:
        return HttpResponseBadRequest('<h1>Bad Request</h1>')

    paginator = Paginator(result_list, 25)
    page = request.GET.get('page')
    try:
        secnews_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        secnews_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        secnews_list = paginator.page(paginator.num_pages)

    context = { 'title': '搜索结果',
                'type': search_type,
                'secnews_list': secnews_list,
                'keyword': keyword}
    return render(request, 'secnews/result.html', context)
