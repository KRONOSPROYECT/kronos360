# Seguridad

- `DemoSigner` existe únicamente para probar el flujo local y no es una firma digital de producción.
- No desarrollar criptografía propia.
- Integrar ML-DSA y el algoritmo clásico mediante bibliotecas mantenidas y revisadas.
- Usar HSM/KMS para claves de producción cuando el nivel de riesgo lo exija.
- Aplicar mínimo privilegio, rotación, revocación y separación de entornos.
- Registrar eventos sin secretos.
- No afirmar que el sistema es indestructible o legalmente válido por sí mismo.

## Revisión antes de producción

- Evaluación de amenazas.
- Revisión de dependencias y CVE.
- Pruebas de interoperabilidad.
- Pruebas de carga.
- Simulacro de compromiso de claves.
- Revisión legal y de cumplimiento.
- Auditoría independiente.
