FROM python:3.9
COPY requirements.txt /
RUN pip install -r requirements.txt
RUN pip install gunicorn
ADD main.py /
ENV PORT=8080
EXPOSE 8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app