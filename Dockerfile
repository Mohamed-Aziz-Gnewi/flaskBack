FROM ubuntu:20.04
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python3" ]
EXPOSE 5000
CMD ["my_flask.py"]