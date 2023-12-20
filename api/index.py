import flask
from flask import Flask, render_template, redirect, request, url_for
from bson import ObjectId
import pymongo
from pymongo import MongoClient

app = Flask(__name__, template_folder="templates")

client = MongoClient("mongodb+srv://asad:asad@blogdb.acnss0h.mongodb.net/?retryWrites=true&w=majority")

db = client['animeWebsite']
collection = db['anime']

@app.route("/")
def home():
    anime_list = collection.find()
    return render_template("home.html", anime=anime_list)

@app.route('/create', methods=['GET', 'POST'])
def create_anime():
    if request.method == 'POST':
        anime_name = request.form['anime_name']
        anime_image = request.form['anime_image']
        
        anime_data = {
            "name": anime_name,
            "url": anime_image,
            "episodes": []
            
        }
        collection.insert_one(anime_data)
        return f'Anime created with name: {anime_name}'
    return render_template('create.html')


# @app.route("/anime_upload/<anime_id>", methods=['GET', 'POST'])
# def upload_episode(anime_id):
#     anime = collection.find_one({"_id": ObjectId(anime_id)})
#     if request.method == 'POST':
#         episode_link = request.form['episode_link']
#         # Append the new episode link to the anime's 'episodes' list
#         collection.update_one(
#             {"_id": ObjectId(anime_id)},
#             {"$push": {"episodes": episode_link}}
#         )
#         return f'Episode link added to Anime: {anime["name"]}'
#     return render_template("upload_episode.html", anime=anime)

@app.route("/view/<anime_id>")
def view_anime(anime_id):
    anime = collection.find_one({"_id": ObjectId(anime_id)})
    return render_template("view.html", anime=anime)


@app.route("/watch/<anime_id>/<int:episode_number>")
def watch_episode(anime_id, episode_number):
    anime = collection.find_one({"_id": ObjectId(anime_id)})
    if anime and episode_number > 0 and episode_number <= len(anime.get("episodes", [])):
        episode_link = anime["episodes"][episode_number - 1]
        return render_template("watch.html", episode_link=episode_link)
    else:
        return "Episode not found"

@app.route("/add_episode", methods=['GET', 'POST'])
def add_episode():
    anime_titles = [anime["name"] for anime in collection.find()]
    if request.method == 'POST':
        selected_anime = request.form['selected_anime']
        episode_link = request.form['episode_link']
        
        anime = collection.find_one({"name": selected_anime})
        if anime:
            
            collection.update_one(
                {"_id": anime["_id"]},
                {"$push": {"episodes": episode_link}}
            )
            return f'Episode added to Anime: {selected_anime}'
    return render_template("upload_episode.html", anime_titles=anime_titles)


