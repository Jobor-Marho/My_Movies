import sqlalchemy.exc
from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests
from dotenv.main import load_dotenv
import os


load_dotenv()
MY_MOVIEDB_API_KEY = os.environ["MOVIEDB_API_KEY"]
MOVIEDB_LINK = "https://api.themoviedb.org/3"
PARAMS = {
    "api_key": MY_MOVIEDB_API_KEY,
    "query": None
}
HEADERS = {
    'Authorization': os.environ['AUTHORIZATION'],
    'Content-Type': 'application/json;charset=utf-8'
}


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my-favourite-movies.db"
Bootstrap(app)

db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(240), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False)
    ranking = db.Column(db.Integer, unique=False) # rectify it later
    review = db.Column(db.String(120), unique=False)
    img_url = db.Column(db.String(240), unique=False, nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.title


class RateMovieForm(FlaskForm):
    rating_form = FloatField(label='Your Rating out of 10 e.g 7.5', validators=[DataRequired()])
    review_form = StringField(label='Your Review', validators=[DataRequired()])
    submit_btn = SubmitField(label='Done')


class NewMovieForm(FlaskForm):
    title_form = StringField(label="Movie Title", validators=[DataRequired()])
    add_btn = SubmitField(label="Add Movie")


with app.app_context():
    db.create_all()


def get_movies():
    global count
    with app.app_context():
        all_movies = db.session.query(Movie).order_by(Movie.rating).all()
        # rating_list = [film.rating for film in data]
        # rating_list.sort()

        # if len(rating_list) == 0:
        #     length = len(all_movies)
        #     return all_movies, length
        # else:
        #     for rating in rating_list:
        #         for movie in data:
        #             if rating == movie.rating:
        #                 with app.app_context():
        #                     current_movie_data = db.session.query(Movie).filter_by(id=movie.id).first()
        #                     current_movie_data.ranking = len(rating_list) - rating_list.index(rating)
        #                     db.session.commit()
        #                 all_movies.append(movie)
        length = len(all_movies)
    return all_movies, length


def find_movies(query):
    global PARAMS, MOVIEDB_LINK, HEADERS
    PARAMS["query"] = query
    try:
        response = requests.get(url=f'{MOVIEDB_LINK}/search/movie', headers=HEADERS, params=PARAMS)
        data = response.json()
    except requests.exceptions.ConnectionError:
        movies = []
        return movies
    else:
        movies = []

        try:
            results = data['results']
        except KeyError:
            return render_template('error.html')
        else:
            for result in results:
                movie = {
                    'title': result["original_title"],
                    'date': result['release_date'],
                    'id': result['id']
                }
                movies.append(movie)
            return movies


def get_details(query):
    global MOVIEDB_LINK, HEADERS, MY_MOVIEDB_API_KEY
    params = {
        "api_key": MY_MOVIEDB_API_KEY
    }
    try:
        response = requests.get(url=f'{MOVIEDB_LINK}/movie/{query}', headers=HEADERS, params=params)
    except requests.exceptions.ConnectionError:
        return render_template("error.html")
    else:
        data = response.json()
        print(data)
        title = data['original_title']
        year = data['release_date'].split('-')[0]
        description = data['overview']

        response = requests.get(url=f"{MOVIEDB_LINK}/configuration", params=params)
        img = response.json()
        img_url = f"{img['images']['base_url']}/{img['images']['poster_sizes'][4]}/{data['poster_path']}"
        with app.app_context():
            new_movie = Movie(title=title, year=year, description=description, img_url=img_url)
            db.session.add(new_movie) # adding new data tpo the database
            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                title = ""
                return title
            else:
                return title


@app.route("/")
def home():
    movies = get_movies()
    all_movies = movies[0]
    length = movies[1]
    # This line loops through all the movies
    for i in range(len(all_movies)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies, length=length)


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit(id):
    rating_form = RateMovieForm()
    movie = db.session.query(Movie).filter_by(id=id).first()
    title = movie.title
    if rating_form.validate_on_submit():
        movie.rating = rating_form.rating_form.data
        movie.review = rating_form.review_form.data
        db.session.commit()
        return redirect("/")

    return render_template("edit.html", form=rating_form, title=title)


@app.route("/delete/<int:id>")
def delete(id):
    movie = db.session.query(Movie).filter_by(id=id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect('/')


@app.route("/add", methods=['POST', 'GET'])
def add():
    movie_form = NewMovieForm()
    if movie_form.validate_on_submit():
        title = movie_form.title_form.data
        movie_list = find_movies(title)
        length = len(movie_list)
        return render_template('select.html', movies=movie_list, length=length)

    return render_template('add.html', form=movie_form)


@app.route("/id/<int:id>")
def details(id):
    movie_title = get_details(id)
    if movie_title == "":
        return render_template("error.html")
    else:
        movie = db.session.query(Movie).filter_by(title=movie_title).first()
        try:
            movie_id = movie.id
        except AttributeError:
            return render_template("error.html")
        return redirect(f'/edit/{movie_id}')


if __name__ == '__main__':
    app.run(debug=True)
