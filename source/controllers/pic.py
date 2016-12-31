from flask import *
from extensions import db

pic = Blueprint('pic', __name__, template_folder='templates', url_prefix='/fbpliijy/p1')


@pic.route('/pic', methods=['GET'])
def pic_route():
	options = {
		"edit": False
	}
	cur = db.cursor()

	pic_id = request.args.get('picid')

	cur.execute("SELECT * FROM Photo WHERE Photo.picid = %s", (pic_id,))
	results = cur.fetchone()
	cur.execute("SELECT * FROM Contain WHERE Contain.picid = %s", (pic_id,))
	albumid = cur.fetchone()['albumid']

	cur.execute("SELECT sequencenum FROM Contain WHERE Contain.picid = %s", (pic_id,))
	current_seqnum = cur.fetchone()['sequencenum']
	cur.execute("SELECT * FROM Contain WHERE Contain.sequencenum = (SELECT min(Contain.sequencenum) FROM Contain WHERE Contain.albumid = "+str(int(albumid))+" AND Contain.sequencenum > "+str(int(current_seqnum))+" )")
	next_pic = cur.fetchone()
	cur.execute("SELECT * FROM Contain WHERE Contain.sequencenum = (SELECT max(Contain.sequencenum) FROM Contain WHERE Contain.albumid = "+str(int(albumid))+" AND Contain.sequencenum < "+str(int(current_seqnum))+" )")
	prev_pic = cur.fetchone()

	print(albumid)

	if (prev_pic is None or prev_pic['albumid'] != albumid):
		options['prev_id'] = results
	else:
		options['prev_id'] = prev_pic

	if (next_pic is None or next_pic['albumid'] != albumid):
		options['next_id'] = results
	else:
		options['next_id'] = next_pic

	options['pictures'] = results
	options['pictures']['route'] = 'images/' + pic_id + '.' + results['format']
	options['album_id'] = albumid
	
	
	return render_template("pic.html", **options)


