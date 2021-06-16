FROM python:3.9

WORKDIR /usr/src/server

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 10000
EXPOSE 10001


CMD [ "python", "main.py" ]