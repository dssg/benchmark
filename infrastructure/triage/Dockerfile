FROM python:3.6

RUN mkdir /triage
RUN mkdir /code

## Upgrading all the installed python packages
RUN pip freeze — local | grep -v ‘^\-e’ | cut -d = -f 1 | xargs -n1 pip install -U

COPY requirements.txt /code

RUN pip install -r /code/requirements.txt

COPY run.py /code

ENTRYPOINT [ "python" , "/code/run.py" ]
