FROM python:3.7-stretch

ARG AppId
ENV AppId=${AppId}
ARG AppPassword
ENV AppPassword=${AppPassword}


WORKDIR /
RUN mkdir 1
COPY ./requirements.txt /1/requirements.txt
COPY ./main.py /1/main.py
COPY ./views.py /1/views.py
RUN mkdir bots
COPY bots /1/bots

RUN pip install -r /1/requirements.txt
RUN apt-get autoremove -y && \
    apt-get clean \
    && rm -rf /var/lib/apt/lists
CMD ["python", "/1/main.py"]