from database.DB_connect import DBConnect
from model.movie import Movie


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from imdb_0408.movies m 
                    where m.`rank` is not null"""

        cursor.execute(query, ())

        for row in cursor:
            result.append(Movie(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(rank):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=False)
        query = """select r1.movie_id m1 ,r2.movie_id m2, count(distinct r1.actor_id) 
                from (select r.*
                from imdb_0408.movies m ,imdb_0408.roles r 
                where m.id =r.movie_id 
                and m.`rank` is not null
                and m.`rank`>=%s
                ) r1,
                (select r.*
                from imdb_0408.movies m ,imdb_0408.roles r 
                where m.id =r.movie_id 
                and m.`rank` is not null
                and m.`rank`>=%s) r2
                where r1.actor_id=r2.actor_id
                and r1.movie_id<r2.movie_id
                group by m1,m2"""

        cursor.execute(query, (rank,rank,))

        for a in cursor:
            result.append(a)

        cursor.close()
        conn.close()
        return result




