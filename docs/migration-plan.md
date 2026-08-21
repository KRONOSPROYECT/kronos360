# Plan de migración

1. Inventariar algoritmos, claves, certificados, bibliotecas y dependencias.
2. Definir canonización y vectores de prueba.
3. Mantener lectura de registros históricos.
4. Emitir nuevos registros con firma híbrida.
5. Crear evidencias de migración para históricos prioritarios.
6. Rotar y revocar claves con trazabilidad.
7. Retirar la creación con algoritmos obsoletos cuando exista cobertura suficiente.

Las migraciones no sobrescriben el hash o la firma histórica. Una migración crea un nuevo evento que referencia el registro original y registra la fecha real de migración.

## Criterios de salida

- Verificación reproducible entre entornos.
- Cero claves privadas en repositorio o logs.
- Backups restaurables.
- Pruebas positivas y negativas aprobadas.
- Revisión independiente antes de producción.
