FROM python:3.12

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/lukaszdoesthecode/List6_SoftEng.git

WORKDIR /List6_SoftEng

RUN pip install -r requirements.txt

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 9999

CMD ["/wait-for-it.sh", "db:5432", "--timeout=30", "--", "python", "manage.py", "runserver", "0.0.0.0:9999"]
