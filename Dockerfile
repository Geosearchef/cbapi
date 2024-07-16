FROM python:3.12.4-bookworm

WORKDIR /src

COPY . .

RUN pip install -r /src/requirements.txt
RUN pip install gunicorn

EXPOSE 8000

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:8000", "-w", "1", "cbapi:app" ]
