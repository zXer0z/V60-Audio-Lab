#!/system/bin/sh
# SPDX-License-Identifier: GPL-2.0-only
# Read-only snapshot. User starts/stops playback. No gain, routing or volume writes.
set -u
[ "$(id -u)" = 0 ] || { echo 'Run this snapshot from a root shell.' >&2; exit 1; }
echo '=== DEVICE ==='
getprop ro.product.device
getprop ro.build.version.release
getprop ro.boot.slot_suffix
uname -r
getenforce
echo '=== ALSA ==='
cat /proc/asound/card0/pcm1p/sub0/hw_params 2>/dev/null
echo '=== MIXER ==='
for control in 'TERT_MI2S_RX SampleRate' 'TERT_MI2S_RX Format' 'Es9018 State' 'Es9018 HEADSET TYPE' 'Es9018 Dop'; do
    tinymix "$control" 2>/dev/null
done
echo '=== ESS REGISTERS (ACTIVE ONLY) ==='
state=$(tinymix 'Es9018 State' 2>/dev/null)
case "$state" in
    *'>Hifi'*) grep -E '<#(01|06|10|64|72)>=' /sys/bus/i2c/devices/3-0048/registers 2>/dev/null ;;
    *) echo 'ESS not HiFi; registers were not queried.' ;;
esac
echo '=== EDGE ==='
content call --uri content://com.zxerox.lg_extended.dac --method state 2>&1
echo '=== PLAYER BRIDGE ==='
content call --uri content://local.v60.player.bluetooth.root --method audio-status 2>&1
echo '=== AUDIO FILE HASHES ==='
sha256sum /vendor/lib/hw/audio.primary.kona.so /vendor/etc/audio_io_policy.conf \
    /vendor/etc/mixer_paths.xml /vendor/etc/audio/audio_policy_configuration.xml \
    /vendor/etc/audio_platform_info_intcodec.xml 2>/dev/null
echo '=== AUDIOFLINGER ==='
dumpsys media.audio_flinger
