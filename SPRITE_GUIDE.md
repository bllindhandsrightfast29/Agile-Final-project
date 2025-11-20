# 🎨 Sprite Design Guide - 2D NES Ninja Animals

This guide provides visual descriptions and ASCII art concepts for each ninja animal character's sprite design.

## NES Technical Constraints

### Sprite Limitations
- **Max sprite size**: 8x8 or 8x16 pixels per hardware sprite
- **Character sprites**: Built from multiple hardware sprites (4-8 sprites per character)
- **Colors per sprite**: 3 colors + transparency (4-color palette)
- **Total palettes**: 8 palettes available
- **Screen sprites**: Maximum 64 sprites on screen

### Color Palette Reference

```
NES Color Palette (Simplified):
$00 = Black        $10 = Light Gray   $20 = Light Blue
$01 = Dark Gray    $11 = White        $21 = Cyan
$02 = Blue         $12 = Pink         $22 = Light Green
$03 = Purple       $13 = Red          $23 = Yellow
$04 = Dark Red     $14 = Orange       $24 = Light Orange
```

---

## S-RANK CHARACTERS

### 🐸 Gambit the Packet Toad (32x32 pixels)

**Palette**: Orange ($14), Brown ($04), Blue ($02), Black ($00)

```
ASCII Representation (Idle Stance):

    ████████████████
  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
  ██▓▓░░████░░▓▓▓▓██
██▓▓▓▓░░████░░▓▓▓▓▓▓██
██▓▓▓▓████████▓▓▓▓▓▓██
██▓▓▓▓░░░░░░░░▓▓▓▓▓▓██
  ██▓▓████████▓▓▓▓██
  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
    ████████████████
    ██████  ██████
    ██████  ██████
    ██████  ██████
```

**Animation Frames**:
- Frame 1: Idle (mouth closed)
- Frame 2: Idle blink
- Frame 3: Water Style jutsu (mouth open, water pixels)
- Frame 4: Jump (compressed vertically)

**Special Features**:
- WiFi headband (3 curved lines)
- Scroll on back (binary code pattern)
- Kata blade (gray/silver pixels)

---

### 🐍 Pythonix the Code Serpent (16x64 pixels elongated)

**Palette**: White ($11), Green ($22), Purple ($03), Black ($00)

```
ASCII Representation (Coiled):

      ██████
    ██░░▓▓██
    ██░░▓▓██  ← Eyes (green glow)
    ████████
    ██▓▓▓▓██
  ██▓▓▓▓▓▓▓▓██
██▓▓▓▓▓▓▓▓▓▓▓▓██
██▓▓░░░░░░░░▓▓██  ← Circuit patterns
██▓▓░░░░░░░░▓▓██
  ██▓▓▓▓▓▓▓▓██
    ████████
      ████
       ██
```

**Animation Frames**:
- Frame 1: Coiled
- Frame 2: Striking forward
- Frame 3: Code matrix rain effect
- Frame 4: Shadow clone split

**Special Features**:
- Green circuit board patterns on scales
- Forked tongue with binary code
- Purple outline glow during jutsu

---

### 🐵 Enma the Firewall Guardian (32x32 pixels)

**Palette**: White ($11), Gold ($23), Brown ($04), Black ($00)

```
ASCII Representation (Staff Stance):

    ████████████
  ██▓▓▓▓▓▓▓▓▓▓██
  ██░░██████░░██
  ██▓▓▓▓▓▓▓▓▓▓██
  ████████████████
██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
  ██▓▓▓▓▓▓▓▓▓▓██
    ██████████
  ██████  ██████
██▓▓▓▓██  ██▓▓▓▓██
████        ████
│││ STAFF │││
│││││││││││││
```

**Animation Frames**:
- Frame 1: Standing guard
- Frame 2: Staff strike
- Frame 3: Transform to wall (pixelated brick pattern)
- Frame 4: Defensive stance

**Special Features**:
- Wise beard (white pixels with flow)
- Golden staff with rule icons
- Armor plates (brown/gold alternating)

---

### 🦊 Kurama the Nine-Tailed Phisher (64x64 pixels - BOSS SIZE)

**Palette**: Orange ($14), Red ($13), Gold ($23), Black ($00)

```
ASCII Representation (Intimidating Stance):

        ██████████████
      ██▓▓▓▓▓▓▓▓▓▓▓▓██
    ██▓▓▓▓░░░░░░▓▓▓▓▓▓██
    ██▓▓░░████████░░▓▓██  ← Red eyes
  ██▓▓▓▓████████████▓▓▓▓██
  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
██▓▓▓▓▓▓░░░░░░░░░░▓▓▓▓▓▓▓▓██
██▓▓▓▓▓▓████████████▓▓▓▓▓▓██
  ██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
    ████████████████████
    ~~~ NINE TAILS ~~~
   /│\ /│\ /│\ /│\ /│\
  /││\/││\/││\/││\/││\
```

**Animation Frames**:
- Frame 1: Idle menace (tails swaying)
- Frame 2: Chakra aura (orange glow expansion)
- Frame 3: Tailed Beast Bomb charge
- Frame 4: Roar (shake effect)

**Special Features**:
- Nine fiber optic tails (data stream particles)
- Red menacing eyes (2x2 pixels, intense)
- Orange chakra aura (animated flicker)
- Black markings (Naruto seal patterns)

---

## A-RANK CHARACTERS

### 🐌 Katsuya the Forensics Slug (32x24 pixels)

**Palette**: Light Blue ($20), White ($11), Pink ($12), Black ($00)

```
ASCII Representation:

  ╔══════╗
 ││  ○  ○││  ← Antennae
 ╚════════╝
██▓▓▓▓▓▓▓▓▓▓██
██▓▓░░░░░░░░▓▓██
██▓▓▓▓▓▓▓▓▓▓▓▓██
  ████████████
  ~~~healing~~~
  ~~~trail~~~~
```

**Special Features**:
- Glowing antennae (pulse animation)
- Healing pixel trail (sparkle effect)
- Medical cross symbol on body

---

### 🦅 Garuda the Recon Hawk (24x24 pixels + wingspan)

**Palette**: Brown ($04), Gold ($23), Red ($13), Black ($00)

```
ASCII Representation (Flying):

    ╱▀▀▀▀▀▀╲
   │ ●  ● │ ← Radar eyes
    ╲▂▂▂▂▂╱
╱▀▀▀▀████▀▀▀▀╲
░░░░██▓▓██░░░░
░░░░██▓▓██░░░░
    ██▓▓██
    ██  ██
```

**Special Features**:
- Red scanning eyes (sweep effect)
- Radar dish wing patterns
- Gold talons

---

### 🦎 Phantom the Stealth Chameleon (20x20 pixels)

**Palette**: Variable (shifts between all 8 palettes!)

```
ASCII Representation (Multiple states):

Normal:        Blending:      Invisible:
  ██████         ░░░░░░         ○ ○
 ██▓▓▓▓██       ░▓▓▓▓░           ◡
██●▓▓▓▓●██     ░▓▓▓▓▓░
 ████████       ░░░░░░
  ██  ██         ░  ░
```

**Special Features**:
- Color cycling animation (every 4 frames)
- Transparency effect (dithered pixels)
- Rotating eyes (different directions)

---

### 🦉 Athena the Cipher Owl (24x24 pixels)

**Palette**: Purple ($03), Blue ($02), Gold ($23), Black ($00)

```
ASCII Representation:

    ╔═══╗
   ║ ◎ ◎ ║  ← Cipher wheel eyes
    ╚═══╝
  ██▓▓▓▓▓▓██
 ██░▓▓▓▓▓▓░██
██░░▓▓▓▓▓▓░░██
 ██░░░░░░░░██
  ╱██████╲
 ╱        ╲
```

**Special Features**:
- Rotating cipher wheels in eyes
- Encryption formulas on feathers
- Glow effect during decryption

---

## B-RANK CHARACTERS

### 🐕 Pakkun the Exploit Hound (16x16 pixels)

**Palette**: Brown ($04), Black ($00), Red ($13)

```
ASCII Representation:

  ████████
 ██●▓▓▓●██
 ████▲████  ← Red nose
██▓▓▓▓▓▓▓▓██
██▓▓▓▓▓▓▓▓██
 ██████████
 ██  ████  ██
```

**Special Features**:
- Red nose glows when detecting CVEs
- Leaf village bandana (blue)
- Tracking sparkles (white pixels)

---

### 🕷️ Arachnia the Web Crawler (20x20 pixels)

**Palette**: Red ($13), Black ($00), White ($11)

```
ASCII Representation:

╱╲  ╱▀▀▀╲  ╱╲
│ ╲║ ● ● ║╱ │
 ╲ ║▀▀▀▀▀║ ╱
  ╱███████╲
 │  ││ ││  │
 │  ││ ││  │
╱   ││ ││   ╲
```

**Special Features**:
- Pixel web pattern (white lines)
- Multiple green eyes
- Web shooting animation

---

### 🐼 Taichi the Password Panda (28x28 pixels)

**Palette**: Black ($00), White ($11), Green ($22)

```
ASCII Representation:

  ████████████
 ██░░██████░░██
 ██░░██████░░██
  ██████████████
██▓▓▓▓▓▓▓▓▓▓▓▓██
██▓▓▓▓▓▓▓▓▓▓▓▓██
  ██▓▓▓▓▓▓▓▓██
  ██████████
 ███      ███
███        ███
```

**Special Features**:
- Bamboo armor (green plates)
- Password scroll (kanji characters)
- Meditation pose variant

---

## JUTSU EFFECT SPRITES

### Water Style Effects
```
Packet Flood:
~▓▓▓▓▓▓~
~~▓▓▓▓~~
~~~▓▓~~~
~~~~▓~~~
```

### Fire Effects
```
Fox Fire:
   ▲▲
  ▲▓▓▲
 ▲▓▓▓▓▲
▲▓▓▓▓▓▓▲
```

### Lightning Effects
```
Deauth Strike:
│
╱│╲
 │╲│╱
  ╲│╱
   ╲
```

### Shadow Clone
```
Original → Clone:
██▓▓██ → ░░▓▓░░
██▓▓██ → ░░▓▓░░
```

### Summoning Smoke
```
Frame 1:  Frame 2:  Frame 3:
  ░░░      ▒▒▒      ▓▓▓
 ░░░░     ▒▒▒▒     ▓▓▓▓
  ░░░      ▒▒▒      ▓▓▓
```

---

## ANIMATION GUIDELINES

### Standard Animation Cycles

1. **Idle Animation** (4 frames, loop)
   - Frame 1: Base pose
   - Frame 2: Slight bob down
   - Frame 3: Base pose
   - Frame 4: Slight bob up

2. **Attack Animation** (6 frames)
   - Frames 1-2: Wind-up
   - Frames 3-4: Strike
   - Frames 5-6: Recovery

3. **Jutsu Animation** (8 frames)
   - Frames 1-3: Hand signs
   - Frames 4-6: Chakra charge
   - Frames 7-8: Release

4. **Damage Animation** (3 frames)
   - Frame 1: Flash white
   - Frame 2: Knockback
   - Frame 3: Return to idle

### Movement

- **Walk**: 4-frame cycle, 2 pixels per frame
- **Run**: 4-frame cycle, 4 pixels per frame
- **Jump**: 6-frame arc (up 3 frames, down 3 frames)

---

## SPRITE SHEET LAYOUT SUGGESTION

```
Character Sheet (128x128 pixels):

┌────────┬────────┬────────┬────────┐
│ Idle 1 │ Idle 2 │ Idle 3 │ Idle 4 │
├────────┼────────┼────────┼────────┤
│ Walk 1 │ Walk 2 │ Walk 3 │ Walk 4 │
├────────┼────────┼────────┼────────┤
│Attack1 │Attack2 │Attack3 │Attack4 │
├────────┼────────┼────────┼────────┤
│Jutsu 1 │Jutsu 2 │Damage  │ KO     │
└────────┴────────┴────────┴────────┘
```

---

## TIPS FOR PIXEL ARTISTS

1. **Start with silhouette** - Make sure character is recognizable in pure black
2. **Use dithering sparingly** - Alternating pixels for shading (NES style)
3. **Limit colors** - Stick to 4 colors per sprite object
4. **Add personality** - Small details like glowing eyes, swaying tails
5. **Animation first** - Design with animation in mind
6. **Test at 1x** - View at actual pixel size to check readability

## REFERENCE TOOLS

- **NES Palette**: [https://lospec.com/palette-list/nintendo-entertainment-system]
- **Sprite Editors**: Aseprite, PyxelEdit, GIMP (pixel mode)
- **NES Restrictions**: 8x8 or 8x16 base, 64 sprites max, 4 colors + transparent

---

*Ready to bring these ninja animals to life in glorious 8-bit!* 🎨
