# Documentos históricos del repositorio personal

Estos tres documentos se conservan **sin modificar sus bytes**, desde la versión pública de `WiktorNykiel/fundamentos-ciberseguridad` indicada en cada enlace. Forman parte del registro de decisiones y revisiones de septiembre de 2026. No son instrucciones vigentes de despliegue ni evidencia de nuevas pruebas del campus.

La [matriz de migración del 19 de octubre](../../maintenance/2026-10-19-migracion-repositorios.md) explica su incorporación y las decisiones sobre la aplicación de referencia, el campus actual y Awesome DPD. El manifiesto asociado conserva sus hashes SHA-256 y todas las versiones históricas identificadas.

| Documento conservado | Path original y fuente pública | Blob original | SHA-256 de la copia |
|---|---|---|---|
| [legacy-app.md](legacy-app.md) | [`docs/legacy-app.md`](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/6d9bcec26614a47857808072cb3b08614a5c04bd/docs/legacy-app.md) | `550ff16261c20fcb2c0b1e096d258b8793d5082d` | `4933003a9da7b4b15bf93fa96464313ae187a731025227b2dbdcaf826977751c` |
| [2026-09-15-integration.md](2026-09-15-integration.md) | [`docs/maintenance/2026-09-15-integration.md`](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/6d9bcec26614a47857808072cb3b08614a5c04bd/docs/maintenance/2026-09-15-integration.md) | `d745d1915167a9728becf02d5493bf8b17e2ca1a` | `217ee929438477411b7cb1e36b53960f02336c9fe9361fc5483913066e969c8b` |
| [2026-09-18-review.md](2026-09-18-review.md) | [`docs/review-20260918.md`](https://github.com/WiktorNykiel/fundamentos-ciberseguridad/blob/6d9bcec26614a47857808072cb3b08614a5c04bd/docs/review-20260918.md) | `ac3cc7774e5c472519023c65308ffc58fa402199` | `04742257a5d18f85c690372142d52a12e1de1b679440dc3fd9689befd10fe1b4` |

## Cómo interpretar estas referencias

`legacy-app.md` describe la aplicación Next de referencia. Sus dependencias y comandos permanecen asociados al historial personal; no se incorporan a las dependencias del runtime estático del campus.

El informe del 15 de septiembre y la revisión del 18 de septiembre registran la integración y comprobaciones de aquellas versiones. Sus números de PR corresponden al repositorio personal; no deben interpretarse como los PR de igual número del repositorio de la organización. Las cifras de pruebas, versiones y capturas mencionadas conservan su fecha original.

Para operar la versión actual, consultar [revisión y publicación](../../engineering/REVIEW-AND-RELEASE.md) y el [procedimiento de Cloudflare](../../../campus/DEPLOY-CLOUDFLARE.md). El estado de publicación y los pendientes de migración se consultan en la matriz de octubre.

## Atribución

Se conserva la autoría y atribución del origen, incluida la de Wiktor Nykiel, así como las referencias de terceros. Esta copia documental no asigna una licencia nueva ni convierte la visibilidad pública del repositorio en una ampliación de derechos de uso.
