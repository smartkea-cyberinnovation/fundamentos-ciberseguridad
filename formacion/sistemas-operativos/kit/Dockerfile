# Imagen didactica; fijar digest verificado al preparar cada cohorte.
ARG PYTHON_IMAGE=python:3.13-slim
FROM ${PYTHON_IMAGE}
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY --chown=10001:10001 web.py /app/web.py
USER 10001:10001
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 CMD ["python", "-c", "import json,urllib.request; r=urllib.request.urlopen('http://127.0.0.1:8080/healthz',timeout=2); assert r.status==200 and json.load(r)['status']=='ok'"]
CMD ["python", "web.py", "--host", "0.0.0.0", "--port", "8080"]
