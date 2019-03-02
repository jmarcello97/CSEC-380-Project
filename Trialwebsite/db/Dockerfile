FROM mysql:5.7
COPY . /docker-entrypoint-initdb.d/database.sql
EXPOSE 3306
CMD ["mysqld"]
