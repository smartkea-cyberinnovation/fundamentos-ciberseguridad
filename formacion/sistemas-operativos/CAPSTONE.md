# M32 · Capstone: operar, proteger, investigar y recuperar

**40 horas: 10 de teoría/seminarios y 30 de práctica**, divididas en L32A/B/C de 10 h cada una. Entrada: checkpoints C1–C5 y M31. Equipos de dos o tres alumnos, con defensa individual. Escenario ficticio, sin marca de una institución real.

## Encargo

Una pequeña organización necesita un servicio web interno, una estación de administración y usuarios de Linux, Windows y macOS. Debe poder inventariar, dar acceso, consultar estado, restaurar datos y explicar una actividad anómala. Los datos, identidades y registros son sintéticos. La cobertura nativa de cada SO debe indicarse expresamente: la falta de Mac no se oculta mediante una simulación.

El servicio no recibe datos personales ni se publica en Internet. Puede ser una web estática, API local de inventario o portal de estado. Si se implementa interfaz, será clara y accesible. Docker/Compose es una opción de empaquetado; el alumno justifica sus límites. Swarm/Kubernetes constituyen una extensión de arquitectura, no un requisito oculto para aprobar la administración básica.

## Seminarios teóricos: 10 horas

Arquitectura y amenazas 2 h; contrato de operación y mínimos de bastionado 2 h; preparación de evidencia y respuesta 2 h; recuperación y comunicación 2 h; revisión técnica y defensa de decisiones 2 h. Estas horas ya están incluidas en las 40.

## L32A · Construcción y operación: 10 h

**Objetivo:** entregar una solución operable por otra persona.

**Entorno:** redes internas, Linux servidor, Windows cliente/administrador y macOS asignado cuando esté disponible. Colector independiente o exportación controlada de logs.

**Tareas:** definir activos/usuarios/datos/flujos; fijar versiones; construir repositorio y runbook; preparar servicio con permisos mínimos; utilizar DNS/TLS de laboratorio; crear inventario con scripts propios; verificar GUI/CLI; preparar copia y restauración antes de simular incidentes.

**Evidencias:** diagrama; inventario sanitizado; matriz de acceso; configuración sin secretos; comprobaciones de servicio; código revisado con al menos seis pruebas, incluidas entradas inválidas; instrucciones desde entorno limpio.

**Éxito:** compañero reproduce la puesta en marcha; servicio responde solo por flujos previstos; cuentas separadas; ninguna credencial en Git; el alumno distingue dependencia del host y del contenedor.

**Recuperación:** snapshot/copia verificados y procedimiento de parada. Mantener la evidencia fuera de la VM que podría restaurarse.

## L32B · Bastionado y observabilidad: 10 h

**Objetivo:** demostrar mejoras de seguridad y detectar una desviación benigna.

**Tareas:** revisar baseline por sistema; registrar mínimo diez controles con evidencia y aplicabilidad; corregir al menos tres desviaciones aprobadas; probar usuario autorizado/no autorizado; configurar retención y campos mínimos; generar actividad normal; ejecutar un cambio benigno documentado que deba observarse, como alta autorizada o tarea de resumen; comprobar detección y cobertura.

**Evidencias:** baseline, excepciones, diffs, pruebas funcionales/negativas, registros correlacionados, hipótesis de detección, rollback y riesgo residual.

**Éxito:** se observa lo esperado con contexto y se explica lo no observable; no se desactiva protección para facilitar pruebas; después del cambio sigue funcionando el servicio y la recuperación.

**Recuperación:** retirar cuentas/tareas temporales y documentar. No limpiar logs del caso.

## L32C · Investigación, recuperación y defensa: 10 h

**Objetivo:** separar evidencia y conjetura, recuperar el servicio y presentar decisiones verificables.

**Incidencias disponibles:** configuración accidental con permiso insuficiente; servicio detenido; archivo sustituido en el dataset; evento sintético coincidente con un IOC; reloj desfasado o ausencia de ingestión. El docente elige dos, sin malware ni explotación. Uno debe tener explicación benigna alternativa.

**Tareas:** definir preguntas de triage y alcance; preservar originales y manifiestos; construir cronología; realizar búsqueda de IOCs sobre copias; confirmar o descartar con contexto; aplicar recuperación aprobada; medir duración y pérdida; preparar informe y demostración. IA puede revisar textos o código sintético, con registro y comprobación humana.

**Evidencias:** acta de recepción y cadena de custodia; consultas y resultados; línea temporal con zona y límites; informe técnico; resumen ejecutivo de dos páginas; restauración verificada; matriz de pruebas; registro de IA; defensa individual.

**Éxito:** conclusiones trazables, restauración funcional, permisos conservados y ausencia de exageraciones sobre compromiso/atribución. Otro alumno puede repetir el análisis desde la copia preservada.

**Recuperación:** cerrar accesos, aplicar retención y retirar recursos del laboratorio sin borrar material antes de evaluación.

## Rúbrica del proyecto: 100 puntos

| Dimensión | Puntos | Evidencia de nivel competente |
|---|---:|---|
| Arquitectura y reproducibilidad | 15 | Versiones, flujos, instalación y límites claros |
| Administración de los tres sistemas | 15 | GUI/CLI coherentes; cobertura nativa declarada |
| Scripting y calidad | 15 | Contratos, errores, seguridad, pruebas y revisión |
| Bastionado y secretos | 15 | Mínimo privilegio, baseline y excepciones verificadas |
| Observabilidad y detección | 10 | Fuentes, intervalos, correlación y cobertura |
| DFIR e interpretación | 15 | Originales, hashes, custodia y conclusiones proporcionales |
| Recuperación | 10 | Restauración demostrada y resultados medidos |
| Comunicación y uso de IA | 5 | Defensa comprensible, crítica y trazable |
| **Total** | **100** | |

Aprobado: al menos 70/100, todos los requisitos críticos y defensa individual satisfactoria. La parte de un SO sin evaluación nativa se declara pendiente: no se otorga una acreditación multiplataforma completa por analizar capturas.

## Requisitos críticos

No exponer el laboratorio; no incluir secretos/datos reales; disponer de recuperación; no alterar originales de evidencia; no ejecutar fuera de alcance; no atribuir resultados que no se hayan observado; no utilizar la IA como ejecutor o verificador único. Un incumplimiento crítico requiere remediación y repetición de la parte afectada antes de aprobar, aunque la nota aritmética sea alta.

## Defensa individual

El docente solicita un cambio pequeño no anunciado sobre datos sintéticos, una explicación de permisos, una lectura de log y una recuperación parcial. Se evalúa razonamiento y uso de ayuda, no memoria de opciones. Cada miembro explica un componente que no haya desarrollado en exclusiva.
