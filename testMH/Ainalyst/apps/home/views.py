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

START_DATE = date.today() - timedelta(days=30)
END_DATE = date.today()


@login_required(login_url="/login/")
def index(request):
    report_list = Report.objects.order_by('-create_date', '-id')
    new_report = report_list.filter(create_date='2022-07-28')
    pos_Q = Q(opinion='Buy') | Q(opinion='StrongBuy') | Q(opinion='매수') | Q(opinion='강력매수')
    positive_reports = report_list.filter(pos_Q)
    negative_reports = report_list.filter(~pos_Q)
    new_positive = positive_reports.filter(create_date__range=[START_DATE, END_DATE])
    new_negative = negative_reports.filter(create_date__range=[START_DATE, END_DATE])
    hot_topic = Counter([report.company for report in new_report]).most_common()

    # Variable for graph
    # 1년치 데이터 선택, range: 2021-08.01 ~ 2022-08-09
    start, end = (date.today() - timedelta(days=365)).replace(day=1), date.today()
    last_year_pos_reports = Report.objects.filter(Q(create_date__range=[start, end]) & pos_Q).values('create_date')\
                                          .annotate(counts=Count('create_date'))
    last_year_neg_reports = Report.objects.filter(Q(create_date__range=[start, end]) & (~pos_Q)).values('create_date')\
                                          .annotate(counts=Count('create_date'))

    #  [{create_date: 날짜, counts: 해당 날짜에 올라온 리포트 수 }]
    counts = set(map(lambda day: day['create_date'].strftime("%Y-%m"), last_year_pos_reports))
    months = sorted(list(counts))
    dict_counts = {'positive': {count: 0 for count in counts}, 'negative': {count: 0 for count in counts}}

    for report in last_year_pos_reports:
        dict_counts['positive'][report['create_date'].strftime("%Y-%m")] += report['counts']
    for report in last_year_neg_reports:
        dict_counts['negative'][report['create_date'].strftime("%Y-%m")] += report['counts']

    pos_counts = [count for _, count in sorted(dict_counts['positive'].items())]
    neg_counts = [count for _, count in sorted(dict_counts['negative'].items())]

    context = {'segment': 'index',
               'total_num_report': len(report_list),
               'total_num_positive': len(positive_reports),
               'total_num_negative': len(negative_reports),
               'new_reports': len(new_report),
               'new_positive': len(new_positive),
               'new_negative': len(new_negative),
               'hot_topic': hot_topic[:3],
               'months': months,
               'pos_counts': pos_counts,
               'neg_counts': neg_counts,
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


# # printout Report list
# def report(request):
#     reportdb = PostgresDB()
#     report_list = reportdb.execute(f"SELECT * FROM home_report ORDER BY create_date DESC;")
#     print(report_list)
#     # report_list = Report.objects.order_by('-create_date')
#     context = {'report_list': report_list}
#     html_template = loader.get_template('home/report_list.html')
#     return HttpResponse(html_template.render(context, request))