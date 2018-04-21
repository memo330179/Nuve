from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
import os
import errno

ALLOWED_EXTENSIONS = ['mp4', 'mkv'] #todo: need the full list of extensions

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            
            
def create_directory(filename):
    # import pdb; pdb.set_trace();
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def upload_movie(media_file):
    if media_file and allowed_file(media_file.filename):
        filename = secure_filename(media_file.filename)
        saved_file_path = os.path.join(UPLOAD_FOLDER, "movies", filename)
        create_directory(saved_file_path)
        media_file.save(saved_file_path)
        return saved_file_path

def upload_episode(media_file, info):
    if media_file and allowed_file(media_file.filename):
        filename = secure_filename(media_file.filename)

        
        saved_file_path = os.path.join(UPLOAD_FOLDER,
                                        "shows",
                                        info['title'],
                                        str(info['season']),
                                        filename)
        create_directory(saved_file_path)
        media_file.save(saved_file_path)
        return saved_file_path
