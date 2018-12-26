#!/usr/bin/env python3


import psycopg2

DBNAME = "news"


def create_view():
    try:
        db = psycopg2.connect(database=DBNAME)
        crs = db.cursor()
        crs.execute(" CREATE OR REPLACE VIEW article_pageviews AS"
                    " SELECT title,author,views FROM articles a"
                    " INNER JOIN ("
                    " SELECT path ,count('*') as views FROM log"
                    " WHERE path like '/article/%' and status='200 OK'"
                    " GROUP BY path"
                    " ) AS tp"
                    " on a.slug =  substring(tp.path from '/article/(.*)$') ;"
                    )
        crs.execute(" CREATE OR REPLACE VIEW log_day AS"
                    " SELECT date_trunc('day', time) as time_day,status"
                    " FROM log"
                    )
        db.commit()
        db.close()
        return True
    except Exception as e:
        print('Error : '+str(e))
        return False


if __name__ == '__main__':
    create_view()
