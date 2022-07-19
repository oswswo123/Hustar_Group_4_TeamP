from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Columns

@login_required(login_url='common:login')
def index(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    columns_list = Columns.objects.order_by('-create_date')
    if kw:
        columns_list = columns_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(opinion__icontains=kw) |  # 견해 검색
            Q(writer__icontains=kw) |  # 글쓴이 검색
            Q(stock_firm__icontains=kw) |  # 투자증권 검색
            Q(id__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(columns_list, 20)  # 페이지당 20개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'columns_list': page_obj, 'page': page, 'kw': kw}
    Columns.author = request.user  # author 속성에 로그인 계정 저장
    return render(request, 'AInalyst/columns_list.html', context)

@login_required(login_url='common:login')
def detail(request, columns_id):
    columns = Columns.objects.get(id=columns_id)
    context = {'columns': columns}
    return render(request, 'AInalyst/columns_detail.html', context)

