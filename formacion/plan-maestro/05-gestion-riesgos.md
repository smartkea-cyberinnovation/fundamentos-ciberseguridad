# 05 · Gestión de riesgos: método, cálculos y decisiones

[Índice](README.md) · [Controles](04-controles-correspondencias.md) · [Datos del caso](riesgo-ejemplo.json) · [Fuentes](09-fuentes.md)

## Objetivos de aprendizaje

Formular escenarios; distinguir amenaza, vulnerabilidad e impacto; decidir qué datos faltan; evaluar con escalas explícitas; separar situación inherente, actual y objetivo; seleccionar controles; calcular un ejemplo sin falsa precisión; registrar una decisión de tratamiento y comprobarla.

NIST SP 800-30 orienta la evaluación de riesgos; ISO/IEC 27005 aporta guía de gestión de riesgos de seguridad de la información en relación con un SGSI. MAGERIT/PILAR es otra referencia útil para activos, dependencias y salvaguardas. No se presentará una fórmula única como exigida por todos los métodos. FAIR, EBIOS RM e integración ERM con la serie NIST 8286 quedan como lecturas de ampliación a validar antes de desarrollarlas. [S03, S06, S10]

## Vocabulario y estados

**Amenaza:** posible causa o fuente de un evento dañino. **Vulnerabilidad:** debilidad relevante para el escenario. **Exposición:** condiciones que ponen el activo al alcance del evento. **Impacto:** consecuencia sobre objetivos y personas. **Riesgo:** incertidumbre sobre objetivos, expresada mediante escenario, posibilidad/frecuencia y consecuencias, no solo mediante un número.

**Inherente:** valoración respecto de una línea base explícita sin las salvaguardas que se decida descontar. **Actual:** riesgo con controles realmente existentes y evidencia de operación. **Objetivo:** riesgo estimado después de aplicar un tratamiento todavía propuesto. **Residual:** riesgo que permanece después de los controles considerados; distinguir residual actual comprobado de residual objetivo previsto. La organización debe fijar la semántica y aplicarla consistentemente.

Un control comprado no equivale a implantado; implantado no equivale a eficaz; eficaz en una prueba no garantiza eficacia universal. El estado objetivo no se etiqueta como riesgo ya reducido.

## Proceso de doce pasos

1. **Contexto:** servicio, objetivos, alcance, horizonte, partes afectadas y restricciones. Identificar propietario del riesgo y autoridad de aceptación.
2. **Criterios:** definir impacto, escalas, unidades, tolerancia, apetito y reglas de escalado antes de puntuar.
3. **Inventario y dependencias:** servicios, datos, activos, identidades, proveedores y recursos físicos/humanos.
4. **Escenarios:** causa/fuente → evento → activo/proceso afectado → consecuencia. Formular también escenarios no maliciosos.
5. **Evidencia:** incidentes históricos, pruebas, cobertura, exposición, inventario, contratos; separar datos de supuestos.
6. **Análisis inherente:** usar línea base documentada, sin descontar dos veces el mismo control.
7. **Controles actuales:** registrar objetivo, alcance, diseño, implantación, cobertura, operación, prueba y fallo posible.
8. **Análisis actual:** reevaluar posibilidad/frecuencia e impacto con evidencia de controles, no con un porcentaje genérico.
9. **Evaluación y priorización:** comparar con criterios; considerar obligaciones, urgencia, dependencia y capacidad, no solo ranking numérico.
10. **Tratamiento:** evitar, reducir, compartir/transferir o aceptar con autoridad; asignar coste, responsable, plazo, hitos y riesgo objetivo.
11. **Verificación:** implantar, probar, medir riesgo residual y registrar limitaciones. Reabrir la decisión si el control no logra el efecto esperado.
12. **Seguimiento:** revisar por fecha y por cambio de amenaza, servicio, proveedor, incidente, ley o calidad de evidencia.

## Modelo cualitativo: útil, pero no monetario

Puede usarse una matriz 5×5 si se definen categorías con ejemplos y límites. Por ejemplo, probabilidad ordinal de excepcional a muy frecuente e impacto de limitado a extremo sobre un horizonte definido. El producto de dos ordinales es **un índice de priorización acordado**, no una probabilidad ni una pérdida en euros.

| Ejemplo de escala de impacto | Qué debe definirse antes del caso |
|---|---|
| Operación | Duración y extensión de interrupción; servicios afectados |
| Financiero | Bandas de pérdida y qué partidas incluyen |
| Personas/privacidad | Daños a derechos, seguridad o bienestar; reversibilidad y afectados |
| Legal/contractual | Obligación aplicable, condición de incumplimiento y consecuencias plausibles |
| Reputación/confianza | Evidencia de efecto, población y horizonte; no multiplicadores arbitrarios |

No sumar ni promediar escalas de distintas dimensiones sin justificar una regla. Cuando una consecuencia crítica para personas impone escalado, no debe diluirse entre puntuaciones económicas bajas. La escala requiere calibración con ejemplos y revisión entre evaluadores.

## Ejemplo cuantitativo completo, con supuestos sintéticos

**Escenario R-001:** interrupción del portal por modificación no autorizada de configuración. **Horizonte:** un año. **Unidad de frecuencia:** eventos/año; **unidad de severidad:** euros/evento. Todas las cifras y eficacias siguientes son inventadas para docencia; no describen una empresa real ni una eficacia probada de un fabricante.

Supuesto simplificador: frecuencia y severidad media permiten aproximar una pérdida anual esperada. Si existe dependencia entre ambas, heterogeneidad de incidentes o fuerte cola de pérdidas, este producto no representa por sí solo la distribución completa.

| Variable | Línea base inherente | Situación actual ilustrativa | Objetivo ilustrativo |
|---|---:|---:|---:|
| Frecuencia anual | 0,40 | 0,30 | 0,14 |
| Pérdida media por evento | 120.000 € | 108.000 € | 96.000 € |
| Pérdida anual esperada | 48.000 € | 32.400 € | 13.440 € |

**Cálculo:** ALE = frecuencia anual × pérdida media por evento. Inherente: 0,40 × 120.000 = 48.000 €/año. Actual: reducción de frecuencia del 25 % y de severidad del 10 % respecto de la misma base, esto es 0,40 × 0,75 × 120.000 × 0,90 = 32.400 €/año. Objetivo: reducción de frecuencia del 65 % y de severidad del 20 % respecto de esa base: 0,40 × 0,35 × 120.000 × 0,80 = 13.440 €/año.

El tratamiento objetivo combina medidas de acceso/cambio con detección y restauración. Los porcentajes representan la hipótesis conjunta del escenario, **no eficacias independientes de productos que puedan multiplicarse sin más**. La restauración suele actuar sobre determinadas consecuencias y duraciones; no debe descontarse como si impidiera todo evento.

**Decisión incremental:** la mejora se compara con el estado actual, no con el inherente. Reducción esperada: 32.400 − 13.440 = **18.960 €/año**. Si el coste anual equivalente adicional fuese 12.000 €, el beneficio neto esperado ilustrativo sería **6.960 €/año**. La razón `(reducción − coste) / coste` sería **58 %**, bajo esos supuestos; no constituye una rentabilidad garantizada ni una justificación suficiente para obligaciones legales o impactos a personas.

Comparar inherente y objetivo produciría 34.560 €/año de diferencia, pero atribuirla íntegramente a la nueva inversión sobrevaloraría el tratamiento, porque parte del efecto ya existe. Éste es un error que la práctica debe detectar.

**Frecuencia no es probabilidad:** 0,40 eventos/año no equivale necesariamente a un 40 % de probabilidad anual de al menos un evento. Con un modelo Poisson homogéneo asumido, esa probabilidad sería `1 − exp(−0,40) ≈ 32,97 %`; el curso debe declarar el modelo, no darlo por cierto.

## Sensibilidad e incertidumbre

Ensayar frecuencia inherente 0,2–0,6 y pérdida media 60.000–180.000 manteniendo, solo para ilustrar, los factores de reducción. Los extremos aritméticos de ALE inherente van de 12.000 a 108.000 €/año; los del objetivo, de 3.360 a 30.240 €/año. **No son un intervalo de confianza** ni percentiles: faltan distribuciones y dependencias.

El ejercicio debe encontrar la condición de equilibrio: reducción anual incremental = coste anual adicional. Identificar qué supuesto cambia la decisión antes de recomendar recopilar más datos. En niveles avanzados, utilizar escenarios discretos o simulación reproducible y explicar distribución, correlación, semillas y límites; no reemplazar datos por una simulación vistosa.

## Dos escenarios complementarios

**R-002 — indisponibilidad por energía.** Evento no malicioso; infraestructura física y dependencia del proveedor. Controles: alimentación protegida, redundancia apropiada, plan de recuperación y prueba. Un EDR no reduce directamente un corte eléctrico; un segundo servicio en el mismo edificio puede compartir el fallo.

**R-003 — divulgación de datos personales.** Consecuencias para personas, además de coste empresarial. Controles: minimizar datos, limitar acceso, conservación, cifrado y respuesta. La pérdida financiera baja no implica riesgo bajo para los afectados. Analizar necesidad de EIPD y obligaciones con el marco aplicable. [S07, S09]

## Diseño y prueba de controles

| Capa de valoración | Pregunta | Evidencia |
|---|---|---|
| Adecuación del diseño | ¿El mecanismo actúa sobre este escenario? | Análisis de amenaza, objetivo y limitaciones |
| Implantación | ¿Está instalado y configurado donde corresponde? | Configuración efectiva, inventario y cambios |
| Cobertura | ¿Qué activos/usuarios/flujos cubre? | Denominador y activos no cubiertos |
| Operación | ¿Se mantiene y se utiliza correctamente? | Registro de revisión, respuesta y actualización |
| Eficacia | ¿La prueba consigue el resultado esperado? | Positivos/negativos, resultado y condiciones |
| Dependencia | ¿Qué fallo común podría anular varias medidas? | Proveedor, IAM, red, energía y cuentas compartidas |

No aplicar `riesgo residual = inherente × (1 − suma de porcentajes)` de forma genérica. Las medidas pueden solaparse, fallar juntas, afectar componentes distintos o introducir nuevos riesgos. Documentar compensaciones y degradación cuando un control no puede operar.

## Registro y tratamiento

Para cada riesgo: ID, servicio, dueño, escenario, afectados, amenaza, vulnerabilidad/condiciones, horizonte, unidades, evidencia, incertidumbre, inherente, controles actuales y pruebas, actual, opción de tratamiento, coste y fuente, responsable, vencimiento, objetivo, criterio de aceptación, autoridad, residual verificado y próxima revisión.

**Evitar:** retirar la actividad o exposición concreta, verificando efectos secundarios. **Reducir:** cambiar probabilidad/frecuencia o consecuencias y demostrarlo. **Compartir/transferir:** contrato/seguro/proveedor con límites, exclusiones y riesgo remanente; no transfiere automáticamente la responsabilidad ni el daño reputacional. **Aceptar:** decisión explícita de la autoridad, dentro de los criterios, con plazo y vigilancia; no marcar como aceptado un riesgo simplemente porque no hay presupuesto.

## Ejercicios y evaluación

El alumno recibe el caso R-001, detecta la diferencia entre reducción total e incremental, recalcula con coste alternativo, explica incertidumbre y propone dos evidencias para validar la eficacia. Después analiza R-002/R-003 y demuestra por qué no cabe reutilizar las mismas pérdidas ni porcentajes. Aprobación: cálculos coherentes con unidades y conclusiones proporcionales; ninguna eficacia de fabricante inventada.

**Salida profesional:** registro de riesgos, plan de tratamiento, informe de una página para dirección y anexos con datos/supuestos. GRC no termina en una matriz de colores: exige decisión, ejecución, comprobación y seguimiento.
