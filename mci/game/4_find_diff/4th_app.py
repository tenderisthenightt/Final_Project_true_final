from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
#import sqlite3 as sql
import os
import random

app = Flask(__name__)


# html 렌더링
@app.route('/',  methods=['POST','GET'])
def wrong_img():
    # 랜덤으로 텍스트 보내기
    random_class =random.sample(['나비','지렁이','컴퓨터'], 3)
    for i in random_class :
        random_list = [i+'1', i+'2',i+'3',i+'X']
        random_list_2 = []
        for  j in random.sample(random_list, 4):
            random_list_2.append(j)
        img1 = random_list_2[0]
        img2 = random_list_2[1]
        img3 = random_list_2[2]
        img4 = random_list_2[3]
    
   
    # 누른 버튼의 text 를 받아서 정답인지 오답인지 판별하기
    point =[]
    if request.method == 'POST':
        image = str(request.form['button'])
        if 'X' in image:
            point.append('정답')
        else: point.append('오답')
        
    return render_template('4th_test.html',img1 = img1, img2=img2,img3=img3,img4=img4)


if __name__ == '__main__':
    app.run(debug=True)  