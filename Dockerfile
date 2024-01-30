FROM python:3.11.3

RUN apt-get update && apt-get -y upgrade
RUN pip3 install --upgrade pip

WORKDIR /usr/src/int_plan_opt
COPY requirements.txt /usr/src/int_plan_opt/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/int_plan_opt
RUN python3 -m pytest --log-disable=main

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["main.py"]