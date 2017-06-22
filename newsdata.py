# "Database code" for the DB Forum.

import psycopg2, bleach

DBNAME = "news"


# Function to get most popular three articles of all time from the database
def get_articles():
    db = psycopg2.connect(database=DBNAME, user="postgres", host="localhost", password="Sandymask35")
    c = db.cursor()
    c.execute(
        "select articles.title ,count(*) as views from log ,articles "
        "where log.path like concat('%', articles.slug) "
        "group by articles.title order by views desc limit 3")
    articles = c.fetchall()
    print(articles)
    db.close()
    return articles


# Function to get who are the most popular article authors of all time
def get_authors():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME, user="postgres", host="localhost", password="Sandymask35")
    c = db.cursor()
    c.execute(
        "select authors.name ,count(*) as views from log ,"
        "articles,authors where log.path like concat('%', articles.slug) "
        "and authors.id= articles.author "
        "group by authors.name order by views desc")
    articles = c.fetchall()
    print(articles)
    db.close()
    return articles


# Function to get on which days did more than 1% of requests lead to errors
def get_max_error_day():
    db = psycopg2.connect(database=DBNAME, user="postgres", host="localhost", password="Sandymask35")
    c = db.cursor()
    c.execute("select day, perc from ("
              "select day, round((sum(requests)/(select count(*) from log where "
              "substring(cast(log.time as text), 0, 11) = day) * 100), 2) as "
              "perc from (select substring(cast(log.time as text), 0, 11) as day, "
              "count(*) as requests from log where status like '%404%' group by day)"
              "as log_percentage group by day order by perc desc) as final_query "
              "where perc >= 1")
    max_error_day = c.fetchall()
    print(max_error_day)
    db.close()
    return max_error_day


get_articles()
get_authors()
get_max_error_day()
