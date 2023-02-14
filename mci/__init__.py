# from flask import Flask
# from werkzeug.utils import secure_filename
# import sqlite3 as sql
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #tensorflow warning 끄는 용
# import ssl
# import warnings
# warnings.simplefilter("ignore", UserWarning)

# # SECRET_KEY = config.SECRET_KEY



# def create_app():
#     app = Flask(__name__)
#     # app.secret_key=SECRET_KEY
#     app.config.from_envvar('APP_CONFIG_FILE')
#     context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#     context.load_cert_chain('fullchain1.pem', 'privkey1.pem')

    

#     from .views import main_views, first_test, second_test, third_test, fourth_test, fifth_test, sixth_test, result
#     app.register_blueprint(main_views.bp)
#     app.register_blueprint(first_test.bp)
#     app.register_blueprint(second_test.bp)
#     app.register_blueprint(third_test.bp)
#     app.register_blueprint(fourth_test.bp)
#     app.register_blueprint(fifth_test.bp)
#     app.register_blueprint(sixth_test.bp)
#     app.register_blueprint(result.bp)

#     return app

# app = create_app()

# if __name__ == '__main__':
  
#     app.run(host='0.0.0.0', port=7777, ssl_context=("fullchain1.pem", 'privkey1.pem'))