import threading, time, datetime, os
from serv import db
from serv.models import Upload
from flask import current_app

def runFileCleanup():
    print("Initiating file cleanup to remove expired uploads")
    x = threading.Thread(target=cleanup_thread_function)
    x.start()


def cleanup_thread_function():
    while True:
        # print("Clearing expired files ...")

        # for each available upload:
        availableUploads = Upload.query.filter(Upload.status == 1).all()

        # check if current date is less than or equal to expirationDatetime:
        for record in availableUploads:
            if datetime.datetime.today() >= record.expirationDatetime:
                try:
                    record.status = 0
                    db.session.commit()

                    fileToDelete = current_app.config['UPLOAD_FOLDER'] + record.hashname
                    os.remove(fileToDelete)
                    # TODO: log deletion
                except:
                    # TODO: log 'could not remove...'
                    pass
        # wait
        time.sleep(1800)  # 30minutes (3600 seconds = 1 hour)


