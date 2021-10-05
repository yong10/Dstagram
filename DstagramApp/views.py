from django.shortcuts import render, redirect, HttpResponse
from .models import User, Photo, Comment
from django.contrib import messages
from urllib.parse import urlparse
import bcrypt


def index(request):
    return render(request, 'index.html')

def logUser(request):
    user = User.objects.filter(email=request.POST['email'])
    errors = {}
    if not user:
        errors['email'] = "Invalid email or password"
    else:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/Dstagram')
        else:
            errors['password'] = "Invalid email or password"
        
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        return redirect('/Dstagram')


def register(request):
    return render(request, 'register.html')

def addUser(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        users = User.objects.create(f_name=request.POST['f_name'], l_name=request.POST['l_name'], email=request.POST['email'], password=pw_hash)
        request.session['userid'] = users.id
        return redirect('/Dstagram')

def Dstagram(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        context = {
            'loggedin': User.objects.get(id=request.session['userid']),
            'allPhotos': Photo.objects.all().order_by('-created_at'),
        }
        return render(request, 'Dstagram.html', context)

def createPhoto(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        return render(request, 'create.html')

def addPhoto(request):
    user = User.objects.get(id=request.session['userid'])
    Photo.objects.create(creater=user, text=request.POST['text'], image=request.FILES['img'])
    return redirect('/Dstagram')

def update(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        context = {
            'one': Photo.objects.get(id=id)
        }
        return render(request, 'update.html', context)

def updatePhoto(request, id):
    updatephoto = Photo.objects.get(id=id)
    updatephoto.text = request.POST['text']
    updatephoto.save()
    return redirect('/Dstagram')

def deletePhoto(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        photo = Photo.objects.get(id=id)
        photo.delete()
    refer_url = request.META.get('HTTP_REFERER')
    path = urlparse(refer_url).path
    return redirect(path)

def addComment(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        u = User.objects.get(id=request.session['userid'])
        p = Photo.objects.get(id=id)
        Comment.objects.create(commentText=request.POST['comment'], commenter=u, photoCommented=p)
    refer_url = request.META.get('HTTP_REFERER')
    path = urlparse(refer_url).path
    return redirect(path)

def deleteComment(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        c = Comment.objects.get(id=id)
        c.delete()
    refer_url = request.META.get('HTTP_REFERER')
    path = urlparse(refer_url).path
    return redirect(path)

def like(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        u = User.objects.get(id=request.session['userid'])
        p = Photo.objects.get(id=id)
        if u in p.like.all():
            u.like_post.remove(p)
        else:
            u.like_post.add(p)
    
    refer_url = request.META.get('HTTP_REFERER')
    path = urlparse(refer_url).path
    return redirect(path)
    

def liked_post(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        context = {
            'u': User.objects.get(id=request.session['userid'])
        }
        return render(request, 'liked_post.html', context)

def save(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        u = User.objects.get(id=request.session['userid'])
        p = Photo.objects.get(id=id)
        if u in p.favorite.all():
            u.favorite_post.remove(p)
        else:
            u.favorite_post.add(p)
    refer_url = request.META.get('HTTP_REFERER')
    path = urlparse(refer_url).path
    return redirect(path)

def saved_post(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        context = {
            'u': User.objects.get(id=request.session['userid'])
        }
        return render(request,'saved_post.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')