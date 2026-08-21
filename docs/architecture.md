# Arquitectura

## MVP

El MVP separa cinco responsabilidades: canonización, hash, firma, modelo de evidencia y servicios de emisión/verificación/migración. La separación permite sustituir el firmante de desarrollo por implementaciones reales sin cambiar el formato general del registro.

## Flujo de emisión

1. Recibir bytes del documento.
2. Canonizar una envoltura determinista.
3. Calcular SHA3-512.
4. Formar el payload de firma con `record_id`, hash y política.
5. Crear firmas híbridas mediante adaptadores.
6. Persistir evidencia, claves públicas y auditoría.

## Flujo de verificación

Se verifica por separado la huella del contenido y cada firma disponible. El resultado no debe reducirse a una afirmación sin detalles: el consumidor debe saber si falló el contenido, la clave, la política o una firma concreta.

## Evolución

El siguiente paso es extraer persistencia y API en servicios independientes. La política criptográfica debe convertirse en configuración versionada, validada contra una lista permitida y revisada por seguridad.
