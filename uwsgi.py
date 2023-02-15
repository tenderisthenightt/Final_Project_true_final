from mci import app


if __name__ == "__main__":
    app.app.run(host='0.0.0.0', debug=True, port=7777, ssl_context=("fullchain1.pem", 'privkey1.pem'))