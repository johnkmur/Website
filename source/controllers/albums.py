from flask import *
from extensions import db
import os

albums = Blueprint('albums', __name__, template_folder='templates', url_prefix='/fbpliijy/p1')

@albums.route('/albums/edit', methods=['GET', 'POST'])
def albums_edit_route():
	options = {
		"edit": True,
	}
	cur = db.cursor()
	
	if request.method == 'GET':
		user = request.args.get('username')
		cur.execute("SELECT * FROM Album WHERE username= %s;", (user,))
		results = cur.fetchall()
		options['albums'] = results
		options['username'] = user

	elif request.method == 'POST':
		user = request.form['username']
		if request.form['op'] == "delete":
			albumid = request.form['albumid']
			cur.execute("SELECT * FROM Photo JOIN Contain ON Contain.picid = Photo.picid WHERE Contain.albumid = %s;",(albumid,))
			results = cur.fetchall()
			cur.execute("DELETE FROM Album WHERE albumid = %s",(albumid,))
			for result in results:
				picid = result['picid']
				format = result['format']
				cur.execute("DELETE FROM Photo WHERE picid = %s",(picid,))
				os.remove('static/images/'+ picid +'.'+ format)
			db.commit()
		elif request.form['op'] == "add":
			title = request.form['title']
			cur.execute('INSERT INTO Album VALUES(DEFAULT, %s, DEFAULT, DEFAULT, %s)', (title, user))
			db.commit()
		return redirect(url_for('albums.albums_edit_route',username=user))

	return render_template("albums.html", **options)

@albums.route('/albums', methods=['GET'])
def albums_route():
	user = request.args.get('username')

	cur = db.cursor()
	cur.execute("SELECT * FROM Album WHERE username='%s'" % user)
	results = cur.fetchall()

	options = {
		"edit": False,
		"username": user,
		"albums": results,
	}
	return render_template("albums.html", **options)