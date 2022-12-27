FROM python:alpine3.17

WORKDIR /usr/src/app

COPY src/ /usr/src/app/

RUN pip install -r requirements.txt

CMD [ "./entrypoint.sh" ]
