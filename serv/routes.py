from flask import render_template, url_for, flash, redirect, request
from serv import app, db
from serv.models import Upload
from serv.forms import ExampleForm
import secrets
import datetime


@app.route("/",  methods=['GET', 'POST'])
@app.route("/home",  methods=['GET', 'POST'])
@app.route("/index",  methods=['GET', 'POST'])
@app.route("/upload",  methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        f = request.files['file']

        hashname = secrets.token_hex(6)
        while Upload.query.filter_by(hashname=hashname).first() is not None:
            hashname = secrets.token_hex(6)
        uploadInstance = Upload(filename=f.filename, hashname=hashname, datetime=datetime.date.today(), uploaderEmail="uploader@mail.com")
        db.session.add(uploadInstance)
        db.session.commit()
        flash("Happy sharing! Here's the link: " "\"localhost:5000/v/" + hashname + "\"", 'success')

        f.save("uploads/" + hashname)
        return redirect(url_for('home'))
    return render_template('home.html', title="Home Page")






# @app.route("/form", methods=['GET', 'POST'])
# def form():
#     form = ExampleForm()
#     if form.validate_on_submit():
#         flash(f'Submitted Form - flash message for {form.name.data}', 'success')#
#         return redirect(url_for('home'))
#     return render_template('formPage.html', title="Example Form Page", form=form)
