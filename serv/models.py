from serv import db

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    hashname = db.Column(db.String(16), unique=True, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    uploaderEmail = db.Column(db.String(320), nullable=False)
    status = db.Column(db.Integer, default=1, nullable=False)  # 1: available, 0: unavailable

    def __repr__(self):
        return f"Upload('{self.id}', '{self.filename}', '{self.hashname}'), '{self.datetime}'), '{self.uploaderEmail}')"