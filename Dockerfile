# syntax=docker/dockerfile:1
FROM python:3.10.11-alpine
WORKDIR /code
ENV MONGO_DETAILS="mongodb+srv://Al5A7Qlifzo1usDM:Al5A7Qlifzo1usDM@cluster0.j1hcpju.mongodb.net/?retryWrites=true&w=majority"
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install "pymongo[srv]"
EXPOSE 8000
COPY . .
CMD ["python3", "app/main.py"]
