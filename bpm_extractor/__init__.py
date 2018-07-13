from conf import *
from pydub import AudioSegment
from aubio import tempo, source
from numpy import diff, median

__author__ = "Ori Roza"


class BMPExtractor(object):
    """
    Using Aubio example of retrieving BPM of an audio
    """
    WIN_S = 512  # fft size
    HOP_S = WIN_S // 2  # hop size

    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.audio_file_wav = self.audio_file.split(MP3_AUDIO_EXT)[0]
        self._convert_to_wav()
        self.s = source(self.audio_file_wav + WAV_AUDIO_EXT, 0, self.HOP_S)
        self.o = tempo("default", self.WIN_S, self.HOP_S, self.s.samplerate)
        self._beats = []

    def _convert_to_wav(self):
        sound = AudioSegment.from_mp3(self.audio_file)
        sound.export(self.audio_file_wav + WAV_AUDIO_EXT, format=WAV_AUDIO_EXT[1:])

    def _get_beats(self):
        # total number of frames read
        total_frames = 0
        while True:
            samples, read = self.s()
            is_beat = self.o(samples)
            if is_beat:
                this_beat = self.o.get_last_s()
                self._beats.append(this_beat)
            total_frames += read
            if read < self.HOP_S: break

    def get_bpm_samples(self):
        self._get_beats()
        return 60. / diff(self._beats)

    def get_song_stats(self, samples):
        """
        Returns:
            * BPM average
            * High BPM values percentage of an audio samples
            * Amount of high BPM values sequence (more than 5 in sequence)
        """
        high_bpm_counter = 0
        seq_counter = 0
        high_bpm_sequence = 0
        chosen_samples = samples[: SAMPLES_QUANTITY]  # last X samples
        chosen_samples = [sample-5 for sample in chosen_samples]  # Reducing the values (to be more accurate)
        bpm_avg = median(chosen_samples)
        chosen_length = len(chosen_samples)
        for i in xrange(chosen_length):
            if chosen_samples[i] > HIGH_BPM_THRESHOLD:
                high_bpm_counter += 1
                seq_counter += 1
                if seq_counter > 5:
                    high_bpm_sequence += 1
            else:
                seq_counter = 0

        self.delete_wav()
        return (high_bpm_counter * 100) / chosen_length, int(round(bpm_avg)), high_bpm_sequence

    def delete_wav(self):
        try:
            os.remove(self.audio_file_wav+WAV_AUDIO_EXT)
        except Exception as e:
            print e