# Psycho10

**Psycho10** is a chaotic automated video remix generator inspired by early YouTube Poop (YTP) editing styles, 2000s internet aesthetics, and high-energy meme remix culture. It combines random media selection, heavy visual effects, kinetic typography, and aggressive audio manipulation to automatically generate surreal remix videos.

The project uses **Python** and **MoviePy 1.0.1** to build fast-paced, glitchy compilation edits using videos, GIF overlays, images, and audio samples.

---

# Features

## Automated Remix Generation

* Randomly selects media from multiple folders.
* Automatically builds fast-paced remix videos.
* Generates chaotic edits with rapid transitions.

## Visual Style & Aesthetics

### Low-Fidelity Textures

Many clips intentionally simulate **240p / 360p video quality**, heavy compression artifacts, and a **4:3 aspect ratio** similar to early YouTube videos.

### Kinetic Typography

Fast moving meme text with bold colors and classic internet fonts such as:

* Comic Sans
* Impact
* Arial Bold

Text may bounce, jitter, zoom, or appear suddenly for comedic emphasis.

### Bright Saturated Palettes

High contrast color grading is applied automatically to produce loud, surreal visuals.

### Surreal Imagery

Random overlays and edits including:

* GIF layers
* Image sprites
* Particle effects
* Glitch frames
* RGB split
* Strobe flashes

---

# Editing Style

Psycho10 recreates common editing styles from early meme remix videos.

### Sentence Mixing

Audio is chopped into fragments and rearranged so characters appear to say new phrases.

### Rapid Cut Editing

Clips often last **0.1 to 3 seconds** creating fast chaotic pacing.

### Overlay Chaos

Multiple layers may appear simultaneously:

* GIF animations
* Meme text
* Particles
* Image sprites

---

# Audio & Sound Design

## Ear-Rape / Distortion

Sudden volume spikes and heavy distortion may be applied for comedic shock.

## Stutter Loops

Small audio fragments repeat rapidly to create mechanical rhythmic sounds.

Example:

```
ha ha ha ha ha ha
wow wow wow wow
```

## Nostalgic Synth Jingles

High pitched ringtone-era melodies inspired by early 2000s internet sounds.

## Layered Sound Effects

Multiple cartoon sound effects may overlap:

* Boings
* Whistles
* Explosions
* Crash sounds

---

# Project Structure

Recommended folder layout:

```
Psycho10/
│
├── media/
│   ├── videos/
│   ├── audio/
│   ├── gifs/
│   └── images/
│
├── output/
│
├── temp/
│
├── main.py
│
└── README.md
```

### Folder Purpose

| Folder | Description                  |
| ------ | ---------------------------- |
| videos | Source video clips           |
| audio  | Music, speech, sound effects |
| gifs   | Animated overlays            |
| images | Static overlays              |
| output | Rendered videos              |
| temp   | Temporary processing files   |

---

# Installation

Install Python dependencies:

```
pip install moviepy==1.0.1 numpy opencv-python librosa pydub
```

FFmpeg is required for MoviePy.

Download FFmpeg and add it to the system PATH.

---

# Running Psycho10

Run the script from the project directory:

```
python main.py
```

The program will:

1. Scan media folders
2. Randomly select clips
3. Apply visual effects
4. Remix audio samples
5. Combine clips with transitions
6. Export a chaotic remix video

Output video:

```
output/ytpmv_psycho_v10.mp4
```

---

# Customization

Several settings can be modified inside `main.py`.

Examples:

```
CLIP_DURATION_RANGE
MAX_CLIPS
MAX_OVERLAYS
TEXT_COLORS
FONT_LIST
```

Reducing clip count improves performance on slower computers.

---

# Performance Notes

Rendering hundreds of clips with effects can be CPU intensive.

Tips:

* Lower MAX_CLIPS for faster rendering.
* Use shorter video clips.
* Use ultrafast encoding preset.

---

# Inspiration

Psycho10 is inspired by early internet remix culture including:

* YouTube Poop editing
* 2000s CGI commercial mascots
* Meme mashups
* High-energy synth music videos
* Surreal internet humor

---

# License

Open experimentation project intended for creative remixing and automated video generation.

---

# Warning

The generated videos may contain:

* Rapid flashing lights
* Loud audio spikes
* Chaotic visuals

Viewer discretion is advised.

---

End of Psycho10 README.
