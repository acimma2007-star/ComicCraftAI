<<<<<<< HEAD
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

=======
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

>>>>>>> 4259a77dbb679077cc99e1d64f91f77e46761268
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]