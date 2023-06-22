from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from pytube import YouTube
import re

app_bp = Blueprint("app_bp", __name__, template_folder="templates",
                   static_folder="static", static_url_path="/AppFolder/static")

resolution = {18:"360p/High Resolution", 22:"720p/High Resolution"}

def sanitize_filename(filename):
    # Remove any characters that are not alphanumeric, spaces, or common filename symbols
    return re.sub(r'[^\w\s.-]', '', filename)

@app_bp.route("/")
def index():
    return render_template("index.html")

@app_bp.route("/submit", methods=["GET","POST"])
def submit():
    try:
        if request.method == "POST":
            url = request.form["url"]
            ytube = YouTube(url)
            ytube = ytube.streams.filter(mime_type="video/mp4")
            #print(ytube)
            data = [(i.itag, resolution[i.itag]) for i in ytube if i.itag in resolution]
            print(data)
            for i in data:
                flash(i, "video")
            return render_template("index.html", data=url)
    except:
        flash("Something went wrong! Try again later!", "fail")
        return redirect(url_for("app_bp.index"))

@app_bp.route("/download", methods=["GET", "POST"])
def download():
    try:
        if request.method == "POST":
            url = request.form["url"]
            print(url)
            res = request.form["resolution"]
            print(res)
            video = YouTube(url)
            file = video.streams.get_by_itag(res)
            f_name = sanitize_filename(video.title)+'.mp4'
            print(f_name)
            file.download(filename=f_name)
            return send_file(f_name, as_attachment=True)
    except Exception as e:
        print(e)
        flash("Something went wrong", "fail")
        return redirect(url_for('app_bp.index'))
