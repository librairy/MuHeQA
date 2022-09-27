FROM huggingface/transformers-tensorflow-cpu:4.18.0

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY *.py /app/
COPY application/ /app/application/

WORKDIR /app

RUN curl https://delicias.dia.fi.upm.es/nextcloud/index.php/s/Jp5FeoBn57c8k4M/download --output /app/resources.zip
RUN  apt-get update -y && \
     apt-get clean
RUN apt-get install -y unzip
RUN unzip /app/resources.zip -d /app/

#ENTRYPOINT ["python3"]
CMD ["uvicorn","main:app"]