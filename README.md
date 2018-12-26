# Logs analysis project 
 ## What is this project?
This project is a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the `psycopg2` module to connect to the database.

This project responds to three questions :
**1. What are the most popular three articles of all time?**
**2. Who are the most popular article authors of all time?**
**3. On which days did more than 1% of requests lead to errors?** 
There is a **Function** for each question .

First, you must create the database views by running :
```
python3 create_views.py
```
or using ***psql***, connect to database news
 ``` >> psql news ```
 Then type the View definition :
 ```
  CREATE OR REPLACE VIEW article_pageviews AS
  SELECT title,author,views FROM articles a
  INNER JOIN (
         SELECT path ,count('*') as views FROM log
         WHERE path like '/article/%' and status='200 OK'
         GROUP BY path
  ) AS tp on a.slug =  substring(tp.path from '/article/(.*)$') ;
```
```
CREATE OR REPLACE VIEW log_day AS
 SELECT date_trunc('day', time) as time_day,status FROM log
```

To run the programme type :
```
python3 report.py
```
 ### Response Exemple: 
 1. The most popular three articles of all time:

	Candidate is jerk, alleges rival -- 338647
	
	Bears love berries, alleges bear -- 253801
	
	Bad things gone, say good people -- 170098

2. The most popular article authors of all time:

	Ursula La Multa -- 507594
	
	Rudolf von Treppenwitz -- 423457
	
	Anonymous Contributor -- 170098
	
	Markoff Chaney -- 84557

3. Days did more than 1% of requests lead to errors:

	July 17, 2016 -- 2.27


