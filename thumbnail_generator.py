import os
import math
from PIL import Image, ImageDraw, ImageFont

def find_font(font_type="bold", size=20):
    candidates = []
    if font_type == "impact":
        candidates = [
            "C:/Windows/Fonts/impact.ttf",
            "/usr/share/fonts/truetype/msttcorefonts/impact.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
        ]
    elif font_type == "bold":
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]

    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def generate_youtube_thumbnail(output_path=None):
    """
    Generates a viral, high-CTR YouTube thumbnail (1920x1080) for the
    Pokémon Magikarp Solo Run challenge.
    """
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "recordings", "thumbnail.png")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    w, h = 1920, 1080

    # 1. Background: Dark electric gradient arena
    img = Image.new("RGB", (w, h), (14, 18, 26))
    draw = ImageDraw.Draw(img)

    # Radial/diagonal atmospheric background lighting
    for r in range(700, 0, -25):
        alpha = int(45 * (1 - r / 700))
        # Orange glow bottom-left for Magikarp
        draw.ellipse([200 - r, 700 - r, 200 + r, 700 + r], fill=(alpha + 20, int(alpha * 0.7), 10))
        # Cyan-blue glow top-right for Champion arena
        draw.ellipse([1600 - r, 350 - r, 1600 + r, 350 + r], fill=(10, int(alpha * 0.8), alpha + 30))

    font_huge = find_font("impact", 76)
    font_big = find_font("impact", 56)
    font_mid = find_font("bold", 34)
    font_badge = find_font("bold", 28)
    font_hp = find_font("bold", 42)

    # 2. TOP BANNER: Viral Headline
    # Yellow pill for hook
    draw.rectangle([60, 45, 1200, 140], fill=(255, 204, 0))
    draw.text((85, 55), "CAN AN AI BEAT POKÉMON...", font=font_huge, fill=(10, 12, 16))

    # Red/Crimson punchline
    draw.rectangle([60, 155, 1380, 255], fill=(225, 30, 45))
    draw.text((85, 165), "...WITH ONLY A MAGIKARP?!", font=font_huge, fill=(255, 255, 255))

    # 3. LEFT ARENA CARD: MAGIKARP (THE 1 HP GOD)
    mag_box = [100, 310, 800, 880]
    # Gold border aura
    draw.rectangle([mag_box[0] - 8, mag_box[1] - 8, mag_box[2] + 8, mag_box[3] + 8], fill=(255, 215, 0))
    draw.rectangle(mag_box, fill=(35, 20, 15))

    # Level 100 Badge
    draw.rectangle([130, 340, 420, 395], fill=(255, 140, 0))
    draw.text((150, 350), "Lv. 100 MAGIKARP", font=font_badge, fill=(255, 255, 255))

    # Character Card Center
    draw.rectangle([140, 420, 760, 710], fill=(55, 28, 18), outline=(255, 180, 0), width=4)
    draw.text((220, 520), "MAGIKARP", font=font_huge, fill=(255, 215, 0))
    draw.text((260, 610), "[THE RED SOLO SWEEPER]", font=font_badge, fill=(255, 255, 255))

    # HP Emergency Pill
    draw.rectangle([140, 730, 760, 850], fill=(20, 20, 24), outline=(225, 40, 40), width=3)
    draw.text((170, 745), "HP: 1 / 204  [CRITICAL!]", font=font_hp, fill=(255, 50, 50))
    # Draw HP Bar (1 pixel of red remaining)
    draw.rectangle([170, 805, 730, 825], fill=(45, 50, 60))
    draw.rectangle([170, 805, 178, 825], fill=(255, 50, 50))

    # 4. RIGHT ARENA CARD: CHAMPION BLUE & CHARIZARD
    opp_box = [1120, 310, 1820, 880]
    draw.rectangle([opp_box[0] - 8, opp_box[1] - 8, opp_box[2] + 8, opp_box[3] + 8], fill=(0, 180, 240))
    draw.rectangle(opp_box, fill=(18, 26, 38))

    # Level 65 Badge
    draw.rectangle([1150, 340, 1480, 395], fill=(0, 140, 220))
    draw.text((1170, 350), "Lv. 65 CHARIZARD", font=font_badge, fill=(255, 255, 255))

    # Opponent Card Center
    draw.rectangle([1160, 420, 1780, 710], fill=(25, 38, 56), outline=(0, 180, 240), width=4)
    draw.text((1260, 520), "CHARIZARD", font=font_huge, fill=(255, 120, 0))
    draw.text((1270, 610), "[CHAMPION BLUE'S ACE]", font=font_badge, fill=(200, 225, 255))

    # Opponent Status
    draw.rectangle([1160, 730, 1780, 850], fill=(20, 24, 30), outline=(0, 160, 220), width=3)
    draw.text((1200, 745), "STATUS: 1-HIT KO TARGET", font=font_hp, fill=(255, 215, 0))
    draw.rectangle([1200, 805, 1740, 825], fill=(255, 60, 60))

    # 5. CENTER DRAMATIC ARROW & STRATEGY BADGE
    # Big diagonal action attack arrow
    draw.polygon([(820, 580), (1080, 540), (1030, 500), (1095, 540), (1030, 580)], fill=(255, 40, 40))
    
    # Explosive Badge in Center
    draw.rectangle([760, 460, 1180, 560], fill=(235, 30, 40), outline=(255, 255, 255), width=4)
    draw.text((790, 475), "200 BP FLAIL", font=font_big, fill=(255, 255, 255))
    draw.text((820, 525), "MAXIMUM POWER!", font=font_badge, fill=(255, 255, 0))

    # 6. BOTTOM BANNER BADGES
    draw.rectangle([60, 920, 1860, 1020], fill=(10, 12, 16), outline=(255, 204, 0), width=3)
    draw.text((90, 945), "SOLO CHALLENGE", font=font_big, fill=(255, 204, 0))
    draw.text((580, 952), "|  FOCUS SASH ENDURE  |  INDIGO PLATEAU FINALS  |  NO ITEMS IN BATTLE", font=font_mid, fill=(255, 255, 255))

    img.save(output_path, "PNG")
    print(f"[+] High-CTR Pokémon Challenge Thumbnail saved: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_youtube_thumbnail()
