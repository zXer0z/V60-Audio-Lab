# Cómo se conectan las piezas

## 1. Kernel

[Kernel-DOP](https://github.com/zXer0z/Kernel-DOP) publica el árbol completo y su compilación. Los cambios relevantes son anunciar 352,8 kHz en ESS, añadir esa frecuencia al selector MI2S de LG sin cambiar sus índices anteriores, usar ESS como esclavo de reloj durante DoP y elegir X-tal para la placa exacta de referencia.

`patches/kernel/v60-dop-lab3.patch` es el diff de los seis archivos sobre la revisión QCloud fijada. Sirve para auditar/reconstruir los cambios, no para aplicarlo de nuevo sobre Kernel-DOP, que ya los contiene. Los ajustes de HiFi2 y DRE del driver recuperado son heredados de QCloud.

## 2. HAL ARM32

La receta transforma únicamente el HAL de hash conocido, en dos zonas de código ARM:

- Dirección virtual `0x3f638`, offset de archivo `0x3e638`, 36 bytes: el usecase DoP 82 acepta cierre (`0`), headset cableado (`4`) o auriculares cableados (`8`). Rechaza otros destinos por la salida existente de error antes de cambiar la ruta.
- Dirección virtual `0x6e584`, offset `0x6d584`, 52 bytes: para ese usecase conserva la frecuencia solicitada y fija el ancho de backend a 24 bits antes de actualizar la configuración.

El tamaño del archivo no cambia. Se sustituyen bloques de logging; fuera de DoP también se omiten esos mensajes de depuración. El parche no representa una auditoría de todas las demás rutas o llamadas internas de la HAL.

No se distribuye el binario: `scripts/generate.py` lo crea localmente a partir de la copia del usuario y verifica el resultado exacto.

## 3. Plataforma, mixer, política y DSP

- Los tres dispositivos DACDOP se redirigen de `TERT_TDM_RX_0` a `TERT_MI2S_RX`.
- Se añaden las rutas analógicas DACDOP ausentes a partir de los controles existentes de los perfiles ESS.
- El usecase DoP conecta `MultiMedia2` con MI2S y establece `KHZ_352P8` / `S24_LE` en la variante fija DSD128.
- La política DoP acepta `AUDIO_FORMAT_PCM_24_BIT_PACKED`.
- El perfil DSP DoP24 usa `app_type 69940`, ancho 24 y frecuencias de la familia DoP. Que aparezca 176,4 kHz en el perfil no convierte esta configuración fija de mixer en una variante DoP64 validada.

El parser de perfiles de esta ROM reconoce `AUDIO_OUTPUT_FLAG_PHONE` como nombre del bit `0x800000`, sin reconocer el nombre `AUDIO_OUTPUT_FLAG_DOP`. Se utiliza ese alias solo en el perfil privado; los flags de ejecución siguen siendo DIRECT|LG_DOP (`0x800001`). No se activa una llamada telefónica.

## 4. Orden de montaje

`reference/Dop24-overlay.rc` conserva la acción init usada en la imagen funcional. Los archivos se montan en las rutas exactas de vendor. La política se aplica en `load_persist_props_action`, después del overlay de Magisk y antes del inicio de las clases de servicios de audio, para que el módulo Bluetooth no reponga la política de 32 bits.

Es una **referencia histórica de integración**, no un módulo instalable. Requiere Magisk, `${MAGISKTMP}`, un busybox aportado localmente y los archivos generados colocados con los nombres de la acción. No se publica busybox ni se descarga automáticamente.

En los arranques observados fue necesario comprobar y restaurar las etiquetas SELinux vendor de los archivos montados después de iniciar Android. La acción init no garantiza por sí sola que sobrevivan a las fases posteriores del arranque. SELinux quedó Enforcing. Este repositorio no añade un mecanismo automático nuevo para esa corrección.

## 5. Ramdisk y boot

La imagen funcional se preparó conservando el DTB y las entradas originales del ramdisk del propio dispositivo, incluido Magisk, y añadiendo el overlay. El kernel se sustituyó por el `Image` compilado. Antes de instalar, se desempaquetó el resultado y se compararon kernel, DTB y entradas del ramdisk con los insumos esperados.

Puedes inspeccionar dos ramdisks locales newc ya descomprimidos:

```bash
python3 scripts/inspect-ramdisk.py original.cpio candidato.cpio
```

El informe compara contenido y metadatos, enumera adiciones y falla si faltan o cambian entradas originales. No certifica que las adiciones sean correctas ni que el boot arranque. No inspecciona por sí mismo todas las relaciones de hardlinks CPIO ni la imagen de arranque completa.

En el equipo de referencia se probaron primero arranques temporales. La imagen funcional se instaló permanentemente en el slot A el 2026-10-30, con respaldo conservado y hash de partición verificado. Esto no autoriza asumir el mismo slot en otro teléfono. No se incluyen comandos automáticos de flasheo.

## 6. Zero Music y LG Extended

Antes de abrir AudioTrack, el reproductor suspende su propio ajuste automático de ganancia y espera a que ESS y las salidas PCM estén en reposo. Solicita a LG Extended una reserva AUX temporal, sin sobrescribir la preferencia del usuario.

Protocolo 2 del proveedor `com.zxerox.lg_extended.dac`:

- `dop-begin`: root y token UUID; exige jack, Quad DAC encendido y ESS inactivo. Prepara AUX sin reiniciar un ESS activo.
- `dop-renew`: confirma propietario, conexión y perfil; renueva la reserva de 90 segundos.
- `dop-end`: se solicita después de liberar AudioTrack; permite restaurar la selección conservada cuando el DAC esté en reposo.

El reproductor renueva cada 20 segundos y detiene el transporte si pasan 60 segundos sin confirmación. La reserva se invalida tras reiniciar Android. Los callbacks normales de Edge posponen reaplicaciones durante la reserva, evitando reiniciar el ESS al comienzo de DoP.

La app envía reposo DSD mientras comprueba el portador físico configurado; solo entonces envía el archivo. Perder jack, flags/ruta o progreso detiene el transporte. El portador no se reconduce como audio PCM al altavoz o Bluetooth. No se aplican EQ, balance, ReplayGain, fades ni remuestreo de la app a los datos DSD; la política de foco pausa en lugar de atenuar estos datos.

Esta documentación describe las versiones fijadas de las aplicaciones; no incluye sus fuentes ni pretende reemplazarlas.
