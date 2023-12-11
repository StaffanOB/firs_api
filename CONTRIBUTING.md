# CONTRIBUTING

## How to build docker image
docker build -t flask-smorest-api .

## How to run Docker locally
'''
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api sh -c "flask run --host 0.0.0.0"
'''
## Environments


### Local 
add .env file with the variable for the database url. Example in the repo

### Produciton
docker_entry_point file runs at app starup and ensures that that the database
migaration is run to update the database.

production have to have environmet variables set to beable to connect to the 
database.


## Setup database

'''
flask db upgrade
'''

### Migrate new changes
'''
flsk db migrate
flak db upgrade
'''
