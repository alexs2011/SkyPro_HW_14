from flask import abort, jsonify

import utility.utils as utils
from app import app


@app.route('/movie/<title>')
def movie_by_title(title: str):
    """
    Поиск фильма по названию. Если таких фильмов несколько, выводится самый свежий.
    """
    res = utils.find_movie_by_title(title)
    return jsonify(res)


@app.route('/movie/<int:year_from>/to/<int:year_to>')
def movies_by_years_range(year_from: int, year_to: int):
    """
    Поиск фильмов по диапазону лет. Выводятся первые 100 найденных.
    """
    res = utils.find_movies_by_years_range(year_from, year_to)
    return jsonify(res)


@app.route('/rating/<name>')
def rating_page(rating_name: str):
    """
    Поиск по группам рейтинга: для детей, для семейного просмотра, для взрослых.
    """
    allowed_rating_names = {'children', 'family', 'adult'}
    if rating_name not in allowed_rating_names:
        abort(404)
    res = utils.find_by_rating(rating_name)
    return jsonify(res)


@app.route('/genre/<genre>')
def movies_by_genre(genre: str):
    """
    Поиск по жанрам. Выводит 10 самых свежих фильмов.
    """
    res = utils.find_by_genre(genre)
    return jsonify(res)
