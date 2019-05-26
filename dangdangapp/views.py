from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from dangdangapp.models import AddressInfo,Booksinfo,OrderList,Sort1,TOrder,TUser,Confirm_string
from django.core.paginator import Paginator
import re,time,random,string
from dangdangapp.captcha.image import ImageCaptcha
from dangdangapp.shoppingcar import Caritem,Car
import random,datetime
import json
import os
from django.core.mail import send_mail,EmailMultiAlternatives

# Create your views here.
def return_bookdetails(request):
    bookid=request.session.get('book_id')
    return redirect('/dangdang/bookdetails/?bookid='+bookid)

def bookdetails(request):   #书籍详情页跳转
    id=request.GET.get('bookid')
    request.session['book_id']=id
    book=Booksinfo.objects.get(id=id)
    sortid=book.sort_id
    secondname=Sort1.objects.get(id=sortid).sort_name
    secondsort=Sort1.objects.get(id=sortid)
    parentid=Sort1.objects.get(id=sortid).parent_id
    firstname=Sort1.objects.get(id=parentid).sort_name
    firstsort=Sort1.objects.get(id=parentid)
    username = request.session.get('username')
    if username:
        u1 = username[0:3]
    else:
        u1 = ''
    return render(request,'Book details.html',{
        'book':book,
        'firstname':firstname,
        'secondname':secondname,
        'firstsort':firstsort,
        'secondsort':secondsort,
        'username': username,
        'u1': u1
    })

def index(request):     #主页面跳转
    books1=Booksinfo.objects.order_by('-arrival_time')[0:8]
    books2=Booksinfo.objects.filter(arrival_time__gte='2019-1-1').order_by('-sales_volume')[0:5]
    books3=Booksinfo.objects.order_by('-customer_grade')[0:12]
    books4 = Booksinfo.objects.filter(arrival_time__gte='2019-1-1').order_by('-sales_volume')[0:10]
    sort1=Sort1.objects.filter(parent_id=0)
    sort2 = Sort1.objects.all()
    username=request.session.get('username')
    if username:
        u1=username[0:3]
    else:
        u1=''
    return render(request,'index.html',{
        'sort1':sort1,
        'sort2':sort2,
        'books1':books1,
        'books2':books2,
        'books3':books3,
        'books4':books4,
        'username':username,
        'u1':u1
    })

def return_booklist(request):
    bookid=request.session.get('a')
    parentid=request.session.get('b')
    num=request.session.get('c')
    print(bookid,68)
    print(parentid,69)
    print(num,70)
    return redirect('/dangdang/booklist/?bookid='+bookid+'&parentid='+parentid+'&num='+num)

def booklist(request):  #跳转到分类页面
    sort1 = Sort1.objects.filter(parent_id=0)
    sort2 = Sort1.objects.all()
    bookid=request.GET.get('bookid')
    parentid=request.GET.get('parentid')
    number=str(request.GET.get('num'))
    request.session['a']=bookid
    request.session['b']=parentid
    request.session['c']=number
    username = request.session.get('username')
    if username:
        u1 = username[0:3]
    else:
        u1 = ''
    if number.isdigit() :
        number=number
    else:
        number=1
    if not number:
        number = 1
    else:
        number=int(number)
    if parentid =='0':
        firstsort = Sort1.objects.filter(id=bookid)[0] #获取第一分类的名字
        secondsort = None
        bookobj=Sort1.objects.filter(parent_id=bookid)    #获取第二分类对象
        l=[]
        for i in bookobj:
            l.append(i.id)
        l1=[]
        for j in l:
            obj=Booksinfo.objects.filter(sort_id=j)
            for k in range(0,len(obj)):
                l1.append(obj[k])
        pagtor=Paginator(l1,per_page=5)
        allnum = pagtor.num_pages
        if number not in range(1,allnum+1):
            number=allnum
        page=pagtor.page(number)

        return render(request, 'booklist.html', {
            'sort1': sort1,
            'sort2': sort2,
            'bookid': bookid,
            'parentid': parentid,
            'firstsort': firstsort,
            'secondsort':secondsort,
            'pages':page,
            'page_all_num':pagtor.num_pages,
            'num':number,
            'username':username,
            'u1':u1
        })
    else:
        secondsort=Sort1.objects.filter(id=bookid)[0].sort_name
        firstsort=Sort1.objects.filter(id=parentid)[0]
        books=Booksinfo.objects.filter(sort_id=bookid)
        pagtor = Paginator(books, per_page=4)
        allnum = pagtor.num_pages
        if number not in range(1, allnum + 1):
            number = allnum
        page = pagtor.page(number)
        return render(request,'booklist.html',{
            'sort1':sort1,
            'sort2':sort2,
            'bookid':bookid,
            'parentid':parentid,
            'firstsort':firstsort,
            'secondsort':secondsort,
            'pages': page,
            'page_all_num': pagtor.num_pages,
            'num': number,
            'username': username,
            'u1': u1
        })



def checkname(request):
    username = request.POST.get('username')
    if username=='':
        return HttpResponse('a')
    else:
        u=TUser.objects.filter(name=username)
        a=re.match( r"1\d{10}", username)
        b=re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',username)
        if u:
            return HttpResponse('Y')  #用户名已经存在
        else:
            if a or b:
                return HttpResponse('N')  #匹配手机格式
            else:
                return HttpResponse('y')#格式不正确

def checkpwd(request):
    time.sleep(1)
    pwd = request.POST.get('pwd')
    if pwd=='':
        return HttpResponse('a') #密码不能为空
    else:
        if len(pwd)<6 or len(pwd)>20:
            return HttpResponse('n')  # 密码长度不符合要求
        else:
            return HttpResponse('y')  #密码格式正确

def recheckpwd(request):
    time.sleep(1)
    repwd = str(request.POST.get('repwd'))
    pwd = str(request.POST.get('pwd'))
    if repwd=='':
        return HttpResponse('a') #密码不能为空
    else:
        if repwd == pwd:
            return HttpResponse('n')  #两次密码一样
        else:
            return HttpResponse('z')  #两次密码不一样

def getcaptcha(request):
    image=ImageCaptcha()
    code=random.sample(string.ascii_letters+string.digits,4)
    code="".join(code)
    request.session['code']=code
    data=image.generate(code)
    return HttpResponse(data,'image/png')



def checkcapt(request):      #检查验证码
    num = request.POST.get('number')
    code=request.session.get('code')
    if num.lower()==code.lower():
        return HttpResponse('y')
    else:
        return HttpResponse('n')


def register(request):   #注册页面跳转
    flag=request.GET.get('flag')
    a = request.session.get('a')
    b = request.session.get('b')
    c = request.session.get('c')

    return render(request,'register.html',{
        'flag':flag,
        'bookid':a,
        'parentid':b,
        'num':c
    })

def email_receive(request):
    flag=request.GET.get('flag')
    code=request.GET.get('code')
    username=request.GET.get('username')
    userid=TUser.objects.get(name=username).id
    codetime=request.session.get('nowtime')
    print(userid,230)
    print(codetime,231)
    checkcode=Confirm_string.objects.filter(code_time=codetime,user_id=userid)[0]
    if checkcode:
        checkcode=checkcode.code
        if int(code)==int(checkcode):
            request.session['username']=username
            return render(request, 'register ok.html', {
                'flag': flag,
                'username': username
            })
    else:
        return redirect('/dangdang/register/?flag=' + flag)

def registerlogic(request):
    flag=request.GET.get('flag')
    txt_vcode=request.POST.get('txt_vcode')
    code=request.session.get('code')
    username=request.POST.get('txt_username')
    email=request.POST.get('email')
    count=TUser.objects.filter(name=username).count()
    pwd1=request.POST.get('txt_password')
    pwd2=request.POST.get('txt_repassword')
    check_num=random.randint(1,10)
    codetime=datetime.datetime.now()
    print(codetime,253)
    code_time=(codetime+datetime.timedelta(hours=-8)).strftime("%Y-%m-%d %H:%M:%S")
    print(code_time,255)
    request.session['nowtime']=code_time
    if  count==0 and pwd1==pwd2 and pwd1!=''and txt_vcode.lower()==code.lower():
        TUser.objects.create(name=username,password=pwd1,email=email)
        user=TUser.objects.get(name=username,password=pwd1,email=email)
        user.confirm_string_set.create(code=check_num,code_time=codetime)
        subject, from_email, to = '邮箱验证', 'zhuanghanzhong@sina.com', 'zhz_python@sina.cn'
        text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
        html_content = '<p>感谢注册<a href="http://{}/?code={}&flag={}&username={}"target = blank >  < / a >欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1:8000/dangdang/email_receive',check_num,flag,username)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse('请进行邮箱验证')
    else:
        return redirect('/dangdang/register/?flag='+flag)

def registerok(request):   #注册页面跳转成功
    a=request.GET.get('bookid')
    b=request.GET.get('parentid')
    c=request.GET.get('num')
    print(a,219)
    print(b,220)
    print(c,221)

    return  render(request,'register ok.html',{
        'bookid':a,
        'parentid':b,
        'num':c
    })

def delsession(request):
    del request.session['username']
    return redirect('index')


def login(request):  #登录页面跳转
    flag=request.GET.get('flag')
    print(flag,207)
    return render(request,'login.html',{
        'flag':flag
    })

def loginlogic(request):
    flag = request.GET.get('flag')
    txtUsername=request.POST.get('txtUsername')
    txtPassword=request.POST.get('txtPassword')
    u=TUser.objects.filter(name=txtUsername,password=txtPassword)
    if u:
        request.session['username'] = txtUsername

        return render(request,'register ok.html',{
            'flag': flag,
            'username': txtUsername
        })
    else:
        return redirect('login')

def checklogname(request):
    time.sleep(1)
    logname = request.POST.get('logname')
    print(logname,227)
    if logname=='':
        return HttpResponse('a')
    else:
        u=TUser.objects.filter(name=logname)
        if u:
            return HttpResponse('Y')  #用户名正确
        else:
            return HttpResponse('N') #格用户名不正确

def checklogpwd(request):
    logpwd = request.POST.get('logpwd')
    logname=request.POST.get('logname')
    print(logname,242)
    print(logpwd,243)
    if logpwd=='':
        return HttpResponse('b') #密码不能为空
    else:
        u = TUser.objects.filter(password=logpwd,name=logname)
        print(u)
        if u:
            return HttpResponse('c')  # 密码正确
        else:
            return HttpResponse('d')  #密码不对




def car(request):    #跳转到购物车
    car=request.session.get('car')
    if car:
        carobject=car.caritems
        s=0
        for i in carobject:
            s+=1
            print(i.book.id)
            print(i.book.dd_price)
        save=car.save_price
        total=car.total_price
    else:
        carobject=[]
        total=0
        save=0
        s=0
    username = request.session.get('username')
    if username:
        u1 = username[0:3]
    else:
        u1 = ''
    return render(request,'car.html',{
        'carobject':carobject,
        'total':total,
        'save':save,
        's':s,
        'username':username,
        'ul':u1
    })


def add_car(request):
    bookid=int(request.POST.get('bookid'))
    changenum=int(request.POST.get('changenum'))
    print(bookid,343)
    print(changenum,344)
    car=request.session.get('car')
    if car is None:
        car=Car()
        if changenum:
            car.add_book_toCar(bookid,changenum)
        else:
            car.add_book_toCar(bookid)
        request.session['car'] = car
        return HttpResponse('y')
    else:
        if changenum:
            car.add_book_toCar(bookid, changenum)
        else:
            car.add_book_toCar(bookid)
        request.session['car'] = car
        return HttpResponse('n')


def upbooknum(request):
    bookid=int(request.POST.get('bookid'))
    updown=request.POST.get('updown')
    print(bookid)
    print(updown)
    if updown=='up':
        booknum=int(request.POST.get('booknum'))+1
    else:
        booknum = int(request.POST.get('booknum'))
    car = request.session.get('car')
    car.change_car_count(bookid,booknum)
    request.session['car'] = car
    totalprice= car.total_price  #所有书的总价
    saveprice= car.save_price   #节省的价格
    for i in car.caritems:
        if i.book.id == bookid:
            bookcount=i.amount
            bookprice=i.book.dd_price * bookcount   #相同书的总价
            return JsonResponse({'totalprice':totalprice,'saveprice':saveprice,'bookprice':bookprice,'booknum':booknum})

def delbook(request):
    bookid=int(request.GET.get('bookid'))
    car=request.session.get('car')
    car.delete_book(bookid)
    request.session['car']=car
    return redirect('car')



def indent(request):   #收货地址
    flag=request.GET.get('flag')
    user=request.session.get('username')
    car=request.session.get('car')
    carboject=car.caritems
    print(car.total_price)
    addrinfo=AddressInfo.objects.all()
    print(addrinfo,381)
    if user:
        u1 = user[0:3]
    else:
        u1 = ''
    if user:
        return render(request,'indent.html',{
            'carboject':carboject,
            'addrinfo':addrinfo,
            'car':car,
            'username':user,
            'u1':u1

        })
    else:
        return redirect('/dangdang/login/?flag='+str(flag))

def indentlogic(request):
    addrid=request.GET.get('addrid')
    consignee=request.GET.get('consignee')
    request.session['consignee']=consignee
    address=request.GET.get('address')
    ems1=request.GET.get('ems1')
    phonenum=request.GET.get('phonenum')
    car = request.session.get('car')
    if car:
        a = car.caritems
    else:
        a = ''
    request.session['book_count']=a
    request.session['total_price']=car.total_price
    username = request.session.get('username')
    userid = TUser.objects.get(name=username).id
    n = str(random.randint(1, 9))
    for i in range(6):
        ordernum = random.randint(0, 9)
        n += str(ordernum)
    if addrid=='c':
        AddressInfo.objects.create(consignee=consignee,address=address,zipcode=ems1,phone=phonenum,user_id=userid)
        ass=AddressInfo.objects.get(consignee=consignee,address=address,zipcode=ems1,phone=phonenum,user_id=userid)
    else:
        ass=AddressInfo.objects.get(id=int(addrid))
    ass.torder_set.create(order_num=int(n),generated_time=datetime.datetime.now(),order_all_price=car.total_price,user_id=userid)
    for j in car.caritems:
        abb=TOrder.objects.get(order_num=int(n),generated_time=datetime.datetime.now(),order_all_price=car.total_price,user_id=userid)
        abb.orderlist_set.create(product_id=j.book.id,number=j.amount,all_price=j.amount*j.book.dd_price)

    return redirect('indentok')


def indentok(request):  #订单生成
    a=request.session.get('book_count')
    username = request.session.get('username')
    consignee=request.session.get('consignee')
    totalprice=request.session.get('total_price')
    del request.session['car']
    if username:
        u1 = username[0:3]
        return render(request,'indent ok.html',{
            'totalprice':totalprice,
            'count':len(a),
            'username':username,
            'u1':u1,
            'consignee':consignee

        })
    else:
        return redirect('/dangdang/login/?flag=1' )


def check_name(request):
    time.sleep(1)
    checkname1 = request.POST.get('checkname1')
    if checkname1=='':
        return HttpResponse('a')
    else:
        return HttpResponse('Y')  #收货人正确


def check_addr(request):
    time.sleep(1)
    addr1 = request.POST.get('checkaddr1')
    if addr1 == '':
        return HttpResponse('a')
    else:
        return HttpResponse('Y')  # 收货人正确


def check_ems(request):
    time.sleep(1)
    ems1 = request.POST.get('checkems1')
    if ems1 == '':
        return HttpResponse('a')
    else:
        if len(ems1)==6 and ems1.isdigit():
            return HttpResponse('Y')  # ems格式正确
        else:
            return HttpResponse('N')


def check_phone(request):
    time.sleep(1)
    phone1 = request.POST.get('checkphone1')
    if phone1 == '':
        return HttpResponse('a')
    else:
        if len(phone1) == 7  or len(phone1) == 8 or len(phone1) == 11 and phone1.isdigit():
            return HttpResponse('Y')  # 电话格式正确
        else:
            return HttpResponse('N')  #电话格式不正确

def add_addr(request):
    addrid=int(request.POST.get('addrid'))
    addrobj=AddressInfo.objects.filter(id=addrid)[0]
    return JsonResponse({'receiver':addrobj.consignee,'address':addrobj.address,'ems':addrobj.zipcode,'phonenum':addrobj.phone})


def check_email(request):
    time.sleep(1)
    email=request.POST.get('check_email')
    print(email)
    if email == '':
        return HttpResponse('aa')
    else:
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',email):
            return HttpResponse('bb')
        else:
            return HttpResponse('cc')
