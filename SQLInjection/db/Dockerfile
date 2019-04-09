FROM mysql:5.7
#COPY . /docker-entrypoint-initdb.d/database.sql
ADD user_db.sql /docker-entrypoint-initdb.d
EXPOSE 3306
#CMD ["mysqld"]
