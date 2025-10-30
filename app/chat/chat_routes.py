from flask import Blueprint, render_template, request, redirect, url_for, flash , jsonify , current_app 
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, uuid
from datetime import datetime
from markdown import markdown 
import re
from app.Models import db
from app.Models.Chat import Chat
from app.document_utils.upload_documents import process_and_store_documents
from app.document_utils.qa_chat import get_rag_chain
from app.Models.ChatHistory import ChatHistory
from collections import deque
import whisper
import tempfile
from flask import stream_with_context
from flask import Response, stream_with_context
from flask import request, jsonify
import subprocess
import os
import time

import time




model = whisper.load_model("base")  # or load once globally
chat_bp = Blueprint("chat", __name__)













import os
import time
import tempfile
import subprocess
import traceback
from flask import request, jsonify, url_for, current_app
from flask_login import login_required

from gtts import gTTS







import os
import time
import tempfile
import subprocess
import traceback
from flask import jsonify, request, url_for, current_app
from flask_login import login_required
from gtts import gTTS








import traceback
import subprocess
import os
import tempfile
import time
from flask import current_app, jsonify, url_for, request
from flask_login import login_required






@chat_bp.route("/wav2lip", methods=["POST"])
@login_required
def wav2lip():
    text = request.form.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        from gtts import gTTS
        import tempfile
        import os
        import time
        import subprocess
        import traceback
        from flask import current_app, url_for

        # Generate audio from text
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            tts = gTTS(text)
            tts.save(temp_audio_file.name)
            audio_path = temp_audio_file.name

        # Paths - use temp directory without spaces for Wav2Lip processing
        default_video_path = os.path.join(current_app.static_folder, "videos", "default_talking_face.mp4")
        temp_output_path = os.path.join(tempfile.gettempdir(), f"wav2lip_{int(time.time())}.mp4")
        final_output_path = os.path.join(current_app.static_folder, "videos", f"wav2lip_{int(time.time())}.mp4")
        output_video_with_audio_path = final_output_path.replace(".mp4", "_with_audio.mp4")

        python_executable = r"C:\Users\waliq\OneDrive\Desktop\Chatbot Project\3.8\Wav2Lip\myenv\Scripts\python.exe"
        inference_script_path = r"C:\Users\waliq\OneDrive\Desktop\Chatbot Project\3.8\Wav2Lip\inference.py"
        checkpoint_path = r"C:\Users\waliq\OneDrive\Desktop\Chatbot Project\3.8\Wav2Lip\wav2lip.pth"
        wav2lip_dir = r"C:\Users\waliq\OneDrive\Desktop\Chatbot Project\3.8\Wav2Lip"

        print(f"Checking paths:")
        print(f"Python exe exists: {os.path.exists(python_executable)}")
        print(f"Inference script exists: {os.path.exists(inference_script_path)}")
        print(f"Checkpoint exists: {os.path.exists(checkpoint_path)}")
        print(f"Wav2Lip dir exists: {os.path.exists(wav2lip_dir)}")
        print(f"Default video exists: {os.path.exists(default_video_path)}")
        print(f"Audio path: {audio_path}")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(final_output_path), exist_ok=True)
        
        # Run Wav2Lip with temp path (no spaces)
        command = [
            python_executable,
            inference_script_path,
            "--checkpoint_path", checkpoint_path,
            "--face", default_video_path,
            "--audio", audio_path,
            "--outfile", temp_output_path,
        ]

        print(f"Running command: {' '.join(command)}")
        print(f"Working directory: {wav2lip_dir}")
        
        try:
            print("Starting subprocess...")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout for full processing
                cwd=wav2lip_dir
            )
            
            print(f"Subprocess completed!")
            print(f"Return code: {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("Subprocess timed out after 1 minute")
            return jsonify({"error": "Wav2Lip processing timed out - process may be hanging"}), 500
        except Exception as subprocess_error:
            print(f"Subprocess error: {subprocess_error}")
            return jsonify({"error": f"Subprocess failed: {str(subprocess_error)}"}), 500

        if result.returncode != 0:
            return jsonify({
                "error": "Wav2Lip processing failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }), 500

        # Copy from temp location to final location
        import shutil
        shutil.copy2(temp_output_path, final_output_path)
        
        # Mux audio and video with ffmpeg
        ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-i", final_output_path,
            "-i", audio_path,
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_video_with_audio_path
        ]

        ffmpeg_result = subprocess.run(
            ffmpeg_command,
            capture_output=True,
            text=True,
            timeout=60
        )

        if ffmpeg_result.returncode != 0:
            return jsonify({
                "error": "FFmpeg muxing failed",
                "returncode": ffmpeg_result.returncode,
                "stdout": ffmpeg_result.stdout,
                "stderr": ffmpeg_result.stderr
            }), 500

        # Cleanup
        os.remove(audio_path)
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)
        if os.path.exists(final_output_path):
            os.remove(final_output_path)

        # Return video URL for frontend
        video_filename = os.path.basename(output_video_with_audio_path)
        video_url = url_for('static', filename=f"videos/{video_filename}", _external=True)

        return jsonify({"video_url": video_url})

    except Exception as e:
        error_msg = traceback.format_exc()
        print("Exception in /wav2lip route:\n", error_msg)
        return jsonify({"error": str(e), "traceback": error_msg}), 500







@chat_bp.route("/show_video/<filename>")
@login_required
def show_video(filename):
    # Simple security check
    if not filename.startswith("wav2lip_") or not filename.endswith("_with_audio.mp4"):
        return "Invalid video filename", 400

    video_url = url_for('static', filename=f"videos/{filename}")
    return render_template("show_video.html", video_url=video_url, filename=filename)





















@chat_bp.route("/transcribe", methods=["POST"])
@login_required
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio_file = request.files["audio"]

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        audio_path = tmp.name
        audio_file.save(audio_path)

    try:
        result = model.transcribe(audio_path, fp16=False, language="en")
        text = result.get("text", "").strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(audio_path)

    return jsonify({"text": text})






# -------------------- custom_prompt ------------------

@chat_bp.route('/chat/<int:chat_id>/custom_prompt', methods=['GET', 'POST'])
@login_required
def custom_prompt(chat_id):
    chat = Chat.query.get_or_404(chat_id)

    # Ensure the logged-in user owns the chat
    if chat.user_id != current_user.id:
        flash("You are not authorized to edit this chat.", "danger")
        return redirect(url_for('chat.dashboard'))

    if request.method == 'POST':
        prompt = request.form.get("custom_prompt")
        chat.custom_prompt = prompt
        db.session.commit()
        flash("Custom prompt saved successfully!", "success")
        return redirect(url_for('chat.dashboard'))

    return render_template('custom_prompt.html', chat=chat)







# -------------------- start_chat ------------------


@chat_bp.route("/start_chat/<int:chat_id>", methods=["GET"])
@login_required
def start_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return "Unauthorized", 403

    chat_history = ChatHistory.query.filter_by(chat_id=chat.id, user_id=current_user.id).order_by(ChatHistory.timestamp).all()

    return render_template("start_chat.html", chat=chat, chat_history=chat_history)






# # -------------------- stream_chat ------------------








import markdown  # add this at the top

def clean_stream_chunk(text):
    """Pass streamed chunks as-is for frontend Live Markdown rendering."""
    return text  # no change here

def clean_response(text):
    """Convert final Markdown response to HTML before saving in DB."""
    html = markdown.markdown(text)
    return html

@chat_bp.route("/start_chat/<int:chat_id>/stream", methods=["POST"])
@login_required
def stream_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if chat.user_id != current_user.id:
        return "Unauthorized", 403

    data = request.get_json()
    question = data.get("question", "")

    def generate():
        try:
            chroma_path = chat.chromadb_collection
            bm25_path = os.path.join(chroma_path, "bm25_chunks.pkl")

            previous_entries = ChatHistory.query.filter_by(
                chat_id=chat.id,
                user_id=current_user.id
            ).order_by(ChatHistory.timestamp.desc()).limit(5).all()

            memory_buffer = deque(reversed(previous_entries))

            rag_chain = get_rag_chain(
                chroma_path=chroma_path,
                bm25_path=bm25_path,
                custom_prompt=chat.custom_prompt,
                memory_buffer=memory_buffer
            )

            full_response = ""

            for chunk in rag_chain.stream(question):
                full_response += chunk
                yield clean_stream_chunk(chunk)

            cleaned_response = clean_response(full_response)
            chat_entry = ChatHistory(
                user_id=current_user.id,
                chat_id=chat.id,
                question=question,
                answer=cleaned_response
            )
            db.session.add(chat_entry)
            db.session.commit()

        except Exception as e:
            yield f"\n❌ Error: {str(e)}"

    return Response(stream_with_context(generate()), content_type="text/plain")




























# -------------------- dashboard ------------------



@chat_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")



# -------------------- new_chat ------------------

@chat_bp.route("/new_chat", methods=["GET", "POST"])
@login_required
def new_chat():
    if request.method == "POST":
        file = request.files["pdf"]
        chat_name = request.form.get("chat_name")

        if not file or not chat_name:
            return "Missing file or chat name", 400

        # Save uploaded PDF to DOCUMENTS folder
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        documents_folder = os.path.join("app", "DOCUMENTS")
        os.makedirs(documents_folder, exist_ok=True)
        file_path = os.path.join(documents_folder, filename)
        file.save(file_path)

        # Create unique vector DB folder
        unique_id = uuid.uuid4()
        vector_folder = f"user_{current_user.id}_chat_{unique_id}"
        vector_store_path = os.path.join("app", "Vector Storage", vector_folder)
        os.makedirs(vector_store_path, exist_ok=True)

        # Process PDF into ChromaDB
        try:
            num_chunks = process_and_store_documents(file_path, vector_store_path)
            print(f"✅ Stored {num_chunks} chunks in {vector_store_path}")
        except Exception as e:
            print(f"❌ Error in embedding process: {e}")
            return "Error processing document", 500

        # Save chat metadata with empty prompt
        new_chat = Chat(
            user_id=current_user.id,
            chat_name=chat_name,
            pdf_path=file_path,
            custom_prompt="",  # Stored as empty
            chromadb_collection=vector_store_path
        )
        db.session.add(new_chat)
        db.session.commit()

        return redirect(url_for("chat.dashboard"))

    return render_template("new_chat.html")




# -------------------- view_chats ------------------



@chat_bp.route("/view_chats")
@login_required
def view_chats():
    user_chats = Chat.query.filter_by(user_id=current_user.id, visible=True).order_by(Chat.created_at.desc()).all()
    return render_template("view_chats.html", chats=user_chats)