# A digest can be supplied as PYTHON_IMAGE for a release build.
ARG PYTHON_IMAGE=python:3.13-slim-bookworm
FROM ${PYTHON_IMAGE}
LABEL org.opencontainers.image.title="SmartKEA synthetic HTTP training service"
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /opt/lab
COPY --chown=10001:10001 web/app.py /opt/lab/app.py
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 CMD ["python3", "-c", "import json,urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=2); assert json.load(r)['status']=='ok'"]
CMD ["python3", "/opt/lab/app.py"]
