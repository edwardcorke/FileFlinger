from serv import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    submissions = db.relationship('Upload', backref='uploader', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.name}', '{self.email}')"

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(60), unique=True, nullable=False)
    submitter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Upload('{self.id}', '{self.filename}', '{self.submitter}')"