from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.backends.db import SessionStore
from django.http import JsonResponse
import urllib.parse


from helpers.db_connect import my_db
from helpers.functions import funcs
from helpers.accounts import accounts_helper
import re
import datetime



def reg_htm(request):
    data = {
        "a":"aaa",
        "get_param__msg": request.GET.get('msg'),
        "get_param__err": request.GET.get('err'),
    }

    return render(request, 'reg.html', data)


def reg_process_check_email_username(request):
    conn = my_db().conn()
    if (request.method != 'POST'):
        return JsonResponse({'res': 'error_1'})

    v_email = request.POST.get('email')
    v_user_name = request.POST.get('user_name')

    conn.execute("SELECT email, user_name FROM users WHERE email = %s OR user_name = %s", [v_email, v_user_name])
    res = conn.fetchall()
    if len(res) == 1:
        if v_email == res[0][0]:
            return JsonResponse({'res': 'error_2'})
        if v_user_name == res[0][1]:
            return JsonResponse({'res': 'error_3'})

    return JsonResponse({'res': 'success'})


def reg_process(request):
    data = {"a":"aaa"}

    if (request.method != 'POST'):
        return redirect(settings.SITE_DOMAIN+"/reg")

    conn = my_db().conn()
    v_reg_code = request.POST.get('reg_code')

    conn.execute("SELECT code FROM reg_code")
    res_reg_code = conn.fetchall()
    if v_reg_code != res_reg_code[0][0]:
        return redirect(settings.SITE_DOMAIN + "/reg?err=-1")

    v_user_name = request.POST.get('user_name')
    if len(v_user_name.strip()) < 2:
        return redirect(settings.SITE_DOMAIN + "/reg?err=-2")

    v_email = request.POST.get('email')
    # ct = datetime.datetime.now()
    # # print("current time:-", ct)
    #
    # # ts store timestamp of current time
    # ts = ct.timestamp()
    # v_confirm_email_hash = funcs().md5(v_email+"#@!"+str(ts))
    v_confirm_email_hash = accounts_helper().generate_email_activation_hash(v_email)
    v_link_for_email = settings.SITE_DOMAIN+"/reg_email_confirm?h="+v_confirm_email_hash
    print("v_link_for_email:"+v_link_for_email)


    v_pass = request.POST.get('pass')
    if v_pass == None or len(v_pass) < 8:
        return redirect(settings.SITE_DOMAIN + "/reg?err=-3")

    if re.search(r'[0-9]+', v_pass) == None or re.search(r'[a-z]+', v_pass) == None or re.search(r'[A-Z]+', v_pass) == None:
        return redirect(settings.SITE_DOMAIN + "/reg?err=-4")


    hashed_pwd = make_password(v_pass)

    try:
        conn.execute("INSERT INTO users"
                     "(user_name, email, pass, confirm_email_hash)"
                     "VALUES"
                     "(%s, %s, %s, %s)", [v_user_name, v_email, hashed_pwd, v_confirm_email_hash])
    except Exception as e:
        if 'users_email_uniqix' in repr(e):
            return redirect(settings.SITE_DOMAIN + "/reg?err=-5")
        if 'users_user_name_uniqix' in repr(e):
            return redirect(settings.SITE_DOMAIN + "/reg?err=-6")




    # !!! here send email activation link "v_link_for_email"  to   to "v_email"
    #  accounts_helper().send_email_activation_link(v_email, v_link_for_email
    return redirect(settings.SITE_DOMAIN + "/reg?err=1")


def send_email_activation_hash(request):
    # email activation hash atumatically sending when user  registers, but this is function, if user needs to send code again
    if (request.method != 'POST'):
        return JsonResponse({'res': 'error_1'})

    v_email = request.POST.get('email')

    conn = my_db().conn()
    conn.execute("SELECT 1 FROM users WHERE status_id = 0 AND email = %s", [v_email])
    res = conn.fetchall()
    if len(res) != 1:
        return JsonResponse({'res': 'error_2'})

    v_confirm_email_hash = accounts_helper().generate_email_activation_hash(v_email)
    v_link_for_email = settings.SITE_DOMAIN + "/reg_email_confirm?h=" + v_confirm_email_hash
    print("v_link_for_email:" + v_link_for_email)

    conn.execute("UPDATE users SET confirm_email_hash = %s WHERE email = %s", [v_confirm_email_hash, v_email])

    # !!! here send email activation link "v_link_for_email"  to   to "v_email"
    return JsonResponse({'res': 'success'})

def reg_email_confirm_process(request):
    v_confirm_email_hash = request.GET.get('h')
    if v_confirm_email_hash == None:
        return redirect(settings.SITE_DOMAIN + "/reg?err=ch1")

    if funcs().is_valid_md5(v_confirm_email_hash) == None:
        return redirect(settings.SITE_DOMAIN + "/reg?err=ch2")

    conn = my_db().conn()
    conn.execute("SELECT 1 FROM users WHERE status_id = 0 AND confirm_email_hash = %s", [v_confirm_email_hash])
    res = conn.fetchall()
    if len(res) == 0:
        return redirect(settings.SITE_DOMAIN + "/reg?err=ch3")
    else:
        conn.execute("UPDATE users SET  status_id = 1, confirm_email_hash = NULL  WHERE  confirm_email_hash = %s", [v_confirm_email_hash])
        return redirect(settings.SITE_DOMAIN + "/auth?msg=email_confirmed")



def auth_htm(request):
    data = {
        "a":"aaa",
        "get_param__msg": request.GET.get('msg'),
        "get_param__err": request.GET.get('err'),
        "site_domain": settings.SITE_DOMAIN,
    }

    v_url_email = request.GET.get('email')
    if v_url_email != None:
        data["url_email_for_activation"] = urllib.parse.unquote(v_url_email)

    return render(request, 'auth.html', data)



def auth_process(request):
    conn = my_db().conn()

    if (request.method != 'POST') :
        return redirect(settings.SITE_DOMAIN+"/reg")

    v_email = request.POST.get('email')
    v_pass = request.POST.get('pass')

    if v_email == None:
        return redirect(settings.SITE_DOMAIN + "/auth?err=no_user_found_10")

    conn.execute("SELECT id, pass, status_id, user_name FROM users WHERE email = %s", [v_email])
    res = conn.fetchall()

    if (len(res) != 1):
        return redirect(settings.SITE_DOMAIN + "/auth?err=no_user_found_1")


    if(check_password(v_pass, res[0][1]) != True):
        return redirect(settings.SITE_DOMAIN + "/auth?err=no_user_found_2")


    if(res[0][2] == -1): #user is  blocked
        return redirect(settings.SITE_DOMAIN + "/auth?err=no_user_found_3")

    if (res[0][2] == 0):  # user email not confirmed
        return redirect(settings.SITE_DOMAIN + "/auth?err=no_user_found_4&email="+urllib.parse.quote(v_email))


    request.session["user_id"] = res[0][0]
    request.session["user_status_id"] = res[0][2]
    request.session["user_name"] = res[0][3]

    return redirect(settings.SITE_DOMAIN + "/")
    #return redirect(settings.SITE_DOMAIN + "/auth?err=no_err")




def change_pass_send_email_htm(request):
    data = {
        "cp_send_email_get_param__msg": request.GET.get('msg'),
        "cp_send_email_get_param__err": request.GET.get('err')
    }
    return render(request, 'change_pass_send_email.html', data)

def change_pass_send_email(request):
    data ={}
    if (request.method != 'POST'):
        return redirect(settings.SITE_DOMAIN + "/reg")
    v_email = request.POST.get('email')
    conn = my_db().conn()
    conn.execute("SELECT id  FROM users WHERE email = %s AND status_id > 0", [v_email])
    res = conn.fetchall()
    if (len(res) != 1):
        return redirect(settings.SITE_DOMAIN + "/change_pass?err=no_email_found")

    ct = datetime.datetime.now()
    ts = ct.timestamp()

    v_change_pass_hash = funcs().md5(v_email+"#@!2"+str(ts))
    v_link_for_email = settings.SITE_DOMAIN + "/change_pass_process_htm?h=" + v_change_pass_hash
    print("v_link_for_email:" + v_link_for_email)

    conn.execute("UPDATE users SET change_pass_hash = %s WHERE email = %s ", [v_change_pass_hash, v_email])

    # !!! here send email activation link "v_link_for_email"  to   to "v_email"
    return redirect(settings.SITE_DOMAIN + "/change_pass?msg=email_sended")

def change_pass_process_htm(request):
    v_change_pass_hash = request.GET.get('h')
    if v_change_pass_hash == None:
        return redirect(settings.SITE_DOMAIN + "/change_pass?err=ch100")

    if funcs().is_valid_md5(v_change_pass_hash) == None:
        return redirect(settings.SITE_DOMAIN + "/change_pass?err=ch20")

    conn = my_db().conn()
    conn.execute("SELECT 1 FROM users WHERE status_id > 0 AND change_pass_hash = %s", [v_change_pass_hash])
    res = conn.fetchall()
    if len(res) != 1:
        return redirect(settings.SITE_DOMAIN + "/change_pass?err=ch30")
    else: # hash is valid, open password changing page
        data = {'change_pass_hash_value': v_change_pass_hash}
        return render(request, 'change_pass.html', data)



def change_pass_process(request):
    data ={}
    if (request.method != 'POST'):
        return redirect(settings.SITE_DOMAIN + "/reg")

    v_change_pass_hash = request.POST.get('change_pass_hash')
    if v_change_pass_hash == None or funcs().is_valid_md5(v_change_pass_hash) == None:
        return redirect(settings.SITE_DOMAIN + "/change_pass_process_htm?err=-30")

    v_pass = request.POST.get('pass')
    if v_pass == None or len(v_pass) < 8:
        return redirect(settings.SITE_DOMAIN + "/change_pass_process_htm?err=-3")

    if re.search(r'[0-9]+', v_pass) == None or re.search(r'[a-z]+', v_pass) == None or re.search(r'[A-Z]+', v_pass) == None:
        return redirect(settings.SITE_DOMAIN + "/change_pass_process_htm?err=-4")

    hashed_pwd = make_password(v_pass)
    conn = my_db().conn()
    conn.execute("UPDATE users SET "
                 "pass = %s, "
                 "change_pass_hash = NULL "
                 "WHERE "
                 "change_pass_hash = %s", [hashed_pwd, v_change_pass_hash])

    return redirect(settings.SITE_DOMAIN + "/auth?msg=pass_changed")



def logout_process(request):
    del request.session['user_id']
    del request.session['user_name']

    return redirect(settings.SITE_DOMAIN + "/")