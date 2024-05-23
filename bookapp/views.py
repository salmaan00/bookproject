from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
# Create your views here.
from .forms import AuthorForm,BookForm
from .models import Book

from .models import UserProfile,loginTable

# def createBook(request):
#     books=Book.objects.all()
#
#     if request.method=='POST':
#         title=request.POST.get('title')
#         price=request.POST.get('price')
#
#         book=Book(title=title,price=price)
#         book.save()
#
#     return render(request,'book.html',{'books':books})

def listBook(request):
    books=Book.objects.all()

    paginator=Paginator(books,4)
    page_number=request.GET.get('page')

    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    return render(request,'listbook.html',{'books':books,'page':page})


def detailsView(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request,'detailsview.html',{'book':book})
#
# def updateBook(request,book_id):
#     book=Book.objects.get(id=book_id)
#
#     if request.method=='POST':
#         title= request.POST.get("title")
#         price= request.POST.get('price')
#
#         book.title=title
#         book.price=price
#
#         book.save()
#
#         return redirect('/')
#
#     return render(request,'updateview.html',{'book':book})


def updateBook(request,book_id):
    book=Book.objects.get(id=book_id)

    if request.method=='POST':
        form = BookForm(request.POST,request.FILES,instance=book)

        if form.is_valid():
            form.save()


        return redirect('/')
    else:
        form=BookForm(instance=book)

    return render(request,'updateview.html',{'form':form})




def deleteView(request,book_id):

    book=Book.objects.get(id=book_id)

    if request.method=='POST':
        book.delete()

        return redirect('/')

    return render(request,'deleteview.html', {"book":book})


def createBook(request):

    books=Book.objects.all()


    if request.method=='POST':
        form=BookForm(request.POST,request.FILES)
        print(form)


        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form =BookForm

    return render(request,'book.html',{'form':form,"books":books})

def Create_AuthorForm(request):
    if request.method=="POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form=AuthorForm()

    return render(request,'author.html',{'form':form})


def index(request):
    return render(request,'base.html')


def Search_Book(request):
    query=None
    books=None

    if 'q' in request.GET:

        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query)  | Q(author__name__icontains=query))
    else:
        books=[]
    context={'books':books,'query':query}

    return render(request,'search.html',context)


# def Register_user(request):
#
#     if request.method=="POST":
#         username=request.POST.get('username')
#         first_name=request.POST.get('first_name')
#         last_name=request.POST.get('last_name')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         cpassword=request.POST.get('password1')
#
#         if password==cpassword:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,'this is username already exists')
#                 return redirect('register')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request,'this email already taken')
#                 return redirect('register')
#             else:
#                 user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
#                 user.save()
#             return redirect('login')
#         else:
#             messages.info(request,'this password not match')
#             return redirect('register')
#
#     return render(request,'register.html')
# #
# def loginUser(request):
#     if request.method=='POST':
    #     username=request.POST.get('username')
    #     password=request.POST.get('password')
    #     user=auth.authenticate(username=username,password=password)
    #
    #     if user is not None:
    #         auth.login(request,user)
    #         return redirect('/')
    #     else:
    #         messages.info(request,'please provide correct details')
    #         return redirect('login')
    #
    # return render(request,'login.html')

def logOut(request):
    auth.logout(request)
    return redirect('login')

#
# def homePage(request):
#     return render(request,'home.html')


def homePage(request):
    return render(request,'base.html')


# | Q(author__icontains=query))


def userRegistraion(request):

    login_table=loginTable()
    userprofile=UserProfile()

    if request.method=='POST':
        userprofile.username=request.POST('username')
        userprofile.password=request.POST('password')
        userprofile.password2=request.POST('password1')

        login_table.username=request.POST('username')
        login_table.password=request.POST('password')
        login_table.password2=request.POST('password1')
        login_table.type='user'


    if request.POST["password"]==request.POST['password1']:
        userprofile.save()
        login_table.save()

        messages.info(request,'Registraion success')
        return redirect('login')
    else:
        messages.info(request,"Password not matching")
        return redirect('register')
    return render(request,'register.html')

def loginPage(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=loginTable.objects.filter(username=username,password=password,type='user').exists()
        try:
            if user is not None:
                user_details=loginTable.objects.get(username=username,password=password)
                user_name=user_details.username
                type=user_details.type

                if type=='user':
                    request.session['username'].user_name
                    return redirect('user_view')
                elif type=='admin':
                    request.session['username'].user_name
                    return redirect('admin_view')

            else:
                messages.error(request,'invalid username or password')
        except:
            messages.error(request,'invalid role')

    return render(request,'login.html')



def admin_view(request):
    user_name=request.session['username']
    return render(request,'admin_view.html',{'user_name':user_name})

def user_view(request):
    user_name=request.session['username']
    return render(request,'user_view.html',{'user_name':user_name})


