from flask import *
from extensions import db

main = Blueprint('main', __name__, template_folder='templates', url_prefix='/fbpliijy/p1')

@main.route('/')
def main_route():
    cur = db.cursor()
    cur.execute('SELECT * FROM User')
    results = cur.fetchall()

    options = {
        "usernames": results,
    }

    return render_template("index.html", **options)