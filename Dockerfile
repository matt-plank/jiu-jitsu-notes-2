FROM python:3.12

WORKDIR /app

COPY tailwind.config.js tailwind.config.js

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY pyproject.toml pyproject.toml
COPY jiu_jitsu_notes jiu_jitsu_notes
RUN pip install .

COPY templates templates
RUN tailwindcss -o templates/css/tailwind.css

EXPOSE 8000

CMD ["sh", "-c", "uvicorn jiu_jitsu_notes.app:app --host 0.0.0.0 --port $PORT"]
