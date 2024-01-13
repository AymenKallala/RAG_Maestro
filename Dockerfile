FROM python:3.12.1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./config.yml /code/config.yml
COPY ./src /code/src/
COPY ./images/mithril_security_company_logo.jpeg /code/images/mithril_security_company_logo.jpeg

EXPOSE 8501

RUN pip install --no-cache-dir -r /code/requirements.txt


CMD ["streamlit", "run", "src/app.py"]