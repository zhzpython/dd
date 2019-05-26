from django.urls import path
from  dangdangapp import views

urlpatterns = [

    path('bookdetails/',views.bookdetails,name='bookdetails'),
    path('index/',views.index,name='index'),
    path('booklist/',views.booklist,name='booklist'),
    path('login/',views.login,name='login'),
    path('loginlogic/',views.loginlogic,name='loginlogic'),
    path('car/',views.car,name='car'),
    path('indent/',views.indent,name='indent'),
    path('indentok/',views.indentok,name='indentok'),
    path('register/',views.register,name='register'),
    path('checkname/',views.checkname,name='checkname'),
    path('checkpwd/',views.checkpwd,name='checkpwd'),
    path('recheckpwd/',views.recheckpwd,name='recheckpwd'),
    path('registerlogic/',views.registerlogic,name='registerlogic'),
    path('registerok/',views.registerok,name='registerok'),
    path('getcaptcha/',views.getcaptcha,name='getcaptcha'),
    path('checkcapt/',views.checkcapt,name='checkcapt'),
    path('delsession/',views.delsession,name='delsession'),
    path('checklogname/',views.checklogname,name='checklogname'),
    path('checklogpwd/',views.checklogpwd,name='checklogpwd'),
    path('addcar/',views.add_car,name='addcar'),
    path('upbooknum/',views.upbooknum,name='upbooknum'),
    path('check_name/',views.check_name,name='check_name'),
    path('check_addr/',views.check_addr,name='check_addr'),
    path('check_ems/',views.check_ems,name='check_ems'),
    path('check_phone/',views.check_phone,name='check_phone'),
    path('delbook/',views.delbook,name='delbook'),
    path('add_addr/',views.add_addr,name='add_addr'),
    path('indentlogic/',views.indentlogic,name='indentlogic'),
    path('return_bookdetails/',views.return_bookdetails,name='return_bookdetails'),
    path('return_booklist/',views.return_booklist,name='return_booklist'),
    path('email_receive/',views.email_receive,name='email_receive'),
    path('checkemail/',views.check_email,name='checkemail'),

]