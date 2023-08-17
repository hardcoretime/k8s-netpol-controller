FROM python:3.10-slim-bullseye

COPY requirements.txt /tmp/

RUN pip install --upgrade --no-cache-dir pip==23.0.1 && \
      pip install --no-cache-dir --requirement /tmp/requirements.txt

COPY k8s_netpol_controller /k8s_netpol_controller

WORKDIR /k8s_netpol_controller

ENTRYPOINT [ "python", "__main__.py" ]
