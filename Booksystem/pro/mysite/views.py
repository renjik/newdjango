from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import*
from . form import bookform



# Create your views here.
def signup(request):
    # if request.user.is_authenticated:
    #     return render(request,'home.html')
    # else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            c_password = request.POST.get('c_password')
            if password == c_password:
                if User.objects.filter(username = username,email = email).exists():
                        messages.info(request,'username already taken')
                        print('already have')
                else:
                     new_user = User.objects.create_user(username,email,password)
                     new_user.save()
                     return redirect(login1)
            else:
                 print('wrong password')
        return render(request,'signup.html')
    



def login1(request):
    # if request.user.is_authenticated:
    #      return render (request,'home.html')
    # else:
         if request.method == 'POST':
            username = request.POST.get('username') 
            password = request.POST.get('password') 
            user = authenticate(request,username = username,password = password)
            
            if user is not None:
                 login(request,user)
                 return redirect(upload)
            else:
                 messages.info(request,'user not exist')
                 print('user not exist')
                 return redirect (login1)
         return render(request,'login1.html')

@login_required
def home(request):
     if request.user.is_authenticated:
          return render(request,'home.html')
     else:
          return redirect(login)
     

@login_required
def userlogout(request):
     
     logout(request)
     return redirect(login1)



def upload(request):
     form =bookform()
     if (request.method == 'POST'):
          form = bookform(request.POST,request.FILES)
          if form.is_valid():
               form.save()
               return redirect(fileupload)
     return render(request,'home.html',{'forms':form})

def fileupload(request):
     b ={
          'dwn1': book.objects.all()
     }
     return render(request,'fileupload.html',b)


def edit (request,s_id):
     id = book.objects.get(m = s_id)
     form=bookform( instance = id)
     if request.method == 'POST':
          form=bookform(request.POST,request.FILES,instance = id)
          # b_title = request.POST.get('title')
          # b_pdf = request.FILES.get('pdf')
          # b_cover = request.FILES.get('cover')
          # book.objects.filter(id = s_id).update(title=b_title,pdf=b_pdf,cover=b_cover)
          if form.is_valid():
               form.save()
               return redirect('home')
     return render(request,'edit.html',{'forms':form})

def delete(request,s_id):
     delt = book.objects.get(m = s_id)
     delt.delete()
     return redirect(home)          
     