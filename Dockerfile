FROM python:3.12-slim

WORKDIR .

COPY requirements.txt ./requirements.txt
COPY ./ ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
