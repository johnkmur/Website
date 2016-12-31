from flask import *
from extensions import db
from werkzeug.utils import secure_filename
import os
import hashlib

UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif', 'PNG', 'JPG', 'BMP', 'GIF'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

album = Blueprint('album', __name__, template_folder='templates', url_prefix='/fbpliijy/p1')

@album.route('/album/edit', methods=['GET','POST'])
def album_edit_route():
	options = {
		"edit": True,
	}
	cur = db.cursor()

	if request.method == 'GET':
		album_id = request.args.get('albumid')
		cur.execute("SELECT * FROM Photo JOIN Contain ON Contain.picid = Photo.picid WHERE Contain.albumid = %s;", (album_id,))
		results = cur.fetchall()

		options['pictures'] = results;
		for picture in options['pictures']:
			picture['route'] = 'images/' + picture['picid'] + '.' + picture['format']
		options['album_id'] = album_id

	elif request.method == 'POST':
		album_id = request.form['albumid']
		if request.form['op'] == "delete":
			pic_id = request.form['picid']
			cur.execute("SELECT * FROM Photo WHERE picid = %s;",(pic_id,))
			results = cur.fetchone()
			picformat = results['format']
			cur.execute("DELETE FROM Photo WHERE picid = %s;",(pic_id,))
			os.remove(UPLOAD_FOLDER + pic_id + '.' + picformat)
			cur.execute("UPDATE Album SET lastupdated = CURRENT_TIMESTAMP WHERE albumid = %s;",(album_id,))
			db.commit()
			return redirect(url_for('album.album_edit_route',albumid=album_id))
		elif request.form['op'] == "add":
			# check if the post request has the file part
			if 'file' not in request.files:
				flash('No file part')
				return redirect(url_for('album.album_edit_route',albumid=album_id))
			file = request.files['file']
			# if user does not select file, browser also
			# submit a empty part without filename
			if file.filename == '':
				flash('No selected file')
				return redirect(url_for('album.album_edit_route',albumid=album_id))
			if file and allowed_file(file.filename):
				#make hash
				m = hashlib.md5()
				dot = file.filename.find('.')
				flname = file.filename[0:dot-1]
				flformat = file.filename[dot+1:len(file.filename)]
				m.update(str(album_id))
				m.update(flname)
				pic_id = m.hexdigest()

				#find sequence number
				cur.execute("SELECT sequencenum FROM Contain;")
				results = cur.fetchall()
				for obj in results:
					numbers = [obj['sequencenum']]
				seqnum = max(numbers) + 1

				cur.execute("INSERT INTO Photo VALUES(%s, %s, CURRENT_TIMESTAMP);",(str(pic_id),flformat))
				cur.execute("INSERT INTO Contain VALUES(%s, %s, %s, '');",(seqnum, album_id, pic_id))

				cur.execute("UPDATE Album SET lastupdated = CURRENT_TIMESTAMP WHERE albumid = %s;",(album_id,))

				filename = secure_filename(pic_id + '.' + flformat)
				file.save(UPLOAD_FOLDER + filename)
				db.commit()
				return redirect(url_for('album.album_edit_route',albumid=album_id))

	return render_template("album.html", **options)

@album.route('/album', methods=['GET'])
def album_route():
	options = {
		"edit": False
	}
	cur = db.cursor()

	album_id = request.args.get('albumid')
	cur.execute("SELECT * FROM Photo JOIN Contain ON Contain.picid = Photo.picid WHERE Contain.albumid = %s;", (album_id,))
	results = cur.fetchall();
	options['pictures'] = results
	options['album_id'] = album_id
	for picture in options['pictures']:
			picture['route'] = 'images/' + picture['picid'] + '.' + picture['format']

	return render_template("album.html", **options)

