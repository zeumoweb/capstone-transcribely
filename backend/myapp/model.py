from myapp import bcrypt, db
from flask import jsonify, request, session
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId
from gridfs import GridFS
import uuid


fs = GridFS(db, collection="videos")

# User model
class User:
    def save_to_db(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
        db.users.insert_one(user_data)
                
    def signup(self):
        # Create the user object
        user = {
        "_id": uuid.uuid4().hex,
        "username": request.form.get('name'),
        "email": request.form.get('email'),
        "password": request.form.get('password')
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email address already in use" }), 400

        if db.users.insert_one(user):
            del user['password']
            session['logged_in'] = True
            session['user'] = user
            return jsonify(user), 200

        return jsonify({ "error": "Signup failed" }), 400
    
    def signout(self):
        session.clear()
        return 200, jsonify({ "message": "Successfully signed out" })
    
    def login(self):

        user = db.users.find_one({
        "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials" }), 401


    @staticmethod
    def find_by_email(db, email):
        return db.users.find_one({"email": email})
    

    @staticmethod
    def find_by_id(user_id):
        return db.users.find_one({"_id": ObjectId(user_id)})
    

    @staticmethod
    def is_registered_user(db, email):
        return db.users.find_one({"email": email})
    


# Video model
class Video:
    def __init__(self, user_id, filename, size, dimensions, duration, format_, 
                 original_language, target_language, content):
        self.user_id = user_id
        self.size = size
        self.dimensions = dimensions
        self.duration = duration
        self.format = format_
        self.original_language = original_language
        self.target_language = target_language
        self.content = content
        self.filename = filename.split(".")[0]


    def save_to_db(self):
        video_id = fs.put(self.content, filename=f"{self.filename}", encoding='utf-8')
        video_data = {
            'user_id': self.user_id,
            'size': self.size,
            'dimensions': self.dimensions,
            'duration': self.duration,
            'format': self.format,
            'original_language': self.original_language,
            'target_language': self.target_language,
            'content_id': video_id,
            "filename": self.filename
        }
        db.videos.insert_one(video_data)
        return video_id


    @staticmethod
    def find_by_id(video_id):
        return db.videos.find_one({"_id": ObjectId(video_id)})



# Transcript model
class Transcript:
    def __init__(self, video_id, content, language, filename):
        self.video_id = video_id
        self.content = content
        self.language = language
        self.filename = filename.split(".")[0]


    def save_to_db(self):
        transcript_id = fs.put(self.content, filename=f"transcript_{self.filename}", encoding='utf-8')
        transcript_data = {
            'video_id': self.video_id,
            'language': self.language,
            'transcript_id': transcript_id
        }
        db.transcripts.insert_one(transcript_data)
        return transcript_id


    @staticmethod
    def find_by_id(transcript_id):
        return db.transcripts.find_one({"_id": ObjectId(transcript_id)})
    
    @staticmethod
    def find_by_video_id(video_id):
        return db.transcripts.find({"video_id": ObjectId(video_id)})
    


# Subtitle model
class Subtitle:
    def __init__(self, video_id, content, language, filename):
        self.video_id = video_id
        self.content = content
        self.language = language
        self.filename = filename.split(".")[0]


    def save_to_db(self):
        subtitle_id = fs.put(self.content, filename=f"subtitle_{self.filename}", encoding='utf-8')
        subtitle_data = {
            'video_id': self.video_id,
            'language': self.language,
            'subtitle_id': subtitle_id
        }
        db.subtitles.insert_one(subtitle_data)
        return subtitle_id


    @staticmethod
    def find_by_id(subtitle_id):
        return db.subtitles.find_one({"_id": ObjectId(subtitle_id)})
    
    @staticmethod
    def find_by_video_id(video_id):
        return db.subtitles.find({"video_id": ObjectId(video_id)})

