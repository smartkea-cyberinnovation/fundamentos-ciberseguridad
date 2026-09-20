# Plan docente y mapa curricular

## Finalidad y nivel de entrada

Aprender a administrar un equipo antes de interpretar su actividad como evidencia de seguridad. Se comienza sin experiencia en terminal. Requisitos: manejo básico de teclado y archivos, comprensión de instrucciones técnicas y acceso al laboratorio. El docente nivela mecanografía, rutas, instalación y lectura de errores; no presupone programación, redes o conocimientos de pentesting.

Al finalizar, el alumno debe poder describir el funcionamiento de un SO; operar archivos, identidades, procesos, almacenamiento y redes; automatizar de forma verificable; proteger y restaurar servicios; recopilar evidencia proporcional; contrastar hipótesis de incidente; comunicar límites de sus conclusiones; y revisar críticamente el uso de IA.

La formación no concede atribuciones periciales, acreditación oficial, equivalencia universitaria ni certificaciones de proveedores. Las horas constituyen una propuesta de carga didáctica, ajustable tras un piloto.

## Registro curricular

| ID | Módulo | T | P | Prerrequisitos principales |
|---|---|---:|---:|---|
| M01 | Diagnóstico, trabajo seguro y laboratorio | 5 | 9 | Ninguno |
| M02 | Representación de información y hardware | 5 | 9 | M01 |
| M03 | Arquitectura de SO, arranque y ejecución | 5 | 9 | M02 |
| M04 | Método de terminal, documentación y Git | 5 | 9 | M03 |
| M05 | Linux: shell, directorios y ficheros | 5 | 9 | M04 |
| M06 | Linux: texto, búsqueda y pipelines | 5 | 9 | M05 |
| M07 | Linux: usuarios, permisos y privilegios | 5 | 9 | M05 |
| M08 | Linux: procesos, paquetes, servicios y tareas | 5 | 9 | M06, M07 |
| M09 | Linux: almacenamiento, copias y recuperación | 5 | 9 | M07, M08 |
| M10 | Linux: red del host y control de exposición | 5 | 9 | M08 |
| M11 | Bash: programación estructurada | 5 | 9 | M06, M08 |
| M12 | Bash: automatización robusta y segura | 5 | 9 | M09, M10, M11 |
| M13 | Windows: arquitectura y administración GUI | 5 | 9 | M03, M04 |
| M14 | Windows: CMD y utilidades nativas | 5 | 9 | M13 |
| M15 | Windows: BAT y automatización heredada | 5 | 9 | M14, M11 |
| M16 | PowerShell: lenguaje, objetos y datos | 5 | 9 | M13, M15 |
| M17 | PowerShell: administración de Windows | 5 | 9 | M16 |
| M18 | Windows: identidad, red y acceso remoto | 5 | 9 | M10, M17 |
| M19 | Windows: eventos, protección y recuperación | 5 | 9 | M17, M18 |
| M20 | macOS: Darwin, APFS, GUI y terminal | 5 | 9 | M03, M05 |
| M21 | macOS: zsh, archivos y automatización | 5 | 9 | M11, M20 |
| M22 | macOS: usuarios, servicios, red y launchd | 5 | 9 | M10, M21 |
| M23 | macOS: controles de seguridad y evidencias | 5 | 9 | M19, M22 |
| M24 | Redes, acceso remoto y transferencias | 5 | 9 | M10, M18, M22 |
| M25 | Servicios web, TLS y operación segura | 5 | 9 | M12, M19, M23, M24 |
| M26 | Automatización multiplataforma y contenedores | 5 | 9 | M12, M16, M21, M25 |
| M27 | Logs, observabilidad y correlación temporal | 5 | 9 | M19, M23, M25 |
| M28 | DFIR: triage, preservación y análisis | 5 | 9 | M09, M27 |
| M29 | Threat hunting, IOCs y CTI operativa | 5 | 9 | M06, M16, M27, M28 |
| M30 | Auditoría técnica y perspectiva Red/Purple Team | 5 | 9 | M24, M25, M28, M29 |
| M31 | IA por terminal y supervisión de automatizaciones | 8 | 12 | M12, M16, M21, M28, M29 |
| M32 | Capstone: operar, proteger, investigar y recuperar | 10 | 30 | M01–M31 |
| **Total** | | **168** | **312** | **480 horas** |

## Método de impartición

Cada módulo ordinario ocupa siete sesiones de dos horas. Secuencia recomendada: problema y demostración GUI/CLI; modelo teórico y práctica A; teoría aplicada y práctica B; práctica C con menos ayudas; revisión, refactorización y defensa breve. Dentro de las 9 horas prácticas, A, B y C reciben 3 horas cada una. En M31 se asignan 4 horas por laboratorio; en M32, 10.

Antes de cada laboratorio: identificar equipo, usuario, directorio y efecto esperado; decidir qué requiere privilegios; crear un punto de recuperación cuando corresponda; anotar versión, reloj y alcance. Después: validar el resultado mediante una segunda observación, explicar errores, guardar evidencia minimizada y revertir los cambios temporales.

No se aprueba por copiar comandos. La pregunta recurrente es: qué estado cambia, qué permisos se necesitan, qué evidencia queda, cómo se comprueba y cómo se recupera.

## Diagnóstico inicial

En 45 minutos, sin calificación, cada alumno localiza un archivo, explica ruta absoluta y relativa, identifica su SO, abre una terminal, obtiene ayuda, guarda una salida y describe un error. Las tareas no realizadas originan apoyo, no exclusión. El docente registra autonomía, comprensión, uso de ayuda y accesibilidad. La adaptación no reduce los resultados mínimos de seguridad.

## Rutas de uso

**Completa: 480 horas.** 240 sesiones de dos horas, o 40 semanas de 12 horas. Incluye todos los módulos, evaluación y proyecto. El calendario real debe descontar descansos y días no lectivos; no se asignan fechas institucionales.

**Fundamentos operativos: 120 horas.** Selección de actividades: fundamentos 20; Linux 30; Bash 10; Windows y PowerShell 25; macOS 15; redes y copias 10; mini-proyecto 10. No equivale a superar los módulos íntegros ni habilita la especialización DFIR.

**Administración segura: 240 horas.** Fundamentos 28; Linux/Bash 60; Windows/PowerShell 56; macOS 28; redes, web y automatización 32; hardening y logs 20; proyecto 16. Requiere seleccionar ejercicios con los mismos criterios críticos de privacidad y recuperación.

**Introducción de 60 horas.** Fundamentos 12; Linux/terminal 16; scripting inicial 8; comparación Windows/macOS 10; redes y seguridad 6; proyecto 8. Permite explorar perfiles, no acreditar dominio intermedio-avanzado.

**Especialización profesional.** Tras superar el tronco o acreditar competencia mediante prueba: SysAdmin profundiza M08–M12/M17–M26; SOC en M19/M23/M27/M29; DFIR en M09/M19/M23/M27–M28; CTI en M06/M16/M29/M31; auditoría Red/Purple en M07/M18/M24/M30. No se suman automáticamente horas de rutas que reutilizan contenidos.

## Entregables longitudinales

Un cuaderno técnico versionado; un inventario sin secretos; un mapa de red y de permisos; una biblioteca de scripts con pruebas; un registro de cambios y excepciones de bastionado; un paquete de evidencia sintética con manifiesto; una cronología con incertidumbres; una restauración demostrada; y un informe ejecutivo de dos páginas. Se documenta cuándo se ha utilizado IA y qué parte se ha verificado de forma independiente.

## Checkpoints

C1 al cerrar M04: navegar, obtener ayuda y registrar cambios. C2 al cerrar M12: administrar Linux y automatizar sin privilegios innecesarios. C3 tras M19: explicar CMD/BAT frente a PowerShell y operar Windows nativo. C4 tras M23: trabajar con macOS y respetar sus controles. C5 tras M30: distinguir observación, hipótesis y conclusión, y preparar recuperación. C6 tras M32: defender una solución funcional y sus limitaciones.

El alumno que no supere un checkpoint realiza una tarea de recuperación sobre la competencia concreta; no repite mecánicamente todo el bloque. Ver [evaluación](EVALUACION.md).
