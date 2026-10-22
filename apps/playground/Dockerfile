# Image du playground urban-json. Contexte de build = racine du dépôt
# (cf. docker-compose.yml) : le moteur et l'éditeur sont installés DEPUIS LES
# SOURCES du dépôt, pas depuis PyPI, pour que la machine de test serve
# exactement ce que porte la branche déployée.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /src
COPY packages/urban-json packages/urban-json
COPY packages/urban-json-editor packages/urban-json-editor
COPY apps/playground apps/playground

# Install non éditable : l'image ne dépend plus de /src à l'exécution. Le cœur
# et l'éditeur sont passés explicitement pour que pip ne les tire pas de PyPI.
RUN pip install ./packages/urban-json ./packages/urban-json-editor ./apps/playground \
    && useradd --system --uid 10001 --no-create-home playground

USER playground
EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2).status == 200 else 1)"

CMD ["uvicorn", "urban_json_playground.app:app", "--host", "0.0.0.0", "--port", "8000"]
