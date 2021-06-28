#Docker File, image, container

FROM python:3.8

ADD toptrendingsubreddits.py .

RUN pip install luigi requests schedule

C["python","toptrendingsubreddits.py"]MD 