from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from postgreSQL import PostgresDB


# Create your views here.
# printout Report list
def index(request):
    report = PostgresDB()
    report_list = report.execute(f"SELECT * FROM report ORDER BY create_date DESC;")
    # report_list = Report.objects.order_by('-create_date')
    context = {'report_list': report_list}
    return render(request, 'home/report_list.html', context)

def detail(request, report_id):
    pass
