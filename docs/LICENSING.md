# Licencias y procedencia

## Material propio del laboratorio

Los scripts y la documentación originales de este repositorio se aportan bajo **GNU General Public License versión 2 únicamente (GPL-2.0-only)**. El texto completo está en `LICENSE`. No se ofrece garantía.

## Kernel y cambios derivados

Los parches del kernel derivan del árbol QCloud basado en Linux 4.19.325. Conservan los términos de sus fuentes; esta publicación no los convierte en código MIT ni se atribuye su autoría original.

- Origen: https://github.com/aqbaloch6205/LGV60_Timelm_Qcloud_Kernel
- Base: `78253129915f211b0f4e8c86bea09c50111f3b4d`, rama `thunder-1.3-new`.
- Driver ESS recuperado: `4e55e8eca6beb81f2eab88617d6e496c0f2be4c1`, rama `thunder-1.3`.
- Árbol modificado completo, avisos y licencias por archivo: https://github.com/zXer0z/Kernel-DOP

El kernel es GPL v2 únicamente, con la excepción de llamadas al sistema descrita en su `COPYING` y `LICENSES/exceptions/Linux-syscall-note`. Los archivos individuales conservan sus términos, incluidas licencias duales existentes. La excepción no es una autorización general para redistribuir software propietario.

Créditos: contribuidores de Linux, Qualcomm, LG, ESS Technology, QCloud y sus proyectos de origen. Los ajustes heredados de HiFi2/DRE del driver recuperado no son desarrollos originales de este laboratorio.

## Configuraciones de vendor y recetas

Los diffs de XML/conf contienen extractos de las configuraciones de referencia, no copias completas. Los archivos originales y los resultados generados conservan sus avisos y licencias de origen; el `LICENSE` del laboratorio no sustituye esos términos. La receta registra los cambios exactos y hashes para aportar y generar los archivos localmente.

No se redistribuye ningún HAL completo. Los cambios de código ARM están representados como ediciones acotadas sobre un hash concreto. El usuario debe obtener legítimamente su propia copia y revisar los términos aplicables a cualquier distribución posterior. Tampoco se publica música, firmware empaquetado, ramdisk con Magisk ni claves.

## Documentos externos

Se enlazan el estándar DoP y la ficha ESS como referencias técnicas. No se copian esos documentos dentro del repositorio ni se les aplica la licencia del laboratorio.

Referencia sobre las licencias del kernel: https://www.kernel.org/doc/html/latest/process/license-rules.html
