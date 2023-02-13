from flask import Blueprint, render_template, session

bp = Blueprint('main', __name__, url_prefix='/')

import string
import random

def pw_maker():
    new_pw_len = 32 # 새 비밀번호 길이
 
    pw_candidate = string.ascii_letters + string.digits
    
    new_pw = ""
    for i in range(new_pw_len):
        new_pw += random.choice(pw_candidate)
 
    return new_pw



@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/intro')
def intro():
    session.clear()
    guest = pw_maker()
    session['guest']=guest
    print(guest)
    return render_template('0_intro.html')

@bp.route('/aboutus')
def aboutus():
    session.clear()
    return render_template('aboutus.html')

@bp.route('/abouttest')
def abouttest():
    session.clear()
    return render_template('abouttest.html')