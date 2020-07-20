from flask import render_template, url_for, flash, redirect
from serv import app
from serv.models import User, Upload
from serv.forms import ExampleForm


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template('home.html', title="Home Page")


@app.route("/form", methods=['GET', 'POST'])
def form():
    form = ExampleForm()
    if form.validate_on_submit():
        flash(f'Submitted Form - flash message for {form.name.data}', 'success')#
        return redirect(url_for('home'))
    return render_template('formPage.html', title="Example Form Page", form=form)
