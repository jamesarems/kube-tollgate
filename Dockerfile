FROM python:3.7

RUN mkdir -p /kube-tollgate
WORKDIR /kube-tollgate
ADD . /kube-tollgate
RUN pip install -r requirements.txt

EXPOSE 2222
CMD ["python", "/kube-tollgate/main.py"]
