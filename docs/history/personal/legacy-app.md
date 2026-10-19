# Aplicación Next.js de referencia

La aplicación de `src/` es independiente del campus estático. Se conserva para no eliminar trabajo previo y dispone de su propia CI de instalación, lint, tipos, compatibilidad, build y auditoría.

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run lint
npm run typecheck
npm run test:dependencies
npm run build
```

La línea Node 22 requiere al menos 22.13.0 para el árbol de desarrollo revisado. La CI usa Node 22. Las dependencias efectivas y sus integridades están en `package-lock.json`; no regenerarlo indiscriminadamente.

La página de referencia conserva su texto original en inglés y su atributo `lang="en"`. Su tipografía utiliza fuentes del sistema: ya no descarga Geist mediante `next/font/google`. El campus y sus materiales permanecen en español.

Para probar el curso en Cloudflare Pages se publica `campus/dist`, no esta aplicación. No hay obligación de instalar Node o dependencias de Next.js para publicar el curso estático.
