# Problemas conocidos

## Se solicita 384 kHz y Android termina en 48 kHz

La frecuencia solicitada por la app no acredita la configuración del backend. Compara el hilo activo de AudioFlinger, ALSA y MI2S durante la reproducción. El camino PCM 384 kHz del ESS sigue sin validar. DoP128 usa 352,8 kHz; no necesita 384 kHz.

## Quad DAC encendido: audio entrecortado

En la placa de referencia, la selección MCLK de respaldo perdía sincronización. El cambio a X-tal resolvió el síntoma observado y quedó limitado al modelo DT exacto `Timelm_lao rev_1.01`. No fuerces ese ajuste en otras placas sin investigar su reloj.

## AUX funciona pero Normal/Alta producen siseo al iniciar DoP

Se observó que LG Extended reaplicaba la selección a los 300/1.200 ms tras iniciar reproducción y podía reiniciar el ESS. Se resolvió coordinando una reserva AUX temporal antes de abrir el portador, conservando la preferencia para después.

Que las tres preferencias funcionen con esta coordinación no demuestra tres perfiles físicos DoP: durante la sesión se utiliza AUX temporal. No cambies el modo físico del DAC en caliente para investigar este fallo.

## El laboratorio dice «enviado», pero no oigo música

Escribir tramas no prueba decodificación del receptor. Comprueba la ruta y un fragmento que realmente contenga música: un inicio silencioso confundió parte del diagnóstico original. Ante ruido inesperado, detén la reproducción y baja/apaga el amplificador antes de repetir cambios de ruta. Los primeros patrones del laboratorio se enviaron con el amplificador apagado.

## La política vuelve a 32 bits al reiniciar

El overlay Bluetooth de Magisk podía reponer su XML después del montaje temprano. La acción de referencia aplica la política DoP24 en `load_persist_props_action`. Revisa el archivo que Android carga de verdad y su hash; no solo la copia preparada en almacenamiento temporal.

## Etiquetas SELinux de los archivos montados

En el montaje de referencia, los archivos podían terminar con `system_file` tras arrancar. Se comprobaron y restauraron las etiquetas `vendor_file` para la HAL y `vendor_configs_file` para XML/conf, manteniendo Enforcing. No se publica una solución persistente nueva para ese comportamiento. No desactives SELinux para ocultar errores de montaje o compatibilidad.

## No inicia Android tras cambiar el boot

Recupera el boot original del propio dispositivo desde el bootloader/recovery disponible. El slot y el ramdisk deben corresponder a la instalación real. En el equipo de referencia también existió un fallo de caché de paquetes de la ROM; se conservó esa caché aparte antes de reiniciar. No se debe atribuir automáticamente un bloqueo al mismo fallo en otro dispositivo, ni borrar datos del usuario como procedimiento genérico.

No se incluyen respaldos del teléfono ni comandos automáticos de recuperación. No desbloquees o vuelvas a bloquear el bootloader como parte de estas recetas.

## Capturar estado sin cambiar la reproducción

Después de iniciar tú mismo la reproducción, puedes ejecutar `scripts/capture-state.sh` desde una shell root de Android y guardar su salida localmente. El script consulta estado; no abre archivos musicales, no cambia rutas/volumen y no reinicia servicios. El resultado puede contener nombres o datos privados en dumps de AudioFlinger: no lo publiques sin revisar. `captures/` queda fuera de Git.
