# 09 · Fuentes primarias y límites de la referencia

[Índice](README.md) · Fecha de revisión documental: **18 de septiembre de 2026**.

## Cómo interpretar las fuentes

Las fuentes siguientes se han utilizado para contrastar conceptos, alcance de marcos y ejemplos de capacidades. El diseño curricular, los escenarios, las rúbricas, las matrices parciales y todos los números del ejemplo de riesgos son elaboración didáctica, no texto oficial ni una validación de producto.

Consultar una página no equivale a haber ejecutado una herramienta, desplegado una imagen, leído una norma de pago completa o auditado un sistema. Las referencias de fabricantes apoyan la existencia y modalidad de su oferta; no demuestran eficacia comparativa, cobertura de un plan concreto o adecuación a toda organización.

## Registro

| ID | Fuente y enlace primario | Uso y límite |
|---|---|---|
| S01 | NIST: [Cybersecurity Framework](https://www.nist.gov/cyberframework) y [FAQ](https://www.nist.gov/cyberframework/faqs) | CSF 2.0, funciones, Core, perfiles y Tiers. Las paráfrasis docentes no sustituyen el texto oficial. |
| S02 | NIST: [Informative References](https://www.nist.gov/cyberframework/informative-references) | Correspondencias, OLIR, autoría y límites de las referencias de terceros. |
| S03 | NIST: [SP 800-30 Rev. 1](https://csrc.nist.gov/pubs/sp/800/30/r1/final) | Guía de evaluación de riesgos. El ejemplo numérico del curso no es una fórmula obligatoria de NIST. |
| S04 | NIST: [SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Respuesta a incidentes integrada con gestión del riesgo. |
| S05 | ISO: [ISO/IEC 27001](https://www.iso.org/standard/27001) | Ficha pública de ISO/IEC 27001:2022. No se ha reproducido ni analizado íntegramente una copia licenciada. |
| S06 | ISO: [ISO/IEC 27005:2022](https://www.iso.org/es/contents/data/standard/08/05/80585.html) | Ficha pública y alcance de guía de riesgos de seguridad de información; no lectura completa de la norma de pago. |
| S07 | EUR-Lex: [Reglamento (UE) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj?locale=es) | RGPD: seguridad, responsabilidad, tratamientos, derechos, EIPD, brechas y transferencias según aplicabilidad. |
| S08 | BOE: [Real Decreto 311/2022, ENS](https://www.boe.es/eli/es/rd/2022/05/03/311) | Ámbito, responsables, riesgos, categorización, medidas y aplicabilidad. Revisar texto vigente y requisitos específicos antes de una evaluación real. |
| S09 | AEPD: [presentación de la guía de gestión del riesgo y evaluación de impacto](https://www.aepd.es/la-agencia/agenda/presentacion-de-la-guia-de-gestion-del-riesgo-y-evaluacion-de-impacto-en) | Distinción de riesgo para personas y enfoque EIPD. Se ha consultado la página de presentación, no se afirma lectura integral del PDF de la guía. |
| S10 | CCN: [PILAR](https://pilar.ccn-cert.cni.es/pilar/) | Relación con análisis de riesgos MAGERIT, activos y salvaguardas. Revisar modalidad y licencia antes de exigir instalación. |
| S11 | AWS: [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) | Revisión arquitectónica por propiedades y responsabilidades; no prescripción de un patrón único. |
| S12 | Microsoft: [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/) | Principios y revisión de cargas Azure; ejemplos de servicios requieren validar requisitos. |
| S13 | Google Cloud: [Well-Architected Framework](https://cloud.google.com/architecture/framework) | Arquitectura de cargas cloud y decisiones de calidad. |
| S14 | Docker: [Compose](https://docs.docker.com/compose/) | Modelo y operación de aplicaciones de varios contenedores. |
| S15 | Docker: [Swarm mode](https://docs.docker.com/engine/swarm/) | Servicios, clúster y operación; comprobar publicación de puertos según configuración. |
| S16 | Kubernetes: [conceptos y descripción general](https://kubernetes.io/docs/concepts/overview/) | Modelos y recursos; no acredita una configuración segura del clúster. |
| S17 | Proxmox: [Virtual Environment, características](https://www.proxmox.com/en/products/proxmox-virtual-environment/features) | KVM/LXC e infraestructura; no se fija versión o arquitectura de hardware sin validación del laboratorio. |
| S18 | Kali: [documentación](https://www.kali.org/docs/) | Distribución y estación de herramientas; no equivale a autorización o metodología. |
| S19 | Proyecto: [DVWA, README oficial](https://github.com/digininja/DVWA) | Aplicación de formación controlada y advertencia de no exposición pública. Consultado mediante el conector GitHub. |
| S20 | OWASP: [Juice Shop](https://owasp.org/projects/juice-shop), [guía de formación](https://devguide.owasp.org/en/07-training-education/01-vulnerable-apps/01-juice-shop/) y [anuncio de versión 20](https://owasp.org/blog/2026/05/13/juice-shop-v20.html) | Plataforma didáctica; hay documentación con fechas/versiones diferentes, por lo que se fijará un release concreto al probar el laboratorio. |
| S21 | Cloudflare: [WAF](https://developers.cloudflare.com/waf/) | Capacidad y componentes del WAF; disponibilidad depende de plan y configuración. |
| S22 | Akamai: [App & API Protector](https://www.akamai.com/products/app-and-api-protector) | Ejemplo de oferta comercial web/API, sin recomendación ni comparación de eficacia. |
| S23 | Imperva: [Web Application Firewall](https://www.imperva.com/products/web-application-firewall-waf/) | Ejemplo cloud/centro de datos; comprobar modalidades y oferta vigente antes de selección. |
| S24 | Fortinet: [FortiWeb](https://www.fortinet.com/products/web-application-firewall/fortiweb) | Ejemplo de WAF con modalidades appliance/virtuales; no se extrapolan capacidades a todas las ediciones. |
| S25 | OWASP: [Core Rule Set](https://coreruleset.org/) | Proyecto de reglas para motores compatibles; reglas y motor son componentes distintos. |
| S26 | Zeek: [documentación](https://docs.zeek.org/en/current/) | Observación de red y logs; fijar versión/LTS aplicable al laboratorio. |
| S27 | Suricata: [documentación](https://docs.suricata.io/en/latest/) | Detección/prevención según despliegue. La rama latest consultada puede describir desarrollo: no se presenta como versión estable instalada. |
| S28 | MISP: [proyecto oficial](https://www.misp-project.org/) | Gestión e intercambio de inteligencia e indicadores. |
| S29 | OpenCTI: [documentación](https://docs.opencti.io/latest/) | Modelo y gestión de conocimiento CTI. |
| S30 | Microsoft: [Sentinel overview](https://learn.microsoft.com/en-us/azure/sentinel/overview) | Ejemplo de SIEM y capacidades asociadas; revisar licencias y plataforma de acceso. |
| S31 | Microsoft: [Defender for Endpoint](https://learn.microsoft.com/en-us/defender-endpoint/microsoft-defender-endpoint) | Ejemplo de protección/detección de endpoint según plan y sistema. |
| S32 | ENISA: [ECSF role profiles](https://www.enisa.europa.eu/publications/european-cybersecurity-skills-framework-role-profiles) | Competencias y perfiles de referencia; el catálogo docente no acredita un rol oficial. |
| S33 | W3C: [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Criterios de accesibilidad y objetivo de validación de la interfaz. |
| S34 | Cloudflare: [Static HTML en Pages](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) | Publicación de activos estáticos; se distingue de Workers y del backend opcional. |

## Referencias de ampliación que requieren revisión específica antes de impartir

Manual de la versión instalada de Bash/zsh/CMD/PowerShell; documentación de la distribución Linux y de Apple Platform Security; WordPress y plugins concretos; VirtualBox y componentes adicionales; VMware por producto; ISO 31000; FAIR; EBIOS RM; serie NIST 8286; NICE; MITRE ATT&CK y los formatos STIX/TAXII; normas o requisitos sectoriales adicionales. Su inclusión como tema de estudio **no afirma que se haya comprobado aquí cada versión, licencia o detalle normativo**.

Las búsquedas de manuales completos de algunos hipervisores y herramientas no proporcionaron una lectura íntegra utilizable. Por eso esta referencia no fija sus precios, derechos de distribución, límites exactos o comandos dependientes de versión. Al desarrollar el laboratorio se debe volver a la documentación primaria y registrar ese contraste.

## Correcciones de interpretación que deben mantenerse

- CSF describe resultados y facilita priorización; no certifica por sí solo cumplimiento.
- Las matrices del curso son relaciones parciales elaboradas para enseñar; no se ofrecen como correspondencias normativas oficiales.
- Los códigos ISO concretos deberán verificarse con texto autorizado o referencia informativa identificada; no inventarlos para completar una tabla.
- ENS y RGPD exigen determinar ámbito y condiciones. No toda organización, tratamiento o incidente recibe las mismas medidas o decisiones.
- Las cifras de riesgo son sintéticas; los extremos de sensibilidad no son intervalos estadísticos.
- Los catálogos comerciales no validan eficacia ni funcionalidad de cualquier plan contratado.
- La aplicación vulnerable y su laboratorio no se publican con el campus.
- Documento traducido, laboratorio probado, curso impartido y sistema desplegado son estados diferentes.

## Mantenimiento y trazabilidad

Antes de cada cohorte: anotar sistema/edición/versión/arquitectura, procedencia, licencia, fuente, fecha consultada, comandos o funciones relevantes, cambios, prueba, resultado y revisor. Revisar soporte y avisos pertinentes. Utilizar versiones reproducibles sin confundir fijación de versión con autorización para mantener software sin soporte.

Conservar un registro de cambios del plan y del contenido. Una fuente puede cambiar sin que lo haga el curso: identificar la discrepancia y corregirla antes de evaluar. La publicación de nuevos contenidos debe incluir revisión humana técnica y lingüística, además de comprobaciones automáticas de estructura.
