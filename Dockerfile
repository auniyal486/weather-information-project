FROM --platform=linux/amd64 python:3.9

WORKDIR /code
COPY ./ /code

RUN pip install --upgrade pip 
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
ENV PROD_ENV=True
## ; apk add build-base;
RUN pip install -r /code/requirements.txt

WORKDIR /code
EXPOSE 8080
EXPOSE 443

CMD ["python3", "manage.py", "runserver"]
