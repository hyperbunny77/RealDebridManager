FROM python:3.8-alpine
RUN mkdir /app
RUN mkdir /watch
RUN mkdir /config
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chmod a+x startscript.sh
ENTRYPOINT [ "/bin/sh", "startscript.sh" ]
