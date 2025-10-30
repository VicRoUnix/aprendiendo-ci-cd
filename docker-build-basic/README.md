# Como usar docker con github actions
* Como se puede crear una imagen en DOcker propia, contenerizar la app de python y automatizar todo ese proceso con github Actions

Para ello crearemos un repositorio local y crearemos una aplicacion python para probar.
---

## 1.Crear un DockerFile
* Crearemos el entorno
``` bash
git clone https://github.com/Tu-usuario/app-python.git
cd app-python
```
* Toca el Dockerfile
```txt
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-chache-dir -r requirements.txt

COPY app.py

RUN adduser --disabled-password --gecos '' appuser && \ 
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries-3 \
CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
```

---

## 3.Crearemos un .dockerignore
```bash
nano .dockerignore
```
```txt
.git
__pycache__/
*.pyc
tests/
venv/
.dockerignore
Dockerfile
```

## 3. Testearemos localmente su funcionamiento 
```bash
docker build -t app-python:test .
docker run -d --name app-test -p 5000:5000 app-python:test
curl http://localhost:000/health
docker stop app-test && docker rm app-test
```

## 4.Crearemos Workflow de Build Docker 
```bash
nano .github/workflows/docker-build.yml
```
```yml
name: Build Docker

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Setup Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login al Github Container Registry
      if: github.event_name != 'pull_request'
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Extraer metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=sha
          type=raw,value=latest,enable={{is_default_branch}}
    
    - name: BUild Docker
      uses: docker/build-push-action@v6
      with:
        context: .
        load: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}

    - name: Testear contenedor
      run: |
        IMAGE_TAG=$(echo "${{ steps.meta.outputs.tags }}" | head -n1)
        docker run -d --name test-container -p 5000:5000 $IMAGE_TAG
        sleep 10
        curl -f http://localhost:5000/health
        curl -f http://localhost:5000/
        docker stop test-container && docker rm test-container

    - name: Push Docker images
      if: github.event_name != 'pull_request'
      uses: docker/build-push-action@v6
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
```

## Desglose

A continuación se explica cada campo y bloque usado en el workflow `docker-build.yml`.

### `name`

El nombre del flujo de trabajo (workflow). En este repo se usa: `Build Docker`.

### `on`

Define los eventos que disparan (activan) el workflow.

- `push`: se activa cuando se hace un push.
  - `branches`: especifica a qué ramas aplica el trigger (aquí: `main` y `develop`).
- `pull_request`: se activa al crear/actualizar un pull request.
  - `branches`: aquí solo se activa para PRs dirigido a `main`.

### `env`

Variables de entorno disponibles para todos los jobs y steps:

- `REGISTRY`: `ghcr.io` (GitHub Container Registry).
- `IMAGE_NAME`: usa `github.repository` (ej. `usuario/repo`).

### `jobs` y `build-and-test`

Describe los trabajos a ejecutar. En este caso hay un job `build-and-test` con:

- `runs-on`: `ubuntu-latest` (runner donde se ejecuta el job).
- `permissions`: permisos del `GITHUB_TOKEN` para este job:
  - `contents: read` — necesario para `actions/checkout`.
  - `packages: write` — necesario para publicar imágenes en GHCR.

### `steps`

Secuencia de pasos dentro de `build-and-test` (resumen):

- **Checkout**
  - `uses: actions/checkout@v4` — clona el repo en el runner.

- **Setup Docker Buildx**
  - `uses: docker/setup-buildx-action@v3` — configura Buildx (construcción multi-plataforma y mejor performance).

- **Login al Github Container Registry** (solo fuera de PRs)
  - Condición: `if: github.event_name != 'pull_request'`.
  - `uses: docker/login-action@v3`.
  - `with`:
    - `registry: ${{ env.REGISTRY }}`
    - `username: ${{ github.actor }}`
    - `password: ${{ secrets.GITHUB_TOKEN }}`

- **Extraer metadata**
  - `id: meta`
  - `uses: docker/metadata-action@v5` — genera tags y labels automáticos.
  - `with`:
    - `images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}`
    - `tags:`
      ```text
      type=sha
      type=raw,value=latest,enable={{is_default_branch}}
      ```
    - Esto produce, por ejemplo, un tag por SHA y `latest` si es la rama por defecto.

- **Build Docker**
  - `uses: docker/build-push-action@v6` con:
    - `context: .` — directorio raíz donde está el `Dockerfile`.
    - `load: true` — carga la imagen en el daemon del runner para poder probarla localmente.
    - `tags: ${{ steps.meta.outputs.tags }}`
    - `labels: ${{ steps.meta.outputs.labels }}`

- **Testear contenedor**
  - `run:` — comandos que arrancan un contenedor desde la imagen recién construida y prueban endpoints:
    ```bash
    IMAGE_TAG=$(echo "${{ steps.meta.outputs.tags }}" | head -n1)
    docker run -d --name test-container -p 5000:5000 $IMAGE_TAG
    sleep 10
    curl -f http://localhost:5000/health
    curl -f http://localhost:5000/
    docker stop test-container && docker rm test-container
    ```
  - `-f` en `curl` fuerza fallo si el status HTTP no es 2xx.

- **Push Docker images** (solo fuera de PRs)
  - Condición: `if: github.event_name != 'pull_request'`.
  - `uses: docker/build-push-action@v6` con:
    - `context: .`
    - `push: true` — sube la(s) imagen(es) al registro.
    - `tags: ${{ steps.meta.outputs.tags }}`
    - `labels: ${{ steps.meta.outputs.labels }}`

### Notas adicionales

- `load: true` permite ejecutar la imagen en el runner (útil para tests rápidos) pero no es necesario cuando solo quieres push.
- Asegúrate de tener habilitado `packages: write` si quieres publicar en `ghcr.io`.

Fin del desglose.