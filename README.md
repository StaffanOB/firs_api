# Firs API
This is a course test api

## Run the app
flask run

### monitor redis
docker run -w /app flask-smorest-api sh -c "rq worker -u rediss://red-cm2mioi1hbls73fqc35g:YFyYOAgLnwsltYk6yBOrtNzYowTvDlTV@frankfurt-redis.render.com:6379 emails"

## Servers

### Render.com
* API deployment 
* Redis queue


