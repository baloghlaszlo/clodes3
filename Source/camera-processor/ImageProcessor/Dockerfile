FROM clodes3/python-opencv

COPY * ./

RUN mkdir cascade && mv *.xml cascade/

RUN pip install -r requirements.txt

CMD ["/usr/local/bin/python3", "app.py"]