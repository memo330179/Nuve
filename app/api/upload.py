from werkzeug.utils import secure_filename
from config import upload_folder
allowed_extensions = ['mp4', 'mkv'] #todo: need the full list of extensions

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_movie(media_file):
    if media_file and allowed_file(media_file.filename):
        filename = secure_filename(media_file.filename)
        saved_file_path = os.path.join(UPLOAD_FOLDER, "movies", filename)
        media_file.save(saved_file_path)
        return saved_file_path

def upload_episode(media_file, info):
    if media_file and allowed_file(media_file.filename):
        filename = secure_filename(media_file.filename)
        saved_file_path = os.path.join(UPLOAD_FOLDER,
                                        "shows",
                                        info.title,
                                        info.season,
                                        filename)
        media_file.save(saved_file_path)
        return saved_file_path
