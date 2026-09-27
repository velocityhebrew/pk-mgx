import asyncio
import os
import sys
import time
import subprocess
from datetime import timedelta

from pokemon_battle_engine import get_battle_turns
from battle_renderer import PokemonBattleRenderer
from match_narrator import PokemonNarrator
from thumbnail_generator import generate_youtube_thumbnail

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")
VOICE_DIR = os.path.join(BASE_DIR, "voiceover")
FRAMES_DIR = os.path.join(RECORDINGS_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(RECORDINGS_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(RECORDINGS_DIR, "pokemon_magikarp_challenge.mp4")
SRT_FILE = os.path.join(RECORDINGS_DIR, "pokemon_subtitles.srt")

def format_srt_time(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

async def generate_pokemon_video(limit_turns: int = None):
    turns = get_battle_turns()
    if limit_turns:
        turns = turns[:limit_turns]

    print("=" * 70)
    print("    POKÉMON AI CHALLENGE - 1080P 60FPS EPIDEMIC BROADCAST")
    print("=" * 70)
    print(f"Total Turns: {len(turns)} (Dual Trainer Audio: Red & Blue)")
    print(f"AI Red (Strategist): en-US-GuyNeural")
    print(f"Champion Blue (Rival): en-US-ChristopherNeural")
    print(f"Master Video Output: {OUTPUT_VIDEO}")
    print("=" * 70)

    renderer = PokemonBattleRenderer()
    narrator = PokemonNarrator(VOICE_DIR)

    battle_history = []
    segment_files = []
    subtitles = []
    total_elapsed = 0.0

    seg_counter = 0

    for idx, turn_data in enumerate(turns):
        t_num = turn_data.get("turn", idx)
        action_text = turn_data.get("active_action", "")
        
        # Two dialogue phases per turn:
        # Phase A: Red's Tactical Analysis & Move Execution
        # Phase B: Blue's Reaction & Counter-Attack
        dialogue_phases = [
            ("Red", turn_data["red_dialogue"]),
            ("Blue", turn_data["blue_dialogue"])
        ]

        for speaker, speech_text in dialogue_phases:
            seg_counter += 1
            clip_id = f"turn_{t_num:02d}_{speaker.lower()}"

            # 1. Generate Voiceover Dialogue Audio
            audio_path = await narrator.generate_dialogue(clip_id, speaker, speech_text)
            audio_dur = narrator.get_audio_duration(audio_path)
            clip_dur = audio_dur + 0.5  # Natural pause between lines

            # 2. Render 1080p Arena Frame
            frame_img = renderer.render_frame(
                turn_data=turn_data,
                battle_history=battle_history,
                active_speaker=speaker,
                subtitle=speech_text
            )
            frame_path = os.path.join(FRAMES_DIR, f"frame_seg_{seg_counter:03d}.png").replace("\\", "/")
            frame_img.save(frame_path)

            # 3. Record Subtitle
            subtitles.append({
                "start": total_elapsed,
                "end": total_elapsed + clip_dur,
                "speaker": "TRAINER RED (AI)" if speaker == "Red" else "CHAMPION BLUE",
                "text": speech_text
            })
            total_elapsed += clip_dur

            # 4. Render Video Segment with FFmpeg (1080p 60FPS)
            seg_mp4 = os.path.join(RECORDINGS_DIR, f"seg_poke_{seg_counter:03d}.mp4").replace("\\", "/")
            segment_files.append(seg_mp4)

            if not (os.path.exists(seg_mp4) and os.path.getsize(seg_mp4) > 5000):
                cmd = [
                    "ffmpeg", "-y",
                    "-loop", "1", "-t", str(clip_dur), "-i", frame_path,
                    "-i", audio_path.replace("\\", "/"),
                    "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                    "-r", "60",
                    "-c:a", "aac", "-b:a", "192k",
                    "-af", f"apad=whole_dur={clip_dur}",
                    "-shortest",
                    seg_mp4
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  [+] Segment {seg_counter:02d} rendered: [{speaker}] Turn {t_num} ({clip_dur:.1f}s)")
            else:
                print(f"  [+] Segment {seg_counter:02d} cached: [{speaker}] Turn {t_num} ({clip_dur:.1f}s)")

        # Update battle action log after both speakers complete the turn
        battle_history.append({
            "turn": t_num,
            "action": action_text
        })

    # 5. Write Subtitles File (.srt)
    print("\n[*] Writing Pokémon match subtitles...")
    with open(SRT_FILE, "w", encoding="utf-8") as f:
        for i, sub in enumerate(subtitles, 1):
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(sub['start'])} --> {format_srt_time(sub['end'])}\n")
            f.write(f"[{sub['speaker']}]: {sub['text']}\n\n")
    print(f"[+] Subtitles generated: {SRT_FILE}")

    # 6. Concat all segments into Final Master Video
    concat_list = os.path.join(RECORDINGS_DIR, "pokemon_concat_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for s in segment_files:
            f.write(f"file '{s}'\n")

    print("[*] Merging all segments into master 60FPS Pokémon Broadcast Video with FFmpeg...")
    final_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        OUTPUT_VIDEO
    ]
    subprocess.run(final_cmd, check=True)

    # Clean up intermediate segment files
    for s in segment_files:
        try:
            os.remove(s)
        except Exception:
            pass
    try:
        os.remove(concat_list)
    except Exception:
        pass

    # 7. Generate YouTube Thumbnail
    thumb_path = generate_youtube_thumbnail()

    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print("\n" + "=" * 70)
    print("[SUCCESS] POKÉMON AI CHALLENGE VIDEO GENERATED SUCCESSFULLY!")
    print(f"Video File: {OUTPUT_VIDEO}")
    print(f"Video Size: {size_mb:.2f} MB")
    print(f"Duration:   {total_elapsed:.1f}s ({total_elapsed/60.0:.2f} mins)")
    print(f"Subtitles:  {SRT_FILE}")
    print(f"Thumbnail:  {thumb_path}")
    print("=" * 70)
    return OUTPUT_VIDEO

if __name__ == "__main__":
    limit = None
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        limit = int(sys.argv[1])
    asyncio.run(generate_pokemon_video(limit_turns=limit))
