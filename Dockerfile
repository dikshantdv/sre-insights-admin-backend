FROM python:3.10
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
EXPOSE 18000
CMD ["uvicorn","main:app","--host=0.0.0.0","--port=18000"]
