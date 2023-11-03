# CONTRIBUTING

## How to build docker image
docker build -t flask-smorest-api .

## How to run Docker locally
'''
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" flask-smorest-api sh -c "flask run --host 0.0.0.0"
'''


## Setup database

'''
flask db upgrade
'''

### Migrate new changes
'''
flsk db migrate
flak db upgrade
'''
