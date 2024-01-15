FROM python:3.12.1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./config.yml /code/config.yml
COPY ./src /code/src/
COPY ./.streamlit /code/.streamlit/
COPY ./images/maestro.png /code/images/maestro.png
COPY ./images/streamlit_app.png /code/images/streamlit_app.png

EXPOSE 8501

RUN pip install --no-cache-dir -r /code/requirements.txt


CMD ["streamlit", "run", "src/app.py"]