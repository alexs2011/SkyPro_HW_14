from collections import Counter

from dao.netflix_dao import NetflixDAO

netflix_dao = NetflixDAO("netflix.db")


def find_movie_by_title(title: str) -> dict:
    """
    Поиск фильма по названию. Если таких фильмов несколько, выводится самый свежий.
    """
    res = {
        "is_found": True,
        "title": title,
        "country": None,
        "release_year": None,
        "genre": None,
        "description": None,
    }

    sqlite_query = f"SELECT country, release_year, listed_in, description " \
                   f"FROM 'netflix' " \
                   f"WHERE type='Movie' " \
                   f"AND title='{title}' " \
                   f"ORDER BY date_added DESC " \
                   f"LIMIT 1"
    executed_query = netflix_dao.execute_query(sqlite_query)

    #  Если фильм не найден.
    if len(executed_query) == 0:
        res["is_found"] = False
        return res

    movie = executed_query[0]
    res["country"] = movie[0]
    res["release_year"] = movie[1]
    res["genre"] = movie[2]
    res["description"] = movie[3].strip()

    return res


def find_movies_by_years_range(year_from: int, year_to: int) -> list[dict]:
    """
    Поиск фильмов по диапазону лет. Вывод ограничен 100 фильмами.
    """
    sqlite_query = f"SELECT title, release_year " \
                   f"FROM 'netflix' " \
                   f"WHERE type='Movie' " \
                   f"AND release_year between {year_from} and {year_to} " \
                   f"ORDER BY release_year " \
                   f"LIMIT 100"
    executed_query = netflix_dao.execute_query(sqlite_query)

    res = []
    for row in executed_query:
        d = {
            "title": row[0],
            "release_year": row[1],
        }
        res.append(d)

    return res


def find_by_rating(rating_name: str) -> list[dict]:
    """
    Поиск по группам рейтинга: для детей, для семейного просмотра, для взрослых.
    """
    rating = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'",
    }

    cur_rating = rating[rating_name]

    sqlite_query = f"SELECT title, rating, description " \
                   f"FROM 'netflix' " \
                   f"WHERE rating in ({cur_rating}) " \
                   f"ORDER BY release_year"
    executed_query = netflix_dao.execute_query(sqlite_query)

    res = []
    for row in executed_query:
        d = {
            "title": row[0],
            "rating": row[1],
            "description": row[2].strip()
        }
        res.append(d)

    return res


def find_by_genre(genre: str) -> list[dict]:
    """
    Поиск по жанрам. Выводит 10 самых свежих фильмов.
    """
    sqlite_query = f"SELECT title, description " \
                   f"FROM 'netflix' " \
                   f"WHERE type='Movie' " \
                   f"AND listed_in LIKE '%{genre}%' " \
                   f"ORDER BY date_added DESC " \
                   f"LIMIT 10"
    executed_query = netflix_dao.execute_query(sqlite_query)

    res = []
    for row in executed_query:
        d = {
            "title": row[0],
            "description": row[1].strip()
        }
        res.append(d)

    return res


def get_actors_played_with_given_actors(first_actor: str, second_actor: str) -> list:
    """
    Получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast (если участвовали оба
    переданных актёра) и возвращает список тех, кто играет с ними в паре больше 2 раз.
    """
    sqlite_query = f"SELECT `cast` " \
                   f"FROM 'netflix' " \
                   f"WHERE `cast` LIKE '%{first_actor}%' " \
                   f"AND `cast` LIKE '%{second_actor}%' "
    executed_query = netflix_dao.execute_query(sqlite_query)

    #  Создаём общий список всех актёров (с повторениями), игравших с заданными, убирая при этом заданных актёров.
    actors_lst = []
    for row in executed_query:
        actors_row = row[0].split(", ")
        actors_lst.extend([actor for actor in actors_row if actor not in {first_actor, second_actor}])

    #  Подсчитываем, сколько раз встречаются актёры (т.е. в скольки фильмах они играли).
    actors_counter = Counter(actors_lst)

    res = [actor for actor, count in actors_counter.items() if count >= 2]
    return res
