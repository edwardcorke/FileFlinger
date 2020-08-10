from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
#  # TODO: from werkzeug.exceptions import RequestEntityTooLarge
from flask_login import current_user, login_required
from serv import db, Config
from serv import logger

admin = Blueprint('admin', __name__)


@admin.route('/admin_portal')
@login_required
def admin_portal():
    if current_user.permLevel < Config.permissionLevels['admin']:
        flash("Access to the admin portal area is restricted")
        return redirect(url_for('uploads.home'))

    data = db.session.execute("SELECT id, username, email, permLevel FROM User").fetchall()
    datab = db.session.execute("SELECT id, filename, hashname, filesize, datetime, expirationDatetime, uploaderEmail, message, status FROM Upload").fetchall()
    return render_template('admin_portal.html', data=data, datab=datab)


@admin.route('/admin_portal/users/<userID>')
@login_required
def view_user_account(userID):
    if current_user.permLevel < Config.permissionLevels['admin']:
        flash("Access to the admin portal area is restricted")
        return redirect(url_for('uploads.home'))

    # Updating availability status
    status = request.args.get('status')
    upload_id = request.args.get('upload_id')
    if status:
        db.session.execute("UPDATE Upload SET status = " + status + " WHERE id = " + upload_id)
        db.session.commit()
        logger.log.info('User with id {} changed the availability of upload with id {} to {}'.format(current_user.id, upload_id, status))

    # Updating permission level of an account
    permLevel = request.args.get('permLevel')
    if permLevel:
        permLevel = int(permLevel)
        if str(current_user.id) == userID:
            flash("You cannot change your own permission level")
        elif permLevel > int(current_user.permLevel):
            flash("Cannot raise a user's permission level higher that yourself")
        elif permLevel < 0:
            flash("Invalid permission level")
        else:
            db.session.execute("UPDATE User SET permLevel = " + str(permLevel) + " WHERE id = " + userID)
            db.session.commit()
            logger.log.info('User with id {} changed the permission level of user with id {} to {}'.format(current_user.id, userID, permLevel))


    # Selecting user details
    user = db.session.execute("SELECT id, username, email, permLevel FROM User WHERE id = " + userID).fetchone()

    if user is None:
        flash("No user with ID: " + userID)
        return redirect(url_for('admin.view_users'))

    # Searching for any uploads by the user
    uploads = db.session.execute("SELECT id, filename, hashname, filesize, datetime, expirationDatetime, message, status FROM Upload WHERE uploaderEmail = \"" + user[2] + "\"")
    return render_template('view_user_account.html', title="User Page...", userData=user, uploads=uploads)


@admin.route('/admin_portal/users')
@login_required
def view_users():
    if current_user.permLevel < Config.permissionLevels['admin']:
        flash("Access to the admin portal area is restricted")
        return redirect(url_for('uploads.home'))

    userData = db.session.execute("SELECT id, username, email, permLevel FROM User").fetchall()
    return render_template('view_users.html', data=userData)


@admin.route('/admin_portal/uploads')
@login_required
def view_uploads():
    if current_user.permLevel < Config.permissionLevels['admin']:
        flash("Access to the admin portal area is restricted")
        return redirect(url_for('uploads.home'))

    # Find data if email searched
    email = request.args.get("email")
    search = []
    if email:
        search = db.session.execute("SELECT id, filename, hashname, filesize, datetime, expirationDatetime, message, status FROM Upload WHERE uploaderEmail = \"" + email + "\"").fetchall()

    # Changing availability status
    status = request.args.get('status')
    upload_id = request.args.get('upload_id')
    if status:
        db.session.execute("UPDATE Upload SET status = " + status + " WHERE id = " + upload_id)
        db.session.commit()
        logger.log.info('User with id {} changed the availability of upload with id {} to {}'.format(current_user.id, upload_id, status))

    userData = db.session.execute("SELECT id, filename, hashname, filesize, datetime, expirationDatetime, uploaderEmail, message, status FROM Upload").fetchall()
    return render_template('view_uploads.html', data=userData, search=search)
