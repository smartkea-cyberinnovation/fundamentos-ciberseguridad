# Laboratorios Linux de SmartKEA

El laboratorio combina una caja de herramientas Kali con un objetivo HTTP sintético. Los contenedores ejecutan Linux real sobre el kernel de la máquina anfitriona y mantienen el trabajo en un volumen del proyecto. La terminal web es opcional y empieza en modo lectura.

**Empieza por [la guía de laboratorios](../docs/LABS.md).** Para practicar administración con `sudo`, servicios del sistema y Docker, usa una VM dedicada: [máquina real y Cloudflare Access](../docs/CONEXION-TTYD.md). El despliegue [Swarm](../docs/SWARM.md) dispone de su propio stack, imágenes preconstruidas y secretos externos.

Desde la carpeta que contiene `labs/`:

```bash
docker compose -f labs/compose.yaml build web toolbox
docker compose -f labs/compose.yaml up -d --wait web
docker compose -f labs/compose.yaml run --rm toolbox
```

Dentro de Kali:

```bash
id
pwd
curl --fail --silent --show-error http://web:8080/health | jq
nmap -sT -Pn -sV --version-light -p 8080 web
/opt/lab/bin/make-fixtures.sh /workspace/evidence-synthetic
/opt/lab/bin/verify-evidence.sh /workspace/evidence-synthetic
```

El código se ha preparado para Linux y Docker Compose v2. Las comprobaciones ejecutadas y las que necesitan la máquina anfitriona figuran en [VALIDATION.md](../docs/VALIDATION.md).
