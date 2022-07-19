function openBusiness(type, code, date){
    var url = "/apps.chart/chart.list?";
    var parm = "frame=analysis/layer&report_type="+type+"&business_code="+code+"&report_date="+date;
    document.getElementById("chart_ifrm").src=url+parm;
    _chart_view("V");
}

function openIndustry(type, code, market, date){
    var url = "/apps.chart/chart.list?";
    var parm = "frame=analysis/layer&report_type="+type+"&industry_code="+code+"&market_type="+market+"&report_date="+date;
    document.getElementById("chart_ifrm").src=url+parm;
    _chart_view("V");
}

function _chart_view(type){
    if(type=="V"){
        if($('.frame_back_image').length > 0){
            $('.frame_back_image').show();
        }else{
            document.getElementById("back_image").width = 980;
            document.getElementById("back_image").height = 650;
            document.getElementById("back_image").style.display = "block";
        }
        document.getElementById("chart_view").style.display = "block";
    }else if(type=="C"){
        if($('.frame_back_image').length > 0){
            $('.frame_back_image').hide();
        }else{
            document.getElementById("back_image").width = 0;
            document.getElementById("back_image").height = 0;
            document.getElementById("back_image").style.display = "none";
        }
        document.getElementById("chart_ifrm").src= "";
        document.getElementById("chart_view").style.display = "none";
    }
}



//검색
function _search(url){
    document.getElementById('now_page').value = "1";
    var f = document.getElementById('f_search');
    f.target = "_self";
    f.action = url;
    f.submit();
}

// Enter 액션
function _return(e){
    if(e.keyCode == 13)
        _search('/apps.analysis/analysis.list');
}

//특수 기호 체크
function chkString(obj)
{
    if(obj.search(/,|!|@|{|}|;|\^|\%|\$|\\|\||~|#|\[|\]|\+|\'|\"|<|>/) != -1) {
        return false;
    }
        return true;
}

//숫자만 입력
function handlerNum(val){
    var e = e || event;

    if(e.keyCode >= 48 && e.keyCode <= 57 || e.keyCode >= 96 && e.keyCode <= 105 || e.keyCode == 8 || e.keyCode == 46 || e.keyCode == 9){
        if(e.keyCode == 48 || e.keyCode == 96){ //0을 눌렀을경우
            if(val.value == "" ){
                //e.returnValue=false;
                return ;
            }else{
                return;
            }
        }else{
            return;
        }
    }else{
        e.returnValue=false;
    }
}

//이메일 체크
function chkMail(obj){
    re=/^[0-9a-zA-Z-_\.]*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;

    if(re.test(obj)) {
        return true;
    } else {
        return false;
    }
}


//숫자 체크
function chkNumber(obj){
    var re=/^[0-9]{4}$/i;

    if(re.test(obj)) {
        return true;
    } else {
        return false;
    }
}
//비밀번호 유효성 체크
function passwordcheck(val){
    var tmp1 = /[a-zA-Z].*[0-9]/;
    var tmp2 = /[0-9].*[a-zA-Z]/;
    var tmp3 = /[a-zA-Z].*[!,@,#,$,%,^,&,*,?,_,~]/;
    var tmp4 = /[!,@,#,$,%,^,&,*,?,_,~].*[a-zA-Z]/;

    // 영문+숫자
    var chk1 = tmp1.test(val) || tmp2.test(val);
    // 영문+특수문자
    var chk2 = tmp3.test(val) || tmp4.test(val);

    if(!chk1){
        alert("비밀번호는 문자, 숫자 조합으로 입력해 주세요.");
        return false;
    }

    var SamePass_0 = 0; //동일문자 카운트
    var SamePass_1 = 0; //연속성(+) 카운드
    var SamePass_2 = 0; //연속성(-) 카운드

    var chr_pass_0;
    var chr_pass_1;
    var chr_pass_2;

    for(var i=0; i < val.length; i++)
    {
        chr_pass_0 = val.charAt(i);
        chr_pass_1 = val.charAt(i+1);

        //동일문자 카운트
        if(chr_pass_0 == chr_pass_1)
        {
            SamePass_0 = SamePass_0 + 1;
        }


        chr_pass_2 = val.charAt(i+2);
        //연속성(+) 카운드

        if(chr_pass_0.charCodeAt(0) - chr_pass_1.charCodeAt(0) == 1 && chr_pass_1.charCodeAt(0) - chr_pass_2.charCodeAt(0) == 1)
        {
            SamePass_1 = SamePass_1 + 1;
        }

        //연속성(-) 카운드
        if(chr_pass_0.charCodeAt(0) - chr_pass_1.charCodeAt(0) == -1 && chr_pass_1.charCodeAt(0) - chr_pass_2.charCodeAt(0) == -1)
        {
            SamePass_2 = SamePass_2 + 1;
        }
    }
    if(SamePass_0 > 1)
    {
        alert("동일문자를 3번 이상 사용할 수 없습니다.");
        return false;
    }

    if(SamePass_1 > 1 || SamePass_2 > 1 )
    {
        alert("연속된 문자열(123 또는 321, abc, cba 등)을\n 3자 이상 사용 할 수 없습니다.");
        return false;
    }

    return true;
}

//PAGE 이동
function _Page_Link(link){
    window.location.href = link;
}

//PAGE 이동
function _Order_Link(old, order, url){
    var link = url;
    var order_type = old+order;
    if(old==10000000){
        link = link.replace('&order_type=10000000', '');
        link = link+"&order_type="+order_type;
    }else{
        var chk = link.indexOf(old);
        link = link.replace(old, order_type);
        link = link.replace("3", "0");
    }
    _Page_Link(link);
}


//PAGE 이동
function _popup_open(link, width, height, scrollbars){
    var LeftPosition=0;
    var TopPosition=0;

    if (screen.width < 1025){
        LeftPosition=0;
        TopPosition=0;
    } else {
        LeftPosition=(screen.width)?(screen.width-width)/2:100;
        TopPosition=(screen.height)?(screen.height-height)/2:100;
        TopPosition = TopPosition-20;
    }
    window.open(link, "_new", "width="+width+", height="+height+", top="+TopPosition+", left="+LeftPosition+", scrollbars="+scrollbars+", toolbar=no, location=no, status=no, menubar=no, directories=no, resizable=no");
}

$(function(){
    $('.chart_popup .layer_close').click(function(){
        $('.chart_popup').hide();
        $('.chart_popup > iframe').attr("src", '');
    });

    $('.chart_btn').click(function(e){
        e.preventDefault();
        $('.chart_popup > iframe').attr("src", $(this).attr('href'));
        $('.chart_popup').show();
    });

    $('#container .top_con .tabT01 li a').click(function(e){
        e.preventDefault();
        var url = $(this).attr('href');
        /*

        var report_type = '';

        if(url.indexOf("business")){
            report_type = 'CO';
        }else if(url.indexOf("industry")){
            report_type = 'IN';
        }else if(url.indexOf("market")){
            report_type = 'MA';
        }else if(url.indexOf("economy")){
            report_type = 'EC';
        }else if(url.indexOf("derivative")){
            report_type = 'DE';
        }
        */

        if($.trim($('#search_text').val()) != '' && url.indexOf("business.list") < 0 && url.indexOf("chart.view") < 0){
            if(url.indexOf("?") > 0){
                url = url + '&search_text=' + $.trim($('#search_text').val());
            }else{
                url = url + '?search_text=' + $.trim($('#search_text').val());
            }
            url = url + '&sdate=' + $('#sdate').val();
            url = url + '&edate=' + $('#edate').val();
            if($('#_search_value').attr("data-value") != ''){
                url = url +'&search_value=' + $('#_search_value').attr('data-value');
            }
        }
        location.href = url;
    });
});