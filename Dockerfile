FROM registry.cn-hangzhou.aliyuncs.com/lovehome/base:latest

RUN apt update

ENV LANG=C.UTF-8

ENV LC_ALL=C.UTF-8

WORKDIR /workspace/lovehome

COPY ./ /workspace/lovehome

RUN pipenv install --system

EXPOSE 5000

ENV FLASK_ENV=production
# ENV MYSQL_SERVER=

ENTRYPOINT [ "uwsgi" ]

CMD [ "--ini" , "uwsgi_pro.ini"]
