from flask import Blueprint, render_template, request, session

bp = Blueprint('first', __name__, url_prefix='/')



# 1st test
import keras.applications as kapp
import keras.models as kmodels
import numpy as np
import keras.utils as utils
from ..module.anchor import *
import sqlite3

vgg_model = kapp.VGG16(weights='imagenet', include_top=False)
model = kmodels.Model(inputs=vgg_model.input, outputs=vgg_model.get_layer('block5_pool').output)
anch = ''

def get_image_feature(image):
    img = utils.load_img(image, target_size=(224, 224))
    img = utils.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = kapp.vgg16.preprocess_input(img)
    features = model.predict(img)
    features = features.flatten()
    return features

@bp.route("/vgg")
def similarity_image():
    q, p_path, h_path, sim = random_sim()
    global anch
    anch = q
    print(anch)
    return render_template('1st_test.html', h_path=h_path)

@bp.route("/image_similarity", methods=["POST"])
def image_similarity():
 
    print('1111111111111111')
    # 이미지 받기(blob)
    if request.method == 'POST':
        guest = str(session['guest'])
        image = request.files["image"]
        # Save image_binary to a file or a variable
        img_path = 'drawing/sim/' + guest + '.png'
        image.save(img_path)
        print('222222222222222222')
        global anch
        print(anch)
        global anchor
        p_path = anchor[anch][0]
        sim = anchor[anch][2]


    print('333333333333333')
    

    features1 = get_image_feature(p_path)
    features2 = get_image_feature(img_path)
    print('44444444444444')
    cosine_similarity = np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))
    print(cosine_similarity)
    print(sim)
   
    # db 저장하기
    OX = []
    if cosine_similarity >= sim:
        OX.append(1)
    else: OX.append(0) 
    print(OX)
   

    # DB 생성 / 이미 있으면 나중에 주석처리하기.
    # isolation_level = None (auto commit)
    conn = sqlite3.connect('ijm.db', isolation_level=None)
    # 커서
    cursor = conn.cursor()
    # 테이블 생성(데이터 타입 = TEST, NUMERIC, INTEGER, REAL, BLOB(image) 등)
    # 필드명(ex. name) -> 데이터 타입(ex. text) 순서로 입력 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sim_Test (
        session TEXT PRIMARY KEY NOT NULL,
        game text,
        point float,
        OX integer
        )""")

    # db 에 정보 저장
    game = 'Sim_Test'
    point = float(cosine_similarity)
    OX = OX[0]

    cursor.execute("""
        INSERT INTO Sim_Test (session, game, point, OX) VALUES (?,?,?,?)          
        """, (guest, game, point, OX)
        )

    conn.commit()
    cursor.close()
    conn.close()
    guest = session['guest']
    print(guest)
    return render_template('2nd_test.html')