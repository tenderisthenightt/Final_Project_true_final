from flask import Blueprint, render_template

bp = Blueprint('result', __name__, url_prefix='/')

@bp.route('/result')
def result():
    return render_template('dashboard.html')