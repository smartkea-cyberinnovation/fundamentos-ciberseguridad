# Plantillas de trabajo y evidencias

Copiar la plantilla necesaria a una carpeta local de entrega. Rellenar con datos sintéticos. Las evidencias reales autorizadas se custodian fuera de Git con controles específicos. Una carpeta no separa permisos de acceso dentro del mismo repositorio.

## 1. Ficha de entorno

- ID de equipo/imagen de laboratorio:
- SO, edición, versión, arquitectura y parche:
- Hipervisor/capa de ejecución y recursos:
- Shell/motor, versión y módulos:
- Cuenta de práctica y privilegios autorizados:
- Red, rutas y flujos aprobados:
- Reloj, zona y sincronización:
- Fuentes de logs activas y retención:
- Snapshot/copia, ubicación y prueba de recuperación:
- Licencias/procedencia y limitaciones:

## 2. Entrega de laboratorio

- ID y título; alumno/equipo; edición del curso:
- Objetivo y criterios de éxito:
- Alcance, activos y acciones permitidas:
- Preparación y comprobación de permisos:
- Pasos realizados y comandos explicados:
- Resultados esperados frente a observados:
- Errores, hipótesis y resolución:
- Evidencias: nombre, origen, hora y hash cuando proceda:
- Prueba positiva y negativa:
- Reversión/restauración y comprobación:
- Uso de IA y validación independiente:
- Límites y siguiente mejora:

## 3. Cambio y excepción

| Campo | Valor a completar |
|---|---|
| ID/objetivo/propietario | |
| Activo y servicio afectado | |
| Estado observado y evidencia | |
| Estado deseado y referencia | |
| Impacto, dependencia y riesgo | |
| Aprobación y ventana | |
| Pasos de implementación | |
| Prueba funcional y de restricción | |
| Copia previa y rollback | |
| Resultado y riesgo residual | |
| Excepción, compensación y expiración | |

## 4. Manifiesto de evidencia

Para cada elemento: ID; nombre/ruta lógica; procedencia; tamaño; formato; algoritmo y hash; fecha/hora original; zona; fecha/hora de recepción; herramienta/versión; operador ficticio; permisos; ubicación del original; copia de trabajo; relación con otros elementos; observaciones.

Registrar cada transferencia de custodia: quién entrega/recibe, cuándo, finalidad, identificador, comprobación de integridad y condición del soporte. No presentar esta plantilla por sí sola como garantía jurídica de admisibilidad.

## 5. Línea temporal

| Hora original | Zona original | Hora normalizada | Host/fuente | Evento/acción | Usuario ficticio | Evidencia | Confianza/limitación |
|---|---|---|---|---|---|---|---|

Conservar el texto de timestamp original, precisión y cualquier ajuste de desfase. Una conversión no debe sobrescribir la fuente.

## 6. Indicador e hipótesis de búsqueda

- Tipo y valor original:
- Valor normalizado y algoritmo si corresponde:
- Fuente, fecha de recepción y vigencia:
- Confianza y contexto:
- Pregunta operativa:
- Dataset/campo/intervalo y cobertura:
- Semántica de coincidencia exacta/subdominio/patrón:
- Consulta y versión:
- Controles positivos y negativos:
- Resultados y corroboración:
- Falsos positivos/omisiones/limitaciones:
- Acción propuesta y validación humana:

## 7. Contrato de script

Propósito; no objetivos; intérprete/versión; privilegios; entradas y límites; salida/esquema; exit codes; efectos; ficheros creados; red utilizada; datos sensibles; modo consulta/dry-run; timeout; concurrencia; errores parciales; temporales; pruebas; rollback; dependencias; licencia y responsable.

## 8. Registro de IA

Herramienta/modelo/versión; modo local/remoto; fecha; propósito; categorías de datos; medidas de minimización; permisos efectivos; prompt sanitizado; salida utilizada; observaciones rechazadas; pruebas independientes; revisor; coste/latencia cuando se midan; conservación y eliminación.

## 9. Informe de hallazgo

Título concreto; alcance; condición observada; evidencia; consecuencia plausible; hipótesis alternativa; referencia de control; prioridad justificada; acción correctiva; responsable; plazo propuesto; prueba de éxito; resultado del retest; límites. Evitar calificar una vulnerabilidad como explotada si no hay evidencia de explotación.

## 10. Prueba de recuperación

Servicio/datos; punto de recuperación; copia elegida; integridad; claves de recuperación custodiadas; destino de restauración; pasos; tiempo medido; pérdida medida; permisos; prueba funcional; diferencias; RPO/RTO objetivo frente a conseguido; resultado; mejoras.
