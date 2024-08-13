from myapp import app, db
from myapp.model import User, Video, Transcript, Subtitle, fs
from myapp.chat import generate_response

from flask import request, send_file, jsonify, make_response
from  myapp.video_processor import extract_audio, transcribe_using_assemblyai, add_subtitle_to_video
from myapp.dub_utility import generate_dub
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from myapp.chat import *


# Configurations
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'WEBM'}  # Add allowed extensions as needed
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the video folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


dub_lang = {
    "en": {
        "male": "en-US-Journey-D",
        "female": "en-US-Journey-F"
    },
     "en_uk": {
        "male": "en-US-Journey-D",
        "female": "en-US-Journey-F"
    },
      "en_us": {
        "male": "en-US-Journey-D",
        "female": "en-US-Journey-F"
    },
       "en_au": {
        "male": "en-US-Journey-D",
        "female": "en-US-Journey-F"
    },
       "fr": {
           "male": "fr-FR-Neural2-B",
           "female": "fr-FR-Neural2-C"
       },
       
       "de": {
           "male": "de-DE-Neural2-B",
           "female": "de-DE-Neural2-A"
       },
       "es": {
           "male": "es-ES-Neural2-B",
           "female": "es-ES-Neural2-A" 
       }
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload a video and generate subtitles
@app.route('/subtitle/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file  and allowed_file(file.filename):
        # Extract other form data
        size = request.form.get('size')
        dimensions = request.form.get('dimensions')
        duration = request.form.get('duration')
        original_language = request.form.get('original_language')
        target_language = request.form.get('target_language')
        format_ = file.mimetype
        isSub = request.form.get('sub')
        isDub = request.form.get('dub')
        gender = request.form.get('gender')
        
        print(gender)
        
    

        # Extract audio from the video in memory
        try:
            filename = secure_filename(file.filename)
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(video_path)
            audio_name, audio_path = extract_audio(video_path, filename)
            srt_path, transcript_path = None, None
            if original_language == "auto":
                srt_path, transcript_path = transcribe_using_assemblyai(audio_path, audio_name, target_language=target_language)
            else:
                srt_path, transcript_path = transcribe_using_assemblyai(audio_path, audio_name, lang=original_language, target_language=target_language)
            
            # Add subtitle to the video
            print("Adding subtitle to video", srt_path)
            
            output_video_path = None
            if isSub == "true":
                print("Adding Subtitle...")
                output_video_path = add_subtitle_to_video(False, srt_path,  target_language, video_path, filename)
            
            
            if not output_video_path:
                output_video_path = video_path
                
            if isDub == "true":
                print("Generating Dub...")
                # Todo: Source Language Should be made dynamic
                output_video_path = generate_dub(output_video_path, dub_lang[target_language][gender], "webtech2-ac636-2ce883895de0.json", "english")

            # Save the video to the database
            with open(output_video_path, 'rb') as video_file:
                video_data = video_file.read()
                video = Video(user_id="123", filename=filename, size=size, dimensions=dimensions, duration=duration, format_=format_, original_language=original_language, target_language=target_language, content=video_data)
                video_id = video.save_to_db()

                # Save Subtitles to the database
                with open(srt_path, 'rb') as srt_file:
                    srt_data = srt_file.read()
                    subtitle = Subtitle(video_id, srt_data, target_language, filename)
                    subtitle.save_to_db()

                # Save Transcript to the database
                with open(transcript_path, 'rb') as transcript_file:
                    transcript_data = transcript_file.read()
                    transcript = Transcript(video_id, transcript_data, target_language, filename)
                    transcript.save_to_db()

        except Exception as e:
            return jsonify({"message": f"Failed to process video: {str(e)}"}), 500 
        

        return jsonify({"message": "File uploaded successfully!"}), 200
    return jsonify({"message": "Invalid file format"}), 400
    
# Route to get all videos
@app.route('/videos', methods=['GET'])
def dashboard():
    videos = db.videos.find()
    video_list = []
    for video in videos:
        del video['_id']
        del video['content_id']
        del video['user_id']
        video_list.append(video)
    return jsonify({"videos": video_list}), 200

# Endpoint to delete a video
@app.route('/video/delete/<video_name>', methods=['DELETE'])
def delete_video(video_name):
    video = db.videos.find({'filename': video_name})
    video_id = video.get('content_id')
    try:
        result = db.videos.delete({'_id': video_id})
        db.videos.files.delete({'_id': video_id})
        db.videos.chunks.delete({'files_id': video_id})
        db.transcripts.delete({'video_id': video_id})
        db.subtitles.delete({'video_id': video_id})
        if result.deleted_count >= 1:
            return jsonify({'status': 'success', 'message': 'Entry deleted successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Entry not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({"videos": video_list}), 200

# Endpoint to get a video
@app.route('/download/<video_name>', methods=['GET'])
def download_video(video_name):
    data = db.videos.files.find_one({"filename": video_name})
    if not data:
        return jsonify({"message": "Video not found"}), 404
    

    mime_type = db.videos.find_one({"filename": video_name}).get('format')
    format = mime_type.split('/')[1]
    
    
    fs_id = data['_id']
    try:
        # Extract video data (assuming a field named 'video_data')
        video_bytes = fs.get(fs_id).read()

        # Set response headers
        response = make_response(video_bytes)
        response.headers["Content-Type"] = mime_type  # Adjust based on video type
        response.headers["Content-Disposition"] = f"attachment; filename={video_name}.{format}"
        return response
        
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return jsonify({"message": f"Failed to download file: {str(e)}"}), 500

# Endpoint to download a video transcript
@app.route('/download/transcript/<video_name>', methods=['GET'])
def download_transcript(video_name):
    data = db.videos.files.find_one({"filename": "transcript_" + video_name})
    if not data:
        return jsonify({"message": "Transcript not found"}), 404
    
    fs_id = data['_id']
    try:
        # Extract Text data 
        text_data = fs.get(fs_id).read()       
        return jsonify({"transcript": text_data.decode('utf-8')}), 200
        
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return jsonify({"message": f"Failed to download file: {str(e)}"}), 500
    
# Endpoint to download a video subtitle
@app.route('/download/subtitle/<video_name>', methods=['GET'])
def download_subtitle(video_name):
    data = db.videos.files.find_one({"filename": "subtitle_" + video_name})
    if not data:
        return jsonify({"message": "subtitle not found"}), 404
    
    fs_id = data['_id']
    try:
        # Extract Text data 
        text_data = fs.get(fs_id).read()       
        return jsonify({"subtitle": text_data.decode('utf-8')}), 200
        
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return jsonify({"message": f"Failed to download file: {str(e)}"}), 500
    
# Endpoint to ask questions about the video content
@app.route('/ask/<video_name>', methods=['POST'])
def ask_question(video_name):
    data = request.json
    question = data.get('question')
    
    data = db.videos.files.find_one({"filename": "subtitle_" + video_name})
    if not data:
        return jsonify({"message": "Transcript not found"}), 404
    
    fs_id = data['_id']
    try:
        # Extract Text data 
        text_data = fs.get(fs_id).read()       
        extracted_text = text_data.decode('utf-8')
        return generate_response(extracted_text, question), {"Content-Type": "text/plain"}
        
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        return jsonify({"message": f"Failed to download file: {str(e)}"}), 500

@app.route('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.route('/user/login', methods=['POST'])
def login():
  return User().login()