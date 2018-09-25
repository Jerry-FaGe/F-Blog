from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from .models import Blog,BlogType
from comment.models import Comment
from read_statistics.utils import read_statistics_once_read,get_seven_days_read_data
# Create your views here.

#随机推荐
def rand_blogs(except_id=0):
    rand_count = 3
    return Blog.objects.exclude(id=except_id).order_by('?')[:rand_count]

def get_common(request,blogs_all_list):
    fenye = Paginator(blogs_all_list, 3)  # 一页两条
    page_num = request.GET.get("page", 1)  # 获取页码参数
    page_of_blogs = fenye.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页面
    # 获取当前页码前后各两页
    page_range = list(range(max(current_page_num - 2, 1), min(fenye.num_pages + 1, current_page_num + 3)))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if fenye.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != fenye.num_pages:
        page_range.append(fenye.num_pages)

    # 获取日期内的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all() #BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    context = get_common(request,blogs_all_list)
    if request.session.get('is_login',None):
        context["blogs_count"] = Blog.objects.all().count()
        context['dates'] = dates
        context['read_nums'] = read_nums
        context['rand_blogs'] = rand_blogs()
        return render(request,'userapp/index_re.html',context)
    return redirect("/user/")

def blogs_with_type(request,blog_type_id):
    blog_type = get_object_or_404(BlogType, pk=blog_type_id)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_common(request, blogs_all_list)
    if request.session.get('is_login', None):
        context['blog_type'] = blog_type
        context["blogs_count"] = Blog.objects.all().count()
        return render(request, "blog/blogs_with_type_re.html", context)
    return redirect("/user/")

def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_common(request, blogs_all_list)
    if request.session.get('is_login', None):
        context["blogs_count"] = Blog.objects.all().count()
        context["blogs_with_date"] = "%s年%s月" %(year,month)
        return render(request, "blog/blogs_with_date_re.html", context)
    return redirect("/user/")

def blog_detail(request,blog_id):
    if request.session.get('is_login', None):
        blog = get_object_or_404(Blog, pk=blog_id)
        read_cookie_key = read_statistics_once_read(request, blog)
        previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
        next_blog= Blog.objects.filter(created_time__lt=blog.created_time).first()
        rand_blogs_object = rand_blogs(blog_id)
        user = request.session['user_name']
        comments = Comment.objects.filter(comment_title=blog_id)
        response = render(request,'blog/blog_detail_re.html', locals())
        response.set_cookie('blog_%s_read'%blog_id,"true")
        return response
    else:
        blog = get_object_or_404(Blog, pk=blog_id)
        read_cookie_key = read_statistics_once_read(request, blog)
        previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
        next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
        rand_blogs_object = rand_blogs(blog_id)
        user = "AnonymousUser"
        comments = Comment.objects.filter(comment_title=blog_id)
        response = render(request, 'blog/blog_detail_re.html', locals())
        response.set_cookie('blog_%s_read' % blog_id, "true")
        return response


