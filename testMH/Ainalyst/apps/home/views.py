# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Report
from datetime import timedelta, date
from collections import Counter


@login_required(login_url="/login/")
def index(request):
    pos_Q, neg_Q = Q(new_opinion='매수'), Q(new_opinion='매도')    # 매수 / 매도 report 선택을 위한 QuerySet
    start, end = date.today() - timedelta(days=30), date.today()    # 한달간 데이터 선택을 위한 Variable

    report_list = Report.objects.order_by('-create_date', '-id')
    new_report = report_list.filter(create_date='2022-07-28')
    positive_reports = report_list.filter(pos_Q)
    negative_reports = report_list.filter(neg_Q)
    new_positive = positive_reports.filter(create_date__range=[start, end])
    new_negative = negative_reports.filter(create_date__range=[start, end])
    hot_topic = Counter([report.company for report in report_list.filter(create_date__range=[start, end])]).most_common()

    # Variable for graph
    # 1년치 데이터 선택, range: 2021-08.01 ~ 2022-08-09
    start, end = (date.today() - timedelta(days=365)).replace(day=1), date.today()

    #  결과: [{create_date: 날짜, counts: 해당 날짜에 올라온 리포트 수 }]
    recent_positive = Report.objects.filter(Q(create_date__range=[start, end]) & pos_Q)\
                                    .values('create_date')\
                                    .annotate(counts=Count('create_date'))
    recent_negative = Report.objects.filter(Q(create_date__range=[start, end]) & neg_Q)\
                                    .values('create_date')\
                                    .annotate(counts=Count('create_date'))

    # years: 2022-07, 2022-06, 2022-05, ... 2021-08로 나눠진 월별 데이터를 정렬된 형태로 저장
    years = sorted(list(set(map(lambda day: day['create_date'].strftime("%Y-%m"), recent_positive))))
    dict_years = {'positive': {month: 0 for month in years}, 'negative': {month: 0 for month in years}}

    # 작성 날짜에 해당하는 달에 누적합 => 월별 리포트 수가 나옴
    for report in recent_positive:
        dict_years['positive'][report['create_date'].strftime("%Y-%m")] += report['counts']
    for report in recent_negative:
        dict_years['negative'][report['create_date'].strftime("%Y-%m")] += report['counts']

    # 월별 긍정 리포트 수, 부정 리포트 수만 list에 저장 - graph 출력용
    pos_counts = [count for _, count in sorted(dict_years['positive'].items())]
    neg_counts = [count for _, count in sorted(dict_years['negative'].items())]

    context = {'segment': 'index',
               'total_num_report': len(report_list),    # DB에 저장된 전체 리포트 수
               'total_num_positive': len(positive_reports),    # 전체 긍정 리포트 수
               'total_num_negative': len(negative_reports),    # 전체 부정 리포트 수
               'new_reports': len(new_report),    # 당일 올라온 새 리포트 수
               'new_positive': len(new_positive),    # 최근 한달 긍정 리포트 수
               'new_negative': len(new_negative),    # 최근 한달 부정 리포트 수
               'hot_topic': hot_topic[:3],    # 오늘 올라온 리포트 중 수가 가장 많은 것 Top 3
               'years': years,    # Graph에 나타낼 최근 1년의 기간을 월별로 나눈 것
               'pos_counts': pos_counts,    # 최근 1년간 월별 긍정 리포트 수
               'neg_counts': neg_counts,    # 최근 1년간 월별 부정 리포트 수
               }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def tables(request):
    report_list = Report.objects.order_by('-create_date', '-id')
    page = request.GET.get('page', '1')
    paginator = Paginator(report_list, 10)
    page_obj = paginator.get_page(page)
    context = {'segment': 'index',
               'reports': page_obj,
               }
    html_template = loader.get_template('home/tables.html')
    return HttpResponse(html_template.render(context, request))


def tables_detail(request, report_id):
    report = Report.objects.get(id=report_id)
    context = {'segment': 'index',
               'report': report,
               }
    html_template = loader.get_template('home/tables_detail.html')
    return HttpResponse(html_template.render(context, request))


def profile(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
