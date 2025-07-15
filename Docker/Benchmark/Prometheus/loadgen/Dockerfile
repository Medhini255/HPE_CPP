FROM python:3.11
RUN pip install prometheus_client flask
COPY loadgen.py /loadgen.py
CMD ["python", "/loadgen.py"]
