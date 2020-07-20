from flask import render_template, url_for, flash, redirect, request
from serv import app
from serv.models import User, Upload
from serv.forms import ExampleForm


@app.route("/",  methods=['GET', 'POST'])
@app.route("/home",  methods=['GET', 'POST'])
@app.route("/index",  methods=['GET', 'POST'])
@app.route("/upload",  methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        f = request.files['file']
        filename = "uploads/" + f.filename
        f.save(filename)
        return redirect(url_for('home'))
    return render_template('home.html', title="Home Page")


@app.route("/form", methods=['GET', 'POST'])
def form():
    form = ExampleForm()
    if form.validate_on_submit():
        flash(f'Submitted Form - flash message for {form.name.data}', 'success')#
        return redirect(url_for('home'))
    return render_template('formPage.html', title="Example Form Page", form=form)
