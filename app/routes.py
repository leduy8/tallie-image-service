import io
from werkzeug.utils import secure_filename
from flask import request, send_file, jsonify
from app import app, db
from .models import Img


@app.errorhandler(413)
def size_too_big(error):
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

    return jsonify(
        message='Image has been uploaded successfully',
        id=img.id
    )


@app.route('/upload_multiple', methods=['POST'])
def upload_multiple():
    pics = request.files.getlist('pic')

    pic_list = []

    for pic in pics:
        if not pic:
            return 'No pic uploaded', 400

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        if filename.rsplit('.', 1)[1].lower() not in app.config['ALLOWED_EXTENSIONS']:
            return 'Image must be in jpg, jpeg or png', 400

        img = Img(img=pic.read(), mimetype=mimetype, name=filename)
        db.session.add(img)
        db.session.commit()
        
        pic_list.append({
            'id': img.id
        })

    return jsonify(
        message='Image has been uploaded successfully',
        data=pic_list
    )


@app.route('/images/<id>')
def get_image(id):
    img = Img.query.filter_by(id=id).first()
    
    if not img:
        return f'No image with id={id}', 404

    return send_file(
        io.BytesIO(img.img),
        mimetype=img.mimetype,
        attachment_filename='%s' % img.name
    )


@app.route('/images/<id>/delete', methods=['DELETE'])
def delete_image(id):
    img = Img.query.filter_by(id=id).first()

    if not img:
        return f'No image with id={id}', 404

    db.session.delete(img)
    db.session.commit()
    return jsonify('Image has been deleted.')