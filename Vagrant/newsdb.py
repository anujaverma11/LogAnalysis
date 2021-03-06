#!/usr/bin/env python3
# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

DBNAME = "news"


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def get_popular_articles():
    """ 1. What are the most popular three articles of all time?"""
    db, cursor = connect()

    query = """
            select * from popular_articles limit 3
            """
    cursor.execute(query)
    articles = cursor.fetchall()
    # print (articles)
    for i in range(len(articles)):
        print("%s - %d views" % (articles[i][0], articles[i][1]))
    db.close()


def get_popular_authors():
    """ 2. Who are the most popular article authors of all time?"""
    db, cursor = connect()
    query = """
              select name, popularity
              from authors join popular_article_authors
              on popular_article_authors.author = authors.id;
              """
    cursor.execute(query)
    authors = cursor.fetchall()
    # print (authors)
    for i in range(len(authors)):
        print("%s - %d views" % (authors[i][0], authors[i][1]))

    db.close()


def get_error_details():
    """ 3. On which days did more than 1% of requests lead to errors?"""
    db, cursor = connect()

    query = "select * from request_errors;"
    cursor.execute(query)
    req_errors = cursor.fetchall()
    # print (req_errors)

    for i in range(len(req_errors)):
        error_percent = req_errors[i][1] * 100
        print(req_errors[i][0] + " - %.2f" % (error_percent) +
              "%" + " errors")
    db.close()

if __name__ == "__main__":
    print("Most Popular Three Articles of all times")
    print("-" * 30)
    get_popular_articles()
    print("\n\n")
    print("Most Popular Article Authors of all times")
    print("-" * 30)
    get_popular_authors()
    print("\n\n")
    print("Days when more than 1% request lead to error")
    print("-" * 30)
    get_error_details()
