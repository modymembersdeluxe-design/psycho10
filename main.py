import os
import random

import cv2
import librosa
import numpy as np
from moviepy.editor import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoFileClip,
    concatenate_videoclips,
    vfx,
)
from pydub import AudioSegment
from pydub.effects import normalize, speedup

# ---------- CONFIG ----------
VIDEO_FOLDER = "media/videos"
AUDIO_FOLDER = "media/audio"
GIF_FOLDER = "media/gifs"
IMAGE_FOLDER = "media/images"
OUTPUT_FILE = "output/ytpmv_psycho_v10.mp4"
CLIP_DURATION_RANGE = (0.1, 3)
MAX_CLIPS = 500
MAX_OVERLAYS = 6
TEXT_COLORS = ["yellow", "cyan", "magenta", "lime", "red", "white"]
FONT_LIST = ["Comic-Sans-MS", "Impact", "Arial-Bold"]
MEME_TEXTS = ["LOL", "WTF", "OUCH", "OMG", "NOPE", "???", "???!"]


# ---------- HELPERS ----------
def get_random_file(folder, extensions):
    if not os.path.isdir(folder):
        return None
    files = [
        os.path.join(folder, file_name)
        for file_name in os.listdir(folder)
        if file_name.lower().endswith(extensions)
    ]
    return random.choice(files) if files else None


# ---------- AUDIO PROCESSING ----------
def get_beat_times(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    return librosa.frames_to_time(beat_frames, sr=sr)


def stutter_remix(audio_path):
    sound = AudioSegment.from_file(audio_path)
    snippet_len = random.randint(50, 400)
    start = random.randint(0, max(0, len(sound) - snippet_len))
    snippet = sound[start : start + snippet_len]
    stuttered = snippet * random.randint(2, 8)

    if random.random() < 0.5:
        stuttered = stuttered._spawn(stuttered.raw_data)
        stuttered = stuttered.set_frame_rate(
            int(stuttered.frame_rate * random.uniform(0.7, 1.3))
        )

    if random.random() < 0.5:
        stuttered = speedup(stuttered, playback_speed=random.uniform(1.2, 2.0))

    return normalize(stuttered)


# ---------- AI-DRIVEN CLIP SELECTION ----------
def ai_humor_score(clip):
    frame = clip.get_frame(0)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    motion = np.std(gray)
    brightness = np.mean(gray)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    return motion + brightness / 2 + len(faces) * 10


# ---------- VIDEO EFFECTS ----------
def glitch_effect(clip):
    def frame_glitch(frame):
        if random.random() < 0.25:
            frame = np.flip(frame, axis=1)
        if random.random() < 0.2:
            frame = np.rot90(frame, k=1)
        if random.random() < 0.3:
            frame = np.clip(frame * random.uniform(0.5, 3.5), 0, 255)
        return frame.astype(np.uint8)

    return clip.fl_image(frame_glitch)


def jitter_zoom_3d_effect(clip):
    def transform(get_frame, t):
        frame = get_frame(t)
        zoom = random.uniform(1.0, 1.7)
        h, w = frame.shape[:2]
        ch, cw = h // 2, w // 2
        new_h, new_w = int(h / zoom), int(w / zoom)
        start_h = max(0, min(ch - new_h // 2, h - new_h))
        start_w = max(0, min(cw - new_w // 2, w - new_w))
        frame = frame[start_h : start_h + new_h, start_w : start_w + new_w]
        frame = np.array(ImageClip(frame).resize((w, h)).get_frame(0))
        frame = np.roll(frame, random.randint(-6, 6), axis=1)
        frame = np.roll(frame, random.randint(-6, 6), axis=0)
        frame = np.array(ImageClip(frame).rotate(random.uniform(-15, 15)).get_frame(0))
        return frame.astype(np.uint8)

    return clip.fl(transform, apply_to=["mask"])


def kinetic_text(text, duration):
    txt_color = random.choice(TEXT_COLORS)
    font = random.choice(FONT_LIST)
    txt_clip = TextClip(
        text, fontsize=random.randint(60, 140), color=txt_color, font=font
    ).set_duration(duration)

    def jitter(get_frame, t):
        scale = random.uniform(0.8, 1.6)
        frame = get_frame(t)
        resized = ImageClip(frame).resize(
            (int(frame.shape[1] * scale), int(frame.shape[0] * scale))
        )
        return np.array(resized.get_frame(0))

    return txt_clip.fl(jitter, apply_to=["mask"])


def random_overlay(duration):
    file_path = (
        get_random_file(GIF_FOLDER, (".gif",))
        if random.random() < 0.5
        else get_random_file(IMAGE_FOLDER, (".png", ".jpg", ".jpeg"))
    )
    if not file_path:
        return None

    overlay = (
        VideoFileClip(file_path)
        if file_path.lower().endswith(".gif")
        else ImageClip(file_path)
    )
    overlay = overlay.set_duration(duration)
    overlay = overlay.resize(width=random.randint(50, 300))
    overlay = overlay.set_pos((random.randint(0, 400), random.randint(0, 240)))

    if random.random() < 0.5:
        overlay = overlay.fx(vfx.colorx, random.uniform(1.5, 4.0))

    return overlay


def particle_overlay(clip, density=50):
    def particle_frame(get_frame, t):
        frame = get_frame(t)
        for _ in range(density):
            x = random.randint(0, frame.shape[1] - 1)
            y = random.randint(0, frame.shape[0] - 1)
            frame[y, x] = [random.randint(0, 255) for _ in range(3)]
        return frame

    return clip.fl(particle_frame, apply_to=["mask"])


# ---------- VIDEO BUILD ----------
def build_video():
    video_clips = []
    audio_files = [
        get_random_file(AUDIO_FOLDER, (".mp3", ".wav", ".ogg"))
        for _ in range(MAX_CLIPS // 2)
    ]
    audio_files = [file_path for file_path in audio_files if file_path]

    main_audio_path = random.choice(audio_files) if audio_files else None

    candidate_clips = []
    for _ in range(MAX_CLIPS * 2):
        vid_path = get_random_file(VIDEO_FOLDER, (".mp4", ".mov", ".avi"))
        if not vid_path:
            continue
        clip = VideoFileClip(vid_path)
        candidate_clips.append((ai_humor_score(clip), clip))

    if not candidate_clips:
        raise RuntimeError(
            "No source videos found. Put files in media/videos before running Psycho10."
        )

    candidate_clips.sort(key=lambda item: item[0], reverse=True)
    selected_clips = [clip for _, clip in candidate_clips[:MAX_CLIPS]]

    for clip in selected_clips:
        dur = random.uniform(*CLIP_DURATION_RANGE)
        clip = clip.subclip(0, min(dur, clip.duration))
        clip = glitch_effect(clip)
        clip = jitter_zoom_3d_effect(clip)
        clip = clip.fx(vfx.colorx, random.uniform(1.5, 4.0))

        layers = [clip]
        for _ in range(random.randint(0, MAX_OVERLAYS)):
            overlay = random_overlay(clip.duration)
            if overlay:
                layers.append(overlay)

        if random.random() < 0.7:
            layers.append(kinetic_text(random.choice(MEME_TEXTS), clip.duration))

        layers.append(particle_overlay(clip, density=random.randint(30, 80)))
        video_clips.append(CompositeVideoClip(layers))

    final_video = concatenate_videoclips(video_clips, method="compose", padding=-0.05)

    if main_audio_path:
        sound = stutter_remix(main_audio_path)
        tmp_file = "temp_audio_v10.wav"
        sound.export(tmp_file, format="wav")
        final_video = final_video.set_audio(AudioFileClip(tmp_file))

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    final_video.write_videofile(
        OUTPUT_FILE, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast"
    )


if __name__ == "__main__":
    build_video()
