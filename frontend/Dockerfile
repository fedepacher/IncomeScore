FROM python:3.10.11-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

COPY . ./frontend

COPY .streamlit ./.streamlit

COPY initializer.sh .

RUN chmod +x initializer.sh

EXPOSE 8080

ENTRYPOINT [ "./initializer.sh" ]