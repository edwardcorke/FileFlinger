import threading, time, datetime, os
from serv import db, app
from serv.models import Upload
from sqlalchemy import and_

def runFileCleanup():
    x = threading.Thread(target=cleanup_thread_function)
    x.start()


def cleanup_thread_function():
    while True:
        print("Clearing expired files ...")

        # take current time
        age = datetime.timedelta(30) # TODO: app.config
        cutoffDatetime = datetime.date.today() - age

        # find any expired records that are still available
        expiredUploads = Upload.query.filter(and_(Upload.datetime <= cutoffDatetime, Upload.status == 1)).all()

        # flag records unavailable and delete file with hashname
        for record in expiredUploads:
            try:
                record.status = 0
                db.session.commit()

                fileToDelete = app.config['UPLOAD_FOLDER'] + record.hashname
                os.remove(fileToDelete)
                # TODO: log deletion
            except:
                # TODO: log 'could not remove...'
                pass

        # wait
        time.sleep(1800)  # 30minutes (3600 seconds = 1 hour)
