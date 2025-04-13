from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ml_logic2 import get_song_recommendations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/recommend', methods=['POST'])
def recommend():
    song_name = request.form['song']  # Get the song name input from the form

    # Here, you would fetch song-related data based on the song_name.
    # For example, if you have an API call or some logic to retrieve song data,
    # you would call that here.
    
    # For this example, let's just assume we pass the song name to the template.
    # You would replace this with actual logic to get song info.
    
    recommended_songs = get_song_recommendations(song_name)

    return render_template('song_list.html', song_name=song_name, recommended_songs=recommended_songs)

@app.route('/')
def index():
    return render_template('index.html')

if __name__== "__main__":
    app.run(debug=True)