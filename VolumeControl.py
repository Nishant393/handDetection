import sys

if sys.platform == "win32":
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    class VolumeControl:
        def __init__(self):
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = interface.QueryInterface(IAudioEndpointVolume)

        def get_mute(self):
            return self.volume.GetMute()

        def get_volume(self):
            return self.volume.GetMasterVolumeLevel()

        def get_volume_range(self):
            return self.volume.GetVolumeRange()

        def set_volume(self, level):
            self.volume.SetMasterVolumeLevel(level, None)

elif sys.platform == "linux":
    import os
    try:
        import alsaaudio  # Try ALSA first
        alsa_available = True
    except ImportError:
        alsa_available = False

    class VolumeControl:
        def __init__(self):
            if alsa_available:
                self.mixer = alsaaudio.Mixer()
            else:
                self.mixer = None  # Fallback to pactl if ALSA is unavailable

        def get_mute(self):
            if alsa_available:
                return self.mixer.getmute()[0]
            return os.popen("pactl get-sink-mute @DEFAULT_SINK@").read().strip().endswith("yes")

        def get_volume(self):
            if alsa_available:
                return self.mixer.getvolume()[0]
            return int(os.popen("pactl get-sink-volume @DEFAULT_SINK@").read().split("/")[1].strip().replace("%", ""))

        def get_volume_range(self):
            return (0, 100)  # PulseAudio/ALSA range

        def set_volume(self, level):
            level = max(0, min(100, level))  # Ensure range 0-100
            if alsa_available:
                self.mixer.setvolume(level)
            else:
                os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {level}%")


