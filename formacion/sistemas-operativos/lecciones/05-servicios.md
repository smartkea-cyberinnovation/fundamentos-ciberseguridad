# 05 · Operar un servicio: del host al resultado útil

## Cuatro afirmaciones diferentes

“Existe un proceso”, “hay un puerto escuchando”, “el cliente se conecta” y “la aplicación funciona” no significan lo mismo. Para demostrar cada una necesitas observaciones distintas. El servicio docente permite verlo: una respuesta 200 en `/healthz` no demuestra que otro servidor TLS, un directorio empresarial o un backend externo esté operativo.

Propón una hipótesis antes de probar. Un fallo de nombre apunta a resolución; un rechazo de conexión puede indicar listener ausente; un timeout puede involucrar ruta o filtrado; un error HTTP puede proceder de aplicación. No existe una única interpretación universal de cada síntoma: combina datos y acota destino e intervalo.

## Administración remota

Una sesión requiere autenticación de servidor, identidad del cliente, autorización y transporte apropiado. No aceptar un cambio de identidad de host sin contraste. Las claves de SSH no deben copiarse entre alumnos ni guardarse en Git. WinRM y SSH tienen requisitos distintos; un endpoint restringido puede rechazar correctamente acciones fuera de su función. [S05, S08](../FUENTES.md)

Un bastión es parte de un diseño de acceso, no un permiso para llegar a cualquier segmento. Estudia los saltos mediante un diagrama con origen, destino, identidad, protocolo, finalidad y registro. Los ejercicios de tránsito no autorizado se analizan con diagramas y telemetría preparada, sin establecer cadenas de intrusión.

## Transferir no es preservar todo

Para copiar un conjunto de datos, define qué propiedades importan: contenido, tamaño, nombre, timestamps, propietario y permisos. Calcula y compara manifiestos, pero registra lo que el protocolo y el filesystem no preservan. Verificar SHA-256 de cada archivo no demuestra por sí solo continuidad de custodia ni equivalencia de ACL.

## Web, HTTP y TLS

`kit/web.py` contiene una página clara y un endpoint de estado. No sirve el directorio del proyecto, no interpreta entrada como código y no almacena datos de usuarios. Usa el navegador y una consulta CLI al mismo servidor local, compara cabeceras, estado, cuerpo y log. Consulta una ruta inexistente para distinguir fallo HTTP de ausencia de conectividad.

El ejemplo usa HTTP en loopback: no finge tener TLS. Para aprender TLS, el docente añade en otro laboratorio un servidor apropiado y una CA de prueba controlada. Se evalúan nombre, cadena, fechas y confianza; desactivar validación del cliente no es una corrección. `http.server` no se utiliza como servidor de producción. [S17]

## Compose y Swarm

Compose permite levantar el ejemplo en un host de laboratorio con puerto ligado a loopback. El contenedor usa usuario no privilegiado, filesystem de solo lectura y recursos limitados. No se le entrega el socket de Docker ni carpetas personales.

Swarm consume una imagen ya distribuida y tiene semántica distinta de despliegue/publicación. Su fichero se mantiene separado, sin puertos publicados. La red overlay debe ser accesible solo para los participantes autorizados. Docker documenta que `docker stack deploy` utiliza el formato Compose legado de versión 3; no toda función de la especificación Compose actual se traslada automáticamente. [S09]

Comprueba la configuración y después el estado efectivo. Los YAML revisados no equivalen a un despliegue ejecutado. Continúa con [R06](../practicas/R06-web.md), registrando qué parte has podido probar realmente.
