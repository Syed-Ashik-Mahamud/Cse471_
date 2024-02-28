from django.shortcuts import redirect, render
from home.models import ResetPwdTokens, UserContact, UserModel
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db import connection
import time
import uuid
from lost_and_found.mail_service import send_claim_acception_mail, send_claim_rejection_mail, send_forget_password_mail, send_point_purchase_mail, send_point_success_mail
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.http import HttpResponse

from django.template.loader import get_template

from xhtml2pdf import pisa




# home function


def home(request):
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM user_posts ORDER BY id DESC;')
    allPosts = cursor.fetchall()
    cursor.close()
    search = "All"
    try:
        user = UserModel.objects.get(email=request.session['email'])
        if request.method == 'POST':
            search = request.POST.get('locatn')
            if search:
                print(search)
                if search == "All":
                    cursor = connection.cursor()
                    cursor.execute(
                        'SELECT * FROM user_posts ORDER BY id DESC;')
                    posts = cursor.fetchall()
                    cursor.close()
                    locations = []
                    for post in allPosts:
                        locations.append(post[5])
                    locations = list(dict.fromkeys(locations))
                    locations.sort()
                    return render(request, 'home.html', {'posts': posts, 'locations': locations, 'user': user, 'search': search})
                else:
                    cursor = connection.cursor()
                    cursor.execute(
                        'SELECT * FROM user_posts WHERE location = %s ORDER BY id DESC;', [search])
                    posts = cursor.fetchall()
                    cursor.close()
                    locations = []
                    for post in allPosts:
                        locations.append(post[5])
                    locations = list(dict.fromkeys(locations))
                    locations.sort()
                    return render(request, 'home.html', {'posts': posts, 'locations': locations, 'user': user, 'search': search})
            else:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT * FROM user_posts ORDER BY id DESC;')
                posts = cursor.fetchall()
                cursor.close()
                locations = []
                for post in allPosts:
                    locations.append(post[5])
                locations = list(dict.fromkeys(locations))
                locations.sort()
                return render(request, 'home.html', {'posts': posts, 'locations': locations, 'user': user, 'search': search})
        else:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM user_posts ORDER BY id DESC;')
            posts = cursor.fetchall()
            cursor.close()
            locations = []
            for post in allPosts:
                locations.append(post[5])
            locations = list(dict.fromkeys(locations))
            locations.sort()
            return render(request, 'home.html', {'posts': posts, 'locations': locations, 'user': user, 'search': search})
    except:
        if request.method == 'POST':
            search = request.POST.get('locatn')
            if search:
                print(search)
                if search == "All":
                    cursor = connection.cursor()
                    cursor.execute(
                        'SELECT * FROM user_posts ORDER BY id DESC;')
                    posts = cursor.fetchall()
                    cursor.close()
                    locations = []
                    for post in allPosts:
                        locations.append(post[5])
                    locations = list(dict.fromkeys(locations))
                    locations.sort()
                    return render(request, 'home.html', {'posts': posts, 'locations': locations, 'search': search})
                else:
                    cursor = connection.cursor()
                    cursor.execute(
                        'SELECT * FROM user_posts WHERE location = %s ORDER BY id DESC;', [request.POST.get('locatn')])
                    posts = cursor.fetchall()
                    cursor.close()
                    locations = []
                    for post in allPosts:
                        locations.append(post[5])
                    locations = list(dict.fromkeys(locations))
                    locations.sort()
                    return render(request, 'home.html', {'posts': posts, 'locations': locations, 'search': search})
            else:
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT * FROM user_posts ORDER BY id DESC;')
                posts = cursor.fetchall()
                cursor.close()
                locations = []
                for post in allPosts:
                    locations.append(post[5])
                locations = list(dict.fromkeys(locations))
                locations.sort()
                return render(request, 'home.html', {'posts': posts, 'locations': locations, 'search': search})
        else:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT * FROM user_posts ORDER BY id DESC;')
            posts = cursor.fetchall()
            cursor.close()
            locations = []
            for post in allPosts:
                locations.append(post[5])
            locations = list(dict.fromkeys(locations))
            locations.sort()
            return render(request, 'home.html', {'posts': posts, 'locations': locations, 'search': search})


# authentication function

def authenticate(request):
    return render(request, 'authenticate.html')


# admin login function

def admin_login(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        if request.method == 'POST':
            if request.POST.get('adminUsername') and request.POST.get('adminPass'):
                username = request.POST.get('adminUsername')
                password = request.POST.get('adminPass')
                if username == 'admin' and password == 'admin':
                    return redirect('admin-panel')
                else:
                    messages.error(request, 'Password incorrect...!')
                    return render(request, 'admin_login.html', {'user': user})
        return render(request, 'admin_login.html', {'user': user})
    except:
        messages.error(request, 'You need to login first')
        return redirect('authenticate')


def signup(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('email') and request.POST.get('password'):
            saveUser = UserModel()
            saveToken = ResetPwdTokens()

            saveUser.name = request.POST.get('name')
            saveUser.email = request.POST.get('email')
            saveUser.password = make_password(request.POST.get('password'))
            saveUser.completeProfile = '25%'
            saveUser.point = '200'

            if saveUser.isExists():
                messages.error(
                    request, request.POST.get('email') + " email address already registered...! Please Log in.")
                # return render(request, 'authenticate.html', context)
                return redirect('../authenticate')
            else:
                saveUser.save()
                saveToken.user = saveUser
                saveToken.save()
                messages.success(
                    request, "Hello " + request.POST.get('name') + ", registration details saved successfully...! Please Log in now.")
                return redirect('../authenticate')
    else:
        return redirect('../authenticate')


# sign in function

def login(request):
    if request.method == 'POST':
        try:
            userDetail = UserModel.objects.get(
                email=request.POST.get('email'))
            if check_password(request.POST.get('password'), (userDetail.password)):
                request.session['email'] = userDetail.email
                return redirect('/')
            else:
                messages.error(
                    request, 'Password incorrect...!')
        except UserModel.DoesNotExist as e:
            messages.error(
                request, 'No user found of this email....!')
    return redirect('../authenticate')


# logout function

def logout(request):
    try:
        del request.session['email']
        messages.success(request, "Successfully logged out.")
    except:
        messages.error(request, "An error occurred. Try again.")
        return redirect('/')
    return redirect('/')


# privacy policy function

def privacy_policy(request):
    return render(request, 'privacy_policy.html')


# terms & conditions function

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

# view profile page


def view_profile(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])
        return render(request, 'view_profile.html', {'user': user})
    except:
        messages.error(request, 'You need to login first')
        return redirect('authenticate')





# contact function


def contact(request):
    try:
        user = UserModel.objects.get(email=request.session['email'])

        if request.method == 'POST':
            if request.POST.get('txtname') and request.POST.get('txtEmail') and request.POST.get('txtMsg'):
                saveContact = UserContact()

                saveContact.messengerId = user.id
                saveContact.messengerName = user.name
                saveContact.messengerEmail = user.email
                saveContact.message = request.POST.get('txtMsg')

                saveContact.save()
                time.sleep(3)
                return redirect('/')
        else:
            return render(request, 'contact.html', {'user': user})
    except:
        messages.error(request, 'You need to login first')
        return redirect('authenticate')






# reset password functon


def forget_password(request):
    try:
        if request.method == 'POST' and request.POST.get('resetEmail'):
            email = request.POST.get('resetEmail')

        if not UserModel.objects.filter(email=email).first():
            messages.error(request, 'No user found with this email.')
            return render(request, 'reset_password/forget-password.html')

        user_obj = UserModel.objects.get(email=email)
        token = str(uuid.uuid4())
        resetPwdToken_obj = ResetPwdTokens.objects.get(user=user_obj.id)
        resetPwdToken_obj.forget_password_token = token
        resetPwdToken_obj.save()
        send_forget_password_mail(user_obj.email, token)
        messages.success(request, 'An email has been sent to ' + user_obj.email +
                         '. If you don\'t find any email in your mailbox, please check spam folder.')
        return render(request, 'reset_password/forget-password.html')

    except Exception as e:
        print(e)
    return render(request, 'reset_password/forget-password.html')

# change password functon


def change_password(request, token):
    context = {}

    try:
        resetPwdToken_obj = ResetPwdTokens.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': resetPwdToken_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.error(request, 'No user id found.')
                return render(request, f'reset_password/change-password/{token}/.html', context)

            if new_password != confirm_password:
                messages.error(request, 'both should be equal.')
                return render(request, f'reset_password/change-password/{token}/.html', context)

            user_obj = UserModel.objects.filter(id=user_id).first()
            user_obj.password = make_password(new_password)
            user_obj.save()
            messages.success(request, 'Password updated.')
            return render(request, 'reset_password/change-password.html', context)
        else:
            return render(request, 'reset_password/change-password.html', context)

    except Exception as e:
        print(e)
        messages.error(request, 'url has already been used.')
        return render(request, 'reset_password/change-password.html', context)


