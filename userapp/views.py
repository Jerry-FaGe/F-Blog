import datetime
from django.shortcuts import render,redirect
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from .models import User
from .forms import Login_Form,Register_Form
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog
from django.http import JsonResponse
import datetime, random
from common import util, smssend
# Create your views here.

def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects .filter(read_details__date__lt=today, read_details__date__gte=date) .values('id', 'title') .annotate(read_num_sum=Sum('read_details__read_num')) .order_by('-read_num_sum')
    return blogs[:5]

def home(request):
    if request.session.get('is_login',None):
        return redirect("/blog/")
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    return render(request,'userapp/home_re.html',context)
def index(request):
    pass
    return render(request,'userapp/index_re.html')

def login(request):
    if request.session.get('is_login',None):
        return redirect("/blog/")
    if request.method == "POST":
        login_form = Login_Form(request.POST)
        text = "所有字段都必须填写！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name = username)
                #print(user.password)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/blog/')
                else:
                    text = "密码不正确"
            except:
                text = "用户名不存在"
        return render(request,'userapp/login.html',{"text":text,'login_form':login_form})
    login_form = Login_Form()
    return render(request,'userapp/login.html',{'login_form':login_form})

def register(request):
    if request.session.get('is_login', None):
    # 登录状态不允许注册。
        return redirect("/user/index/")
    if request.method == "POST":
        register_form = Register_Form(request.POST)
        text = "所有字段不能为空"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password']
            password2 = register_form.cleaned_data['re_password']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            phone = register_form.cleaned_data['phoneNO']
            if password1 != password2:
                text = "两次输入的密码不同！"
            else:
                same_username = User.objects.filter(name = username)
                if same_username:#用户名唯一
                    text = "当前用户名已被注册，请重新选择用户名！"
                    return render(request,"userapp/register.html",{"register_form":register_form,"text":text})
                same_email = User.objects.filter(email=email)
                if same_email:#邮箱唯一
                    text = "该邮箱已被注册，请重新选择其他邮箱！"
                    return render(request,"userapp/register.html",{"register_form":register_form,"text":text})
                #没错了，写入数据库
                new_user = User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.phoneNO = phone
                new_user.save()
                return redirect("/user/login/")#跳转到登录页面
    register_form = Register_Form()
    return render(request, 'userapp/register.html',{"register_form":register_form})

def logout(request):
    if not request.session.get('is_login',None):
        return redirect("/user/")
    request.session.flush()
    return redirect("/user/")

#忘记密码
def password(r):
    if r.method == "GET":
        # data = common()
        return render(r, 'userapp/password.html')
        # return render(r, 'userapp/password.html', data)
    else:
        ret = {}
        ret["retCode"] = "1003"
        ret["retMsg"] = "此用户不存在"
        try:
            username = r.POST["username"]
            phoneNO = r.POST["phoneNo"]
            password = r.POST["password"]
            # passwordmw = rsautil.decrypt_data(password)
            # password = util.getMd5(passwordmw)
            smscode = r.POST["smscode"]
            cachecode = cache.get(phoneNO)
            rs = User.objects.get(name=username)
            phoneNO1=rs.phoneNO
            if phoneNO1!= phoneNO:
                ret["retMsg"] = "用户名和手机号不匹配"
                return JsonResponse(ret)
            else:
                if smscode != str(cachecode):
                    ret["retCode"] = "1004"
                    ret["retMsg"] = "验证码有误"
                    return JsonResponse(ret)
                else:
                    # TODO 判断用户名是否存在
                    rs = User.objects.filter(name=username)
                    if len(rs) == 0:
                        ret["retCode"] = "1001"
                        ret["retMsg"] = "此用户不存在"
                        return JsonResponse(ret)
                    else:
                        user = rs[0]
                        user.password = password
                        user.opertionTime = datetime.datetime.now()
                        user.save()
                        ret["retCode"] = "1000"
                        ret["retMsg"] = "/user/login/"
                        return JsonResponse(ret)
        except Exception as e:
            print(e)
        return JsonResponse(ret)

def sms(request):
    phoneNO = request.GET["phoneNO"]
    data = random.randint(100000, 999999)
    cache.set(phoneNO, data, 300)
    # 下面发送短信部分
    send_return = smssend.sendSMS(data, phoneNO)
    rs = {}
    if send_return == True:
        rs["retCode"] = "2000"
        rs["retMsg"] = "验证码发送成功"
        return JsonResponse(rs)
    else:
        rs["retCode"] = "2001"
        rs["retMsg"] = "验证码发送失败，请稍后重试"
        return JsonResponse(rs)