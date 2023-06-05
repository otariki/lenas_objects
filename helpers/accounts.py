from helpers.db_connect import my_db
from helpers.functions import funcs
import datetime
#from django.conf import settings

class accounts_helper():
    def validate_user_session(self, req):
        user_id = req.session.get('user_id')

        # user_id should exists in session and be digit, otherwise non valid user
        if funcs().ctype_digit(user_id) == False:
            return -1

        conn = my_db().conn()
        conn.execute("SELECT status_id FROM users WHERE id = "+str(user_id))
        res = conn.fetchall()

        # user not found by session id (should never happen)
        if len(res) != 1:
            return -2

        # user is inactive or blocked
        if res[0][0] < 1:
            return -3



        # user is valid:
        return 1


    def generate_email_activation_hash(self, v_email):
        ct = datetime.datetime.now()
        # print("current time:-", ct)

        # ts store timestamp of current time
        ts = ct.timestamp()
        v_confirm_email_hash = funcs().md5(v_email + "#@!" + str(ts))
        return v_confirm_email_hash

    def send_email_activation_link(self, v_email, v_link):
        v_email_content = "bla bla "+v_link+ " bla2"
        # send v_email_content to "v_email"
