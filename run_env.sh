
port_server=5000
port_ex=5000
image_name=flask-smorest-api

#docker run -dp $port_ex:$port_server -w /app -v "$PWD:/app" $image_name
docker run -d --name first-api -dp $port_ex:$port_server -w /app -v "$(pwd):/app" $image_name sh -c "flask run --host 0.0.0.0"
