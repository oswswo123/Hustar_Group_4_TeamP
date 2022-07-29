# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Report, Inference
from datetime import date


@login_required(login_url="/login/")
def index(request):
    report_list = Report.objects.order_by('-create_date')
    new_report = len([report for report in report_list if report.create_date == "2022-07-01"]) # str(date.today().strftime("%Y-%m-%d"))
    positive_report = Report.objects.filter(opinion='Buy')
    negative_report = [report for report in report_list if report.opinion != 'Buy']
    context = {'segment': 'index',
               'report_list': report_list[:10],
               'num_report': len(report_list),
               'new_report': new_report,
               'positive_report': positive_report,
               'num_positive_report': len(positive_report),
               'negative_report': negative_report,
               'num_negative_report': len(negative_report),
               }
    html_template = loader.get_template('home/index.html')
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