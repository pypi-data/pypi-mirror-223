import scipy.io.wavfile
import os
import re
import sounddevice as sd
import onnxruntime
import numpy as np
from huggingface_hub import snapshot_download
from gruut import sentences
import time

class TTS:
    def __init__(self, model_name: str, save_path: str = "./model", add_time_to_end: float = 0.8) -> None:
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        
        model_dir = os.path.join(save_path, model_name)
        
        if not os.path.exists(model_dir):
            snapshot_download(repo_id=model_name, 
                              allow_patterns=["*.txt", "*.onnx"], 
                              local_dir=model_dir,
                              local_dir_use_symlinks=False
                            )
        
        sess_options = onnxruntime.SessionOptions()
        self.model = onnxruntime.InferenceSession(os.path.join(model_dir, "exported/model.onnx"), sess_options=sess_options)
        
        with open(os.path.join(model_dir, "exported/vocab.txt"), "r", encoding="utf-8") as vocab_file:
            self.symbols = vocab_file.read().split("\n")
            self.symbols = list(map(chr, list(map(int, self.symbols))))
        
        self.symbol_to_id = {s: i for i, s in enumerate(self.symbols)}
        self.add_time_to_end = add_time_to_end

        
    def _ru_phonems(self, text: str) -> str:
        text = text.lower()
        phonemes = ""
        for sent in sentences(text, lang="ru"):
            for word in sent:
                if word.phonemes:
                    phonemes += "".join(word.phonemes)
        phonemes = re.sub(re.compile(r'\s+'), ' ', phonemes).lstrip().rstrip()
        return phonemes
    
    
    def _text_to_sequence(self, text: str) -> list[int]:
        '''convert text to seq'''
        sequence = []
        clean_text = self._ru_phonems(text)
        for symbol in clean_text:
            symbol_id = self.symbol_to_id[symbol]
            sequence += [symbol_id]
        return sequence
    
    
    def _intersperse(self, lst, item):
        result = [item] * (len(lst) * 2 + 1)
        result[1::2] = lst
        return result
    
    
    def _get_text(self, text: str) -> list[int]:
        text_norm = self._text_to_sequence(text)
        text_norm = self._intersperse(text_norm, 0)
        return text_norm
    
    def _add_silent(self, audio, silence_duration: float = 1.0, sample_rate: int = 22050):
        num_samples_silence = int(sample_rate * silence_duration)
        silence_array = np.zeros(num_samples_silence, dtype=np.float32)
        audio_with_silence = np.concatenate((audio, silence_array), axis=0)
        return audio_with_silence
    
    def save_wav(self, audio, path:str):
        '''save audio to wav'''
        scipy.io.wavfile.write(path, 22050, audio)
    
    
    def play_audio(self, audio):
        sd.play(audio, 22050, blocking=True)
        # sd.play(audio, 22050)
        # time.sleep(
        #     (len(audio)/22050) 
        #     +
        #     self.add_time_to_end
        #     )
    
    
    def __call__(self, text: str, play = False):
        phoneme_ids = self._get_text(text)
        text = np.expand_dims(np.array(phoneme_ids, dtype=np.int64), 0)
        text_lengths = np.array([text.shape[1]], dtype=np.int64)
        scales = np.array(
            [0.667, 1, 0.8],
            dtype=np.float32,
        )
        audio = self.model.run(
            None,
            {
                "input": text,
                "input_lengths": text_lengths,
                "scales": scales,
                "sid": None,
            },
        )[0][0,0][0]
        audio = self._add_silent(audio)
        if play:
            self.play_audio(audio)
        return audio