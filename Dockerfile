# syntax=docker/dockerfile:1

FROM python:3.8
WORKDIR /app
RUN python -m venv .venv
RUN . .venv/bin/activate
RUN python -m pip install --upgrade pip wheel setuptools
COPY . .
RUN pip install -r requirements.txt
# RUN pip install -e .
EXPOSE 5000:5000
CMD ["flask", "run", "--host=0.0.0.0"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD [ "python3", "-m" , "http.server"]