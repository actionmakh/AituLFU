import datetime
import hashlib
import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

# Create your views here.
from blog.models import Person, Post, LookingForYou, Feedback, Reply, Notification, History


def index(req):
    try:
        user = Person.objects.get(username=req.session.get('user'))
        notifications = Notification.objects.filter(lfu_id__in=user.followed)

        for notification in notifications:
            messages.error(req, notification.text, extra_tags='safe')
            alreadySeen = History(notification=notification, user=user)
            alreadySeen.save()

        for history in History.objects.filter(user=user):
            history.notification.delete()
    except:
        pass
    return render(req, 'index.html', {
        'news': Post.objects.all(),
        'LFUs': LookingForYou.objects.all()
    })


def news(req):
    try:
        user = Person.objects.get(username=req.session.get('user'))
        notifications = Notification.objects.filter(lfu_id__in=user.followed)
        print(user.followed)

        for notification in notifications:
            messages.error(req, notification.text, extra_tags='safe')
            alreadySeen = History(notification=notification, user=user)
            alreadySeen.save()

        for history in History.objects.filter(user=user):
            history.notification.delete()
            
    except:
        pass


    news = Post.objects.all()
    for i in range(len(news)):
        if len(news[i].text) > 100:
            news[i].text = news[i].text[:100] + '...'
    alerts = []
    if len(news) == 0:
        alerts.append(
            {
                'type': 'warning',
                'text': 'News are currently empty'
            },
        )
    return render(req, 'news.html', {
        'news': news,
        'alerts': alerts
    })


def login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        passEncrypted = hashlib.md5(password.encode()).hexdigest()
        errors = []
        person = None
        try:
            person = Person.objects.get(username=username)

            if person.password != passEncrypted:
                errors.append(
                    {
                        'type': 'danger',
                        'text': 'Incorrect password'
                    },
                )
        except:
            errors.append(
                {
                    'type': 'danger',
                    'text': 'User not found'
                },
            )

        if len(errors):
            return render(req, 'login.html', {
                'errors': errors
            })

        req.session['user'] = person.username
        return redirect('index')
    return render(req, 'login.html')


def register(req):
    if req.method == 'POST':

        username = req.POST['username']
        password = req.POST['password']
        rePassword = req.POST['rePassword']
        duplicate = Person.objects.filter(username=username)

        errors = []

        if duplicate:
            errors.append(
                {
                    'type': 'danger',
                    'text': 'User with this username already exists, Please use another one'
                }
            )

            if password != rePassword:
                errors.append(
                    {
                        'type': 'danger',
                        'text': 'Passwords does not match'
                    }
                )

            if len(errors):
                return render(req, 'registr.html', {
                    'alerts': errors,
                })
        newPass = hashlib.md5(password.encode()).hexdigest()
        newPerson = Person(username=username, password=newPass, followed=[])
        newPerson.save()

        return redirect('uraura')
    return render(req, 'registr.html')


def aboutUs(req):
    return render(req, 'about_us.html')


def uraura(req):
    return render(req, 'uraura.html')


def aituLFU(req):

    try:
        user = Person.objects.get(username=req.session.get('user'))
        notifications = Notification.objects.filter(lfu_id__in=user.followed)
        print(user.followed)

        for notification in notifications:
            messages.error(req, notification.text, extra_tags='safe')
            alreadySeen = History(notification=notification, user=user)
            alreadySeen.save()

        for history in History.objects.filter(user=user):
            history.notification.delete()
        
    except:
        pass

    LFUs = LookingForYou.objects.all().order_by('created_at').reverse()
    alerts = []

    for i in range(len(LFUs)):
        if len(LFUs[i].text) > 100:
            LFUs[i].text = LFUs[i].text[:100] + '...'
    if len(LFUs) == 0:
        alerts.append(
            {
                'type': 'warning',
                'text': 'LFUs currently empty'
            },
        )
    return render(req, 'aituLFU.html', {
        'LFUs': LFUs
    })


def addLFU(req):
    if req.session.get('user') is None:
        return redirect('login')
    img = req.FILES['image']
    storage = FileSystemStorage()
    image = storage.save(img.name, img)
    imgPath = storage.url(image)
    user = Person.objects.get(username=req.session.get('user'))
    text = req.POST['text']
    date = datetime.datetime.now()
    newLFU = LookingForYou(text=text, user_id=user.id, image=imgPath, created_at=date)
    newLFU.save()
    return redirect('aituLFU')


def lfuPost(req, lfuID):
    try:
        lfu = LookingForYou.objects.get(pk=int(lfuID))
        print(lfu.replies)
        replies = []
        if lfu.replies:
            replies = Reply.objects.filter(pk__in=lfu.replies).order_by('created_at').reverse()
        return render(req, 'lfuPage.html', {
            'lfu': lfu,
            'replies': replies
        })
    except:
        return render(req, '404.html')


def addReply(req, lfuID):
    user = Person.objects.get(username=req.session.get('user'))
    newReply = Reply(text=req.POST['text'], user_id=user.id, created_at=datetime.datetime.now())
    newReply.save()
    lfu = LookingForYou.objects.get(pk=int(lfuID))
    if lfu.replies is None:
        lfu.replies = []
    lfu.replies.append(newReply.id)
    lfu.save()

    notification = Notification(lfu_id=lfu.id,
                                text=f'User {user.username} replied to one of <a href="/lfu/{lfu.id}">lfu</a> you are following')
    notification.save()
    return redirect(f'/lfu/{lfuID}')


def logout(req):
    req.session.delete()
    return redirect('index')


def newsPost(req, newsId):
    try:
        news = Post.objects.get(pk=int(newsId))
        return render(req, 'newsPage.html', {
            'news': news
        })
    except:
        return render(req, '404.html')


def addFeedback(req):
    email = req.POST['email']
    text = req.POST['feedback']
    feedback = Feedback(email=email, text=text)
    feedback.save()
    return render(req, 'index.html', {
        'alerts':
            [
                {
                    'type': 'success',
                    'title': 'Success:',
                    'text': 'Thanks for your feedback!'
                }
            ]
    })


def followlFU(req, lfuID):
    LookingForYou.objects.get(pk=lfuID)
    if LookingForYou:
        user = Person.objects.get(username=req.session.get('user'))
        user.followed.append(lfuID)
        user.save()
        LFUs = LookingForYou.objects.all().order_by('created_at').reverse()
        return render(req, 'aituLFU.html', {
            'alerts':
                [
                    {
                        'type': 'success',
                        'title': 'Success:',
                        'text': f'Now you are following LFU ID({lfuID})',
                    }
                ],
            'LFUs': LFUs,
        })
    return redirect('aituLFU')
