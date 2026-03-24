import os

def get_audio_files(dataset_path):
    """
    This function scans the L2_ARCTIC dataset folder
    and returns a list of all .wav audio file paths.
    """
    audio_files = []

    if not os.path.exists(dataset_path):
        return audio_files

    for speaker in os.listdir(dataset_path):
        speaker_path = os.path.join(dataset_path, speaker)
        wav_path = os.path.join(speaker_path, "wav")

        if os.path.isdir(wav_path):
            for file in os.listdir(wav_path):
                if file.lower().endswith(".wav"):
                    audio_files.append(os.path.join(wav_path, file))

    return audio_files