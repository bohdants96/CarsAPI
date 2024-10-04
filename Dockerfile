FROM python:3.12

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN apt upgrade

RUN useradd -rms /bin/bash car && chmod 777 /opt /run

WORKDIR /car

RUN mkdir /car/static && mkdir /car/media && chown -R car:car /car && chmod 755 /car

COPY --chown=car:car . .

RUN pip install -r requirements.txt

USER car

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]