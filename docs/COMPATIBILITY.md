# Compatibilidad de referencia

La receta es una transformación exacta de archivos conocidos. No detecta ni adapta automáticamente otra ROM.

| Componente | Referencia |
| --- | --- |
| Dispositivo | LG V60, `timelm` |
| Modelo DT | `LG Electronics, Timelm_lao, rev_1.01` |
| Android | 13 |
| Fingerprint de ROM | `lge/timelm/timelm:13/TKQ1.220829.002/2326319175c92:user/release-keys` |
| Kernel | `4.19.325-v60-dop-lab3+` |
| Base QCloud | `78253129915f211b0f4e8c86bea09c50111f3b4d` / `thunder-1.3-new` |
| Driver ESS recuperado | `4e55e8eca6beb81f2eab88617d6e496c0f2be4c1` / `thunder-1.3` |
| Publicación Kernel-DOP | `641fc13707225429d65748c448a24bbc3cef9c39` |
| Root del equipo de referencia | Magisk 30.7, conservado en su ramdisk |
| Zero Music | `1.0.8-beta14` / 143 |
| LG Extended | `1.1.0-beta3` / 4 |
| Protocolo de reserva AUX | 2 |
| Fuente final validada | DSF DSD128 estéreo |
| Transporte | DoP128, PCM24 empaquetado, 352.800 Hz |
| Destino | Quad DAC interno → jack analógico |

No se publica un boot porque incluye elementos específicos del teléfono y su instalación de root. Una imagen basada en otro ramdisk puede perder Magisk, no arrancar o alterar módulos aunque el kernel compile.

## Entradas de la receta

Los seis archivos son aportados por el usuario. Nombres locales:

```text
inputs/audio.primary.kona.so
inputs/audio_platform_info.xml
inputs/audio_platform_info_intcodec.xml
inputs/mixer_paths.xml
inputs/audio_io_policy.conf
inputs/audio_policy_configuration.xml
```

La receta contiene los tamaños, hashes de entrada/salida y rutas Android correspondientes. El HAL esperado es ARM32, no el archivo del directorio `lib64`. La política esperada procede del archivo activo anterior a las modificaciones del laboratorio; no debe confundirse con otro XML de igual nombre que Android no estuviera cargando.

Las ediciones de texto se aplican sobre una representación LF y después se restaura el estilo de saltos de línea exacto de cada salida. La receta registra este paso porque forma parte del hash final. El diff `audio_policy_configuration.xml.semantic.patch` normaliza el formato XML solo para revisión humana: no se aplica directamente al original. La receta JSON es la fuente de las transformaciones exactas.

La receta de política genera también los cambios de la ruta PCM DIRECT Bluetooth de 96 kHz que coexistía en el equipo de referencia. No significa que DoP se transporte por Bluetooth, ni que todo dispositivo Bluetooth acepte esa ruta. El resto de archivos se genera para la variante final DoP24.

## Hashes finales principales

| Archivo | SHA-256 |
| --- | --- |
| HAL ARM32 | `b94f8238337ca4286b579884489711f588f1b8116888e80bc5f9ccaf6ef5cca6` |
| Perfiles DSP | `53851509e76c1d09965f2ff6c5f65dbeb5242b589996a32bdc72d0bf0f05a6d8` |
| Mixer | `2bcb89bbdff1166d347a1a337904c9a14330bace7b00cc771e94187ecb15be2f` |
| Política activa | `ef3169d6eb6d931ebd5c22cb341c60eac967876392fb4e5859de638fc606abec` |
| Plataforma intcodec | `8f4b3f600d3b06f652b116cf486ccdda654b150b9077530182d466b45e864b39` |

El esquema de receta registra el hash de la plataforma adicional. Comprobar hashes es una condición de compatibilidad, no una prueba de audio.
