from serv import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    filesize = db.Column(db.Integer, nullable=False)
    hashname = db.Column(db.String(16), unique=True, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    expirationDatetime = db.Column(db.DateTime, nullable=False)
    uploaderEmail = db.Column(db.String(320), nullable=False)
    message = db.Column(db.String(512), nullable=False, default="")
    status = db.Column(db.Integer, default=1, nullable=False)  # 1: available, 0: unavailable
    password = db.Column(db.String(256))

    def __repr__(self):
        return f"Upload('{self.id}', '{self.filename}', '{self.hashname}', '{self.datetime}', '{self.expirationDatetime}', '{self.uploaderEmail}', {self.status})"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False)  # TODO: unique?
    email = db.Column(db.String(256), nullable=False)  # TODO: verify?
    password = db.Column(db.String(256), nullable=False)
    # salt = db.Column(db.String(64), nullable=False)  # TODO: add salt?
    permLevel = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.permLevel}')"
