from mci import app


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=7777, ssl_context=("fullchain1.pem", 'privkey1.pem'))