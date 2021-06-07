import io
from werkzeug.utils import secure_filename
from flask import request, send_file
from app import app, db
from .models import Img


@app.errorhandler(413)
def size_to_big(error):
    return 'Image must be smaller than 2 Mb', 413


@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']

    if not pic:
        return 'No pic uploaded', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype

    if filename.rsplit('.', 1)[1].lower() not in app.config['ALLOWED_EXTENSIONS']:
        return 'Image must be in jpg, jpeg or png', 400

    img = Img(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()

    return 'Image has been uploaded'


@app.route('/images/<id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return f'No image with id={id}', 404

    return send_file(
        io.BytesIO(img.img),
        mimetype=img.mimetype,
        attachment_filename='%s' % img.name
    )