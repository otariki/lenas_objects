from django.shortcuts import render, redirect
from django.conf import settings
from helpers.db_connect import my_db
from helpers.functions import funcs
from helpers.accounts import accounts_helper



def list_re_objects(request):
    r = accounts_helper().validate_user_session(request)
    if r < 0:
        return redirect(settings.SITE_DOMAIN+"/auth")

    conn = my_db().conn()

    v_sql_params = []
    v_region = request.GET.get('region')
    v_municipality = request.GET.get('municipality')
    v_rooms_cnt = request.GET.get('rooms_cnt')

    v_sql = "SELECT id, region, rooms_cnt, addres  FROM re_objects WHERE TRUE   "
    if v_region != None:
        v_sql = v_sql+" AND region = %s "
        v_sql_params.append(v_region)
    if v_rooms_cnt != None and funcs().ctype_digit(v_rooms_cnt) == True:
        v_sql = v_sql+" AND rooms_cnt = %s "
        v_sql_params.append(v_rooms_cnt)

    v_sql = v_sql +"ORDER BY id DESC "


    conn.execute(v_sql, v_sql_params)
    # res = conn.fetchall()
    re_objects_res = my_db().dictfetchall(conn)

    data = {
        "site_domain": settings.SITE_DOMAIN,
        "auth_user_id": request.session.get('user_id'),
        "auth_user_name": request.session.get('user_name'),
        "auth_user_status_id": request.session.get('user_status_id'),
        "a": "aaa",
        "re_objects": re_objects_res

    }
    return render(request, 'list_of_re_objects.html', data)