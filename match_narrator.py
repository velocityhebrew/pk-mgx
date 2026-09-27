import os
import asyncio
import edge_tts
import soundfile as sf

VOICES = {
    "Red": "en-US-GuyNeural",           # Trainer Red / AI Strategist - Clear, energetic, tactical
    "Blue": "en-US-ChristopherNeural"   # Champion Blue - Arrogant, dramatic, thunderous
}

class PokemonNarrator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    async def generate_dialogue(self, clip_id: str, speaker: str, text: str) -> str:
        voice = VOICES.get(speaker, "en-US-GuyNeural")
        clip_path = os.path.join(self.output_dir, f"{clip_id}_{speaker.lower()}.mp3")
        
        if os.path.exists(clip_path) and os.path.getsize(clip_path) > 1000:
            return clip_path

        # Edge-TTS speech generation
        comm = edge_tts.Communicate(text, voice)
        await comm.save(clip_path)
        
        return clip_path

    def get_audio_duration(self, audio_path: str) -> float:
        try:
            data, fs = sf.read(audio_path)
            return len(data) / fs
        except Exception:
            return 4.0
