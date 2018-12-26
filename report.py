#!/usr/bin/env python3


import psycopg2

DBNAME = "news"


def popularArticles():
    """ return the most three popular article """
    try:
        db = psycopg2.connect(database=DBNAME)
        crs = db.cursor()
        crs.execute(
                    "SELECT title,views FROM article_pageviews "
                    "ORDER BY views DESC limit 3 ;"
                   )
        # db.close()
        return crs.fetchall()
    except Exception as e:
        print('Error : '+str(e))
        return []


def popularArticlesAuthors():
    """ return the most three popular article author"""
    try:
        db = psycopg2.connect(database=DBNAME)
        crs = db.cursor()
        crs.execute(" SELECT name, sum(views) as sum_views"
                    " FROM article_pageviews v"
                    " INNER JOIN authors a on v.author = a.id"
                    " GROUP BY name order by sum_views desc ;"
                    )
        # db.close()
        return crs.fetchall()
    except Exception as e:
        print('Error : '+str(e))
        return []


def logPerDay():
    """ return wich days did more than 1% of requests lead to errors """
    try:
        db = psycopg2.connect(database=DBNAME)
        crs = db.cursor()
        crs.execute(" SELECT time_day,round(c_notok * 100 ,2)/total as percent"
                    " FROM ("
                    " SELECT time_day,count(*) as total FROM log_day"
                    " GROUP BY time_day"
                    " ) AS l1  LEFT JOIN ("
                    " SELECT time_day as day,count(*) as c_notok FROM log_day"
                    " WHERE status !='200 OK' GROUP BY day"
                    " ) AS l2 on l1.time_day = l2.day;"
                    )
        # db.close()
        return crs.fetchall()
    except Exception as e:
        print('Error : '+str(e))
        return []


def print_result(answer, lists):
    """ print results """
    print(answer)
    for a in lists:
        print("\t"+str(a[0])+" -- "+str(a[1]))


if __name__ == '__main__':
    # view = create_view()
    lists = popularArticles()
    print_result("1. The most popular three articles of all time:\n", lists)
    lists = popularArticlesAuthors()
    print_result("\n2. The most popular article authors of all time:\n", lists)
    logs = logPerDay()
    more_the_one = []
    for log in logs:
        if log[1] > 1:
            more_the_one.append(['{0:%B} {0:%d}, {0:%Y}'.format(log[0]),
                                round(log[1], 2)]
                                )
    print_result("\n3. Days did more than 1% of requests lead to errors:\n",
                 more_the_one)
