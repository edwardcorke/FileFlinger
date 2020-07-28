from flask import render_template, url_for, flash, redirect, request, send_file
from serv import app, db, key
from serv.models import Upload
from serv.forms import UploadFile
from serv.encryptDecrypt import encrypt, decrypt
import secrets, datetime, sys, os, io


@app.route("/",  methods=['GET', 'POST'])
@app.route("/home",  methods=['GET', 'POST'])
@app.route("/index",  methods=['GET', 'POST'])
@app.route("/upload",  methods=['GET', 'POST'])
def home():
    uploadForm = UploadFile()
    if uploadForm.validate_on_submit():
        fileReceived = request.files['file']

        if fileReceived.filename == '':
            flash('No selected file')
            return redirect(url_for('home'))

        hashname = saveUpload(fileReceived, uploadForm)
        flash("Happy sharing! Here's the link: " "\"localhost:5000/v/" + hashname + "\"", 'success')

        return redirect(url_for('home')) # TODO: deleted forward to thanks page
    return render_template('home.html', title="Home Page", form=uploadForm)


@app.route('/v/<downloadToken>')
def download(downloadToken):
    search = Upload.query.filter_by(hashname=downloadToken).first()
    if search is None:
        flash("Sorry this is a deadlink")
        return redirect(url_for('home'))

    if search.status == 0:
        flash("Sorry this file has expired and is unavailable")
        return redirect(url_for('home'))

    try:
        filepath = app.config['UPLOAD_FOLDER']
        filename = search.hashname
        fileToSend = open(os.path.join(filepath, filename), "rb")
        fileToSend = decrypt(fileToSend.read(), key)
        return send_file(io.BytesIO(fileToSend), attachment_filename=search.filename, as_attachment=True)
    except:
        flash("Server issue - our apologies we cannot locate the file")
        print("Error: " + str(sys.exc_info()[0]) + " for file: \'" + search.filename + "\' (uploaded by " + search.uploaderEmail + ")")  # TODO: log message & raise correct HTTP code
        return redirect(url_for('home'))


@app.route("/thanks")
def thanks():
    return 'Thanks for uploading'


def saveUpload(fileReceived, uploadForm):

    encrypted_data = encrypt(fileReceived.read(), key)

    hashname = secrets.token_hex(6)
    while Upload.query.filter_by(hashname=hashname).first() is not None:
        hashname = secrets.token_hex(6)
    uploadInstance = Upload(filename=fileReceived.filename, hashname=hashname, datetime=datetime.date.today(),
                            uploaderEmail=uploadForm.email.data, message=uploadForm.message.data)
    db.session.add(uploadInstance)
    db.session.commit()

    filename = app.config['UPLOAD_FOLDER'] + hashname

    with open(filename, "wb") as file:
        file.write(encrypted_data)
    return hashname
