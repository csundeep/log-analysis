#! python3.7
import psycopg2

DBNAME = "news"


# Function to get most popular three articles of all time from the database
def get_articles():
    # db = psycopg2.connect(database=DBNAME, user="postgres", host="localhost", password="Sandymask35")
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "select articles.title, views from articles, "
        " (select path, count(*) as views from log "
        "  group by path) as log "
        "where log.path like concat('%', articles.slug) "
        "order by views desc limit 3")
    articles = c.fetchall()
    db.close()
    return articles


# Function to get who are the most popular article authors of all time
def get_authors():
    """Return all posts from the 'database', most recent first."""
    # db = psycopg2.connect(database=DBNAME, user="postgres", host="localhost", password="Sandymask35")
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        "select authors.name,sum(views) as total_views from authors "
                "JOIN ( select a.author as authorId, b.views as views from "
                "articles as a join(select path,count(*) as views from log "
                "where path like '/article/%' GROUP BY path) as b on "
                "b.path = concat('/article/',a.slug)) article_views on "
                "authors.id = article_views.authorId GROUP BY authors.name "
                "order by sum(views) DESC")
    articles = c.fetchall()
    db.close()
    return articles


# Function to get on which days did more than 1% of requests lead to errors
def get_max_error_day():
    # db = psycopg2.connect(database=DBNAME, user="postgres", host="localhost", password="Sandymask35")
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from (select A.date as date,"
                  "round(100.0*B.error/A.views,2) as error_perct from"
                  "(SELECT time::date as date,count(*) as views from log "
                  "group by time::date) A,(SELECT time::date as date,"
                  "count(*)as error from log  where status like '404 %' "
                  "group by time::date) B where A.date=B.date) error "
                  "where error_perct >1.0")
    max_error_day = c.fetchall()
    db.close()
    return max_error_day


# Function to print top three articles from the database.
def print_top_articles():
    articles = get_articles()
    print("1. What are the most popular three articles of all time?")
    print("*************************************************")
    print("*  {:<34}| {:<9}*".format("Article", "Views"))
    print("*************************************************")
    for article in articles:
        print("* {:<35}| {:<8} *".format(str(article[0]), str(article[1])))
    print("*************************************************\n")


# Function to print the popular authors of all time.
def print_top_authors():
    authors = get_authors()
    print("2. Who are the most popular article authors of all time?")
    print("***************************************")
    print("*  {:<24}| {:<9}*".format("Author", "Views"))
    print("***************************************")
    for author in authors:
        print("* {:<25}| {:<8} *".format(str(author[0]), str(author[1])))
    print("***************************************\n")


# Function to print which day we had more than 1% error requests to the server
def print_max_error_day():
    max_error_day = get_max_error_day()
    print("3. On which days did more than 1% of requests lead to errors?")
    print("************************")
    print("*  DATE      | Percent *")
    print("************************")
    for day in max_error_day:
        print("* {:<10} | {:<6}  *".format(str(day[0]), str(day[1])))
    print("************************")


print_top_articles()
print_top_authors()
print_max_error_day()
