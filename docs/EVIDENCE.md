# Evidencia y límites

## Resultado audible

El 2026-10-29, el usuario confirmó música limpia y continua al reproducir DSF DSD128 por la ruta adaptada hacia su amplificador. Después se integró en el reproductor. La confirmación de escucha no mide por sí sola qué transformaciones se producen en cada etapa.

## Comprobación digital

Se leyó una muestra del buffer de salida de un hilo activo de AudioFlinger, previo a la entrega a la HAL:

| Comprobación | Resultado |
| --- | --- |
| Tamaño de muestra | 11.520 bytes |
| Tramas estéreo PCM24 empaquetado | 1.920 |
| Marcadores `05/FA` válidos en ambos canales | 1.920/1.920 |
| Alternancias de marcador | 1.919/1.919 |
| Marcadores iguales entre canales | 1.920/1.920 |
| Payload DSD comparado con la fuente | 7.680 bytes |
| Bytes diferentes | **0** |
| SHA-256 del payload en ambas versiones | `87c523038b6c6e1558b5cc74672ce6d2bd15d51b660928e959df0ea579432536` |

Se deshizo únicamente el orden de bytes/bits del empaquetado para cotejar con el DSF LSB-first; no se convirtió DSD a PCM. Esto demuestra integridad de ese fragmento en ese punto. La muestra equivale aproximadamente a 5,44 ms del portador: no demuestra toda la canción ni las etapas posteriores.

No se publican los buffers ni fragmentos del archivo musical, las direcciones de memoria, identificadores del teléfono o dumps completos. Este documento registra el resultado del laboratorio, no sustituye una captura independiente reproducida por terceros.

## Configuración observada durante la sesión

- AudioFlinger: DIRECT|DOP (`0x800001`), 352.800 Hz, PCM24 empaquetado, volumen maestro 1 y canales a 0 dB.
- ALSA: estéreo `S24_3LE`, 352.800 Hz.
- MI2S: `KHZ_352P8`, `S24_LE`.
- HAL: confirmación DoP activa.
- ESS: HiFi, perfil AUX temporal.
- Registro 6: `0x4E`, bit 3 de habilitación DoP activo.
- Registro 10: `0x02`, reloj esclavo.
- Registro 64: `0x8D`, bloqueo de reloj y automute global inactivo.

**El registro 64 no es una bandera «DoP reconocido».** El valor observado del registro 72 (`0x0A`) tampoco se interpreta como confirmación de decodificación: no se dispone de una asignación pública inequívoca de ese código a DoP.

Referencias primarias: [estándar DoP 1.1](https://dsd-guide.com/sites/default/files/white-papers/DoP_openStandard_1v1.pdf) y [datasheet ESS ES9219 v1.3, registros 6, 64 y 72](https://www.esstech.com/wp-content/uploads/2026/03/ES9219-Datasheet-v1.3.pdf).

## Lo que falta medir o validar

- Captura eléctrica del enlace I²S o mecanismo documentado equivalente para verificar el último salto hasta el receptor.
- Integridad de la pista completa, no solo una muestra.
- Validación funcional completa de pausa/reanudación, búsqueda y continuidad prolongada de la última beta.
- PCM 384 kHz por el ESS y compatibilidad con otras ROM/revisiones.

El laboratorio tuvo otras variantes (DoP64, contenedor de 32 bits, otros perfiles y relojes). No se presentan como equivalentes a la variante final de DoP128/24 bits. La comparación de escucha entre 24 y 32 bits no aisló todas las variables; no demuestra que el contenedor de 32 bits fuera por sí solo la causa de los problemas.
