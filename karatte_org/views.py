from atexit import register
from django.http import BadHeaderError
from django.shortcuts import redirect, render
from urllib import request
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.conf import settings
from django.core.mail import send_mail,BadHeaderError

#load admin home

def adminlogin(request):
    return render(request,'login.html')


def load_admin_home(request):
    return render(request,'adminhome.html')

def load_folder_create(request):
    folders=imagefolder.objects.all()
    return render(request,'folder.html',{'folders':folders})

def load_updatefolder(request,folderl_id):
    folderl=imagefolder.objects.get(id=folderl_id)
    return render(request,'folderupdate.html',{'folderl':folderl})




def uploadfile(request):
    if request.method=="POST":
        file=request.FILES.get('file')
        aff=affiliation.objects.all()
        print(aff)
        if aff==0 :
            affiliation.objects.create(affiliation_name=file)
        else:
            affi=affiliation.objects.get(id=2)
            affi.affiliation_name=file
            affi.save() 
        return redirect('load_affiliation')

def login(request): 
    try:
        if request.method == 'POST':
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                request.session["uid"] = user.id

                if user is not None:
                    auth.login(request, user)
                    if user.is_superuser==1:
                        return redirect ('load_admin_home')

            except:
                messages.info(request, 'Invalid username or password')
                return render(request, 'login.html')                        
        else:
            #messages.info(request, 'Invalid username or password')
            return render('login.html')        
    except:
       # messages.info(request, 'Invalid username or password')
        return render(request, 'login.html')




#admin folder update

def update_folder(request,folderu_id):
    if request.method=="POST":
        folder=imagefolder.objects.get(id=folderu_id)
        folder.folder_name=request.POST.get('file')
        folder.save()
        folders=imagefolder.objects.all()
        return render(request,'folder.html',{'folders':folders,})
    else:
        return redirect('load_admin_home')




def load_addimages(request):
    return render(request,'addimages.html')

# admin folder 
 
def create_folder(request):
    if request.method=="POST":
        fname=request.POST['file']
        folder=imagefolder(folder_name=fname,)

        folder.save()
        return redirect('load_folder_create')
    else:
        return redirect('load_admin_home')

def deletefolder(request,fldd_id):
    folderdelete=imagefolder.objects.get(id=fldd_id)
    folderdelete.delete()
    return redirect(load_folder_create)



def load_images(request,folimg_id):
    folder=imagefolder.objects.get(id=folimg_id)
    folder_images=images.objects.filter(folder_id=folimg_id)
    print(folder_images)
    return render(request,'images.html',{'folder_images':folder_images,'folder':folder})

#add images to  folder 

def add_images_folder(request):
    if request.method=='POST':
        name=request.POST['name']
        image=request.FILES.getlist('imgs')
        folderid=imagefolder.objects.get(folder_name=name)
        for imag in image:
            images.objects.create(
                image_url=imag,
                folder_id=folderid)
        return redirect('load_images',folderid.id)

#admin delete single image

def deleteimg(request,img_id):
    image=images.objects.get(id=img_id)
    image.delete()
    return redirect('load_folder_create')



# load home page

def load_home_page(request):
    bgimg=blackbelt_holders.objects.all()
    folders=imagefolder.objects.all()
    folimgs=images.objects.all()
    return render(request,'index.html',{'bgimg':bgimg,'folders':folders,'folimgs':folimgs})


def sort_img(request,id):
    print('Hi')
    folimgs = images.objects.filter(folder_id=id)
    
    print(folimgs)
    
    bgimg = blackbelt_holders.objects.all()
    folders = imagefolder.objects.all()
    return render(request,'index.html',{'bgimg':bgimg,'folders':folders,'folimgs':folimgs})





        

def logout(request):
    request.session["uid"] = ""
    auth.logout(request)
    return redirect('load_home_page')