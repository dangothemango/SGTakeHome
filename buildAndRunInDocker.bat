python3 -m unittest discover -s src \
&& \
docker build -t sgth:latest . \
&& \
docker run -d --name SGTakeHome-dgorman -p 8099:8099 -ti sgth:latest
