FROM huggingface/transformers-tensorflow-cpu:4.18.0

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

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

CMD ["uvicorn","main:app","--host", "0.0.0.0", "--port", "8000"]