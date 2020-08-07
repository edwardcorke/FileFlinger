from flask import render_template, url_for, flash, redirect, request, send_file, session
 # TODO: from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.exceptions import InternalServerError
from flask_login import login_user, logout_user, current_user, login_required, user_logged_out
from serv import app, db, key, bcrypt
from serv.models import Upload, User
from serv.forms import UploadFile, RegisterForm, LoginForm, DownloadPasswordForm
from serv.encryptDecrypt import encrypt, decrypt
import secrets, datetime, sys, os, io
from hurry.filesize import size, si


@app.route("/",  methods=['GET', 'POST'])
@app.route("/home",  methods=['GET', 'POST'])
@app.route("/index",  methods=['GET', 'POST'])
@app.route("/upload",  methods=['GET', 'POST'])
def home():
    try:
        uploadForm = UploadFile()

        if uploadForm.validate_on_submit():
            fileReceived = request.files['file']

            # Check if file is blank
            if fileReceived.filename == '':
                flash('No selected file')
                return redirect(url_for('home'))

            expirationDatetime = datetime.date.today() + datetime.timedelta(uploadForm.expirationLength.data)

            hashname = saveUpload(fileReceived, uploadForm, expirationDatetime)
            downloadLink = "v/" + hashname

            # Save metadata to session
            # TODO: create JSON?
            session['downloadLink'] = downloadLink
            session['filename'] = fileReceived.filename
            session['uploader'] = uploadForm.email.data
            session['message'] = uploadForm.message.data
            session['expirationDatetime'] = expirationDatetime
            # TODO: display password on upload thanks page?

            return redirect(url_for('uploadThanks'))
        return render_template('home.html', title="Home Page", form=uploadForm)
    except ():
        # flash("File received too large- max: 2GB")  # TODO: log
        flash("Server error")
        return redirect(url_for('home'))


@app.route("/upload/thanks")
def uploadThanks():
    # Return to home if metadata has not been transferred over successfully from the upload page
    if 'filename' in session:
        return render_template("uploadThanks.html", downloadLink=session['downloadLink'], filename=session['filename'], uploader=session['uploader'], message=session['message'], filesize=size(session['filesize']), expirationDatetime=session['expirationDatetime'])
    print("Could not find session variables")  # TODO: log
    return redirect(url_for('home'))


@app.route("/v/<downloadToken>")
def downloadRedirect(downloadToken):
    session['downloadToken'] = downloadToken
    return redirect(url_for('downloadThanks'))


@app.route("/download/thanks", methods=['GET', 'POST'])
def downloadThanks():
    # Only show page if download token has been received successfully
    if 'downloadToken' in session:
        downloadLink = "/d/" + session['downloadToken']

        # Query database using hashname
        search = Upload.query.filter_by(hashname=session['downloadToken']).first()

        # Cannot find any matches from query
        if search is None:
            flash("Sorry this is a deadlink")
            return redirect(url_for('home'))

        # File flagged unavailable
        if search.status == 0:
            flash("Sorry this file has expired and is unavailable")
            return redirect(url_for('home'))

        passwordRequired = False
        if search.password is not "":
            passwordRequired = True
        passwordForm = DownloadPasswordForm()
        if passwordForm.validate_on_submit():
            session['download_password'] = passwordForm.password.data
            return redirect(downloadLink)

        return render_template('downloadThanks.html',
                               title="Thanks for downloading",
                               form=passwordForm,
                               passwordRequired=passwordRequired,
                               filename=search.filename,
                               uploader=search.uploaderEmail,
                               message=search.message,
                               filesize=size(search.filesize))
    return redirect(url_for('home'))


@app.route('/d/<downloadToken>')
def download(downloadToken):
    search = Upload.query.filter_by(hashname=downloadToken).first()

    # if password is required
    if search.password is not "":
        if 'download_password' not in session:
            flash("password required")
            return redirect(url_for('downloadThanks'))  # TODO: change redirect
        if not bcrypt.check_password_hash(search.password, session['download_password']):
           flash("Incorrect password")
           return redirect(url_for('downloadThanks'))  # TODO: change redirect

    # Decrypt file and send to client
    try:
       filepath = app.config['UPLOAD_FOLDER']
       filename = search.hashname
       fileToSend = open(os.path.join(filepath, filename), "rb")
       fileToSend = decrypt(fileToSend.read(), key)
       return send_file(io.BytesIO(fileToSend), attachment_filename=search.filename, as_attachment=True)
    except:
        flash("Server issue - our apologies we cannot locate the file")
        print("Error: " + str(sys.exc_info()[
                                 0]) + " for file: \'" + search.filename + "\' (uploaded by " + search.uploaderEmail + ")")  # TODO: log message & raise correct HTTP code
        return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerForm.password.data)  # TODO: UTF-8 needed?
        user = User(username=registerForm.username.data, email=registerForm.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("New user created", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=registerForm)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Make sure login page can only be accessed when the user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)  # TODO: add field to form?
            next_page = request.args.get('next')
            flash('Logged in')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful, Please check email and password')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out')
    return redirect(url_for('home'))


@app.route('/admin_portal')
@login_required
def admin_portal():
    if current_user.permLevel < 2:  # TODO: change number to config alias
        flash("Access to the admin portal area is restricted")
        return redirect(url_for('home'))

    data = db.session.execute("SELECT id, username, email, permLevel FROM User").fetchall()
    datab = db.session.execute("SELECT id, filename, hashname, filesize, datetime, expirationDatetime, uploaderEmail, message, status FROM Upload").fetchall()
    return render_template('admin_portal.html', data=data, datab=datab)

               
               
@app.route('/admin_portal/users')
@login_required
def view_users():
    if current_user.permLevel < 2:  # TODO: change number to config alias
        flash("Access to the admin portal area is restricted")
        return redirect(url_for('home'))

    userData = db.session.execute("SELECT id, username, email, permLevel FROM User").fetchall()
    return render_template('view_users.html', data=userData)


@app.route('/admin_portal/uploads')
@login_required
def view_uploads():
    if current_user.permLevel < 2:  # TODO: change number to config alias
        flash("Access to the admin portal area is restricted")
        return redirect(url_for('home'))

    userData = db.session.execute("SELECT id, filename, hashname, filesize, datetime, expirationDatetime, uploaderEmail, message, status FROM Upload").fetchall()
    return render_template('view_uploads.html', data=userData)


@app.route('/admin_portal/users/<userID>')
@login_required
def view_user_account(userID):
    if current_user.permLevel < 2:  # TODO: change number to config alias
        flash("Access to the admin portal area is restricted")
        return redirect(url_for('home'))

    user = db.session.execute("SELECT id, username, email, permLevel FROM User WHERE id = " + userID).fetchall()
    if user == []:
        flash("No user with ID: " + userID)
        return redirect(url_for('view_users'))

    return render_template('view_user_account.html', title="User Page...", userData=user)


@app.errorhandler(404)
def page_not_found(e):
    #  return render_template('404.html'), 404  # TODO: crete 404.html page
    return "<h1>404 - Page not found</h1><a href=\"/\">return home</a>"


@app.errorhandler(413)
def request_entity_too_large(error):
    return 'File Too Large', 413

@app.errorhandler(InternalServerError)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return render_template("500_unhandled.html"), 500

    # wrapped unhandled error
    return render_template("500_unhandled.html", e=original), 500





#####  ADDITIONAL FUNCTIONS  #####

def saveUpload(fileReceived, uploadForm, expirationDatetime):

    encrypted_data = encrypt(fileReceived.read(), key)

    # Create hasname. Hashnames are used to identify uploads
    hashname = secrets.token_hex(6)
    while Upload.query.filter_by(hashname=hashname).first() is not None:  # Make sure hashname is unique in database
        hashname = secrets.token_hex(6)

    # Find filesize of upload file
    fileReceived.seek(0, os.SEEK_END)
    filesize = fileReceived.tell()
    session['filesize'] = filesize

    # hash password (if required)
    hashedPassword = ""
    if uploadForm.password.data is not "":
        hashedPassword = bcrypt.generate_password_hash(uploadForm.password.data)

    # Add record to database
    uploadInstance = Upload(filename=fileReceived.filename,
                            filesize=filesize,
                            hashname=hashname,
                            datetime=datetime.date.today(),
                            expirationDatetime=expirationDatetime,
                            uploaderEmail=uploadForm.email.data,
                            message=uploadForm.message.data,
                            password=hashedPassword)
    db.session.add(uploadInstance)
    db.session.commit()

    filename = app.config['UPLOAD_FOLDER'] + hashname

    # Write encrypted file to directory
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    return hashname
