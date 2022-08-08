# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Report
from datetime import datetime, timedelta
from collections import Counter


def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    return dates


@login_required(login_url="/login/")
def index(request):
    report_list = Report.objects.order_by('-create_date')
    new_report = len([report for report in report_list if str(report.create_date) == '2022-07-28']) # str(date.today().strftime("%Y-%m-%d"))
    positive_report = Report.objects.filter(Q(opinion='Buy') |
                                            Q(opinion='StrongBuy') |
                                            Q(opinion='매수') |
                                            Q(opinion='강력매수'))
    negative_report = [report for report in report_list if report.opinion not in ['Buy', 'StrongBuy', '매수', '강력매수']]
    hot_topic = Counter([report.company for report in report_list]).most_common()

    start = str(datetime.strptime('2022-07-01', "%Y-%m-%d"))
    end = str(datetime.strptime('2022-07-31', "%Y-%m-%d"))
    new_positive = [pos for pos in positive_report if start <= str(pos.create_date) <= end]
    new_negative = [neg for neg in negative_report if start <= str(neg.create_date) <= end]
    context = {'segment': 'index',
               'report_list': report_list[:10],
               'num_report': len(report_list),
               'new_report': new_report,
               'num_positive': len(positive_report),
               'new_positive': len(new_positive),
               'num_negative': len(negative_report),
               'new_negative': len(new_negative),
               'hot_topic': hot_topic[:3]
               }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
def tables(request):
    report_list = Report.objects.order_by('-create_date')
    page = request.GET.get('page', '1')
    paginator = Paginator(report_list, 10)
    page_obj = paginator.get_page(page)

    context = {'segment': 'index',
               'report_list': page_obj,
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