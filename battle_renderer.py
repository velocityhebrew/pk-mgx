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

class PokemonBattleRenderer:
    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height

        self.title_font = find_font("impact", 28)
        self.header_font = find_font("bold", 20)
        self.badge_font = find_font("bold", 16)
        self.log_font = find_font("regular", 16)
        self.log_bold = find_font("bold", 16)
        self.name_font = find_font("bold", 24)
        self.hp_font = find_font("bold", 18)
        self.sub_font = find_font("regular", 21)
        self.sub_bold = find_font("bold", 21)
        self.crit_font = find_font("impact", 38)

    def draw_hp_bar(self, draw: ImageDraw.ImageDraw, x, y, w, h, current_hp, max_hp):
        """Draws a classic Pokémon green-yellow-red HP bar."""
        ratio = max(0.0, min(1.0, current_hp / max(1, max_hp)))
        # Background slot
        draw.rectangle([x, y, x + w, y + h], fill=(35, 40, 50), outline=(70, 80, 95), width=2)
        
        # Color transition
        if ratio > 0.5:
            bar_col = (0, 230, 110) # Vibrant green
        elif ratio > 0.2:
            bar_col = (245, 180, 30) # Yellow-amber
        else:
            bar_col = (235, 55, 55) # Red danger

        fill_w = int(w * ratio)
        if fill_w > 0:
            draw.rectangle([x + 2, y + 2, x + fill_w - 2, y + h - 2], fill=bar_col)

    def draw_arrow(self, draw: ImageDraw.ImageDraw, p1, p2, color=(235, 55, 55), width=12):
        """Draws an action arrow from attacker to defender platform."""
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        dist = math.hypot(dx, dy)
        if dist < 10:
            return

        ux = dx / dist
        uy = dy / dist
        nx = -uy
        ny = ux

        head_len = 34
        head_w = 28
        target_x = x2 - ux * 20
        target_y = y2 - uy * 20

        shaft_end_x = target_x - ux * head_len
        shaft_end_y = target_y - uy * head_len

        draw.line([(x1, y1), (shaft_end_x, shaft_end_y)], fill=color, width=width)
        tip = (target_x, target_y)
        left = (shaft_end_x + nx * (head_w / 2), shaft_end_y + ny * (head_w / 2))
        right = (shaft_end_x - nx * (head_w / 2), shaft_end_y - ny * (head_w / 2))
        draw.polygon([tip, left, right], fill=color)

    def render_frame(self, turn_data, battle_history=None, active_speaker="Red", subtitle=""):
        if battle_history is None:
            battle_history = []

        img = Image.new("RGB", (self.width, self.height), (18, 22, 28))
        draw = ImageDraw.Draw(img)

        # -------------------------------------------------------------
        # 1. TOP TITLE HEADER
        # -------------------------------------------------------------
        draw.rectangle([0, 0, self.width, 52], fill=(12, 14, 18))
        draw.rectangle([0, 50, self.width, 52], fill=(235, 55, 55)) # Crimson accent
        draw.text((40, 12), "POKEMON AI HARDCORE CHALLENGE  |  MAGIKARP SOLO SWEEP", font=self.title_font, fill=(255, 255, 255))
        draw.text((1500, 15), "MINIMAX DAMAGE ENGINE: 100% PRECISION", font=self.header_font, fill=(0, 230, 255))

        # -------------------------------------------------------------
        # 2. LEFT SIDEBAR: STRATEGY BADGE & BATTLE LOG
        # -------------------------------------------------------------
        sb_x = 40
        sb_w = 700

        # Strategy & Tactical Badge
        strat_y = 68
        draw.rectangle([sb_x, strat_y, sb_x + sb_w, strat_y + 75], fill=(26, 32, 42), outline=(218, 165, 32), width=2)
        draw.text((sb_x + 18, strat_y + 12), "CURRENT STRATEGY:", font=self.badge_font, fill=(218, 165, 32))
        draw.text((sb_x + 18, strat_y + 38), turn_data.get("strategy", "Focus Sash + 200 BP Flail"), font=self.name_font, fill=(0, 230, 255))

        # Trainer Profile Cards
        # Blue Card (Top)
        blue_y = 155
        b_active = (active_speaker == "Blue")
        draw.rectangle([sb_x, blue_y, sb_x + sb_w, blue_y + 90], fill=(26, 30, 38), outline=(0, 200, 255) if b_active else (45, 52, 65), width=2)
        # Circular Avatar Blue
        draw.ellipse([sb_x + 20, blue_y + 15, sb_x + 80, blue_y + 75], fill=(15, 25, 40), outline=(0, 200, 255), width=2)
        draw.text((sb_x + 38, blue_y + 26), "B", font=self.title_font, fill=(0, 200, 255))
        draw.text((sb_x + 95, blue_y + 18), "CHAMPION BLUE (Rival)", font=self.header_font, fill=(255, 255, 255))
        draw.text((sb_x + 95, blue_y + 48), "Indigo Plateau Champion  |  Remaining: 6 Pokemon", font=self.log_font, fill=(160, 175, 195))

        # Red Card (Bottom)
        red_y = 255
        r_active = (active_speaker == "Red")
        draw.rectangle([sb_x, red_y, sb_x + sb_w, red_y + 90], fill=(26, 30, 38), outline=(235, 60, 60) if r_active else (45, 52, 65), width=2)
        # Circular Avatar Red
        draw.ellipse([sb_x + 20, red_y + 15, sb_x + 80, red_y + 75], fill=(40, 15, 15), outline=(235, 60, 60), width=2)
        draw.text((sb_x + 38, red_y + 26), "R", font=self.title_font, fill=(235, 60, 60))
        draw.text((sb_x + 95, red_y + 18), "TRAINER RED (AI Operator)", font=self.header_font, fill=(255, 255, 255))
        draw.text((sb_x + 95, red_y + 48), "Solo Challenge: Lv. 100 Magikarp  |  Item: Focus Sash", font=self.log_font, fill=(160, 175, 195))

        # Battle Action Log (Center-Left)
        log_y = 355
        log_h = 540
        draw.rectangle([sb_x, log_y, sb_x + sb_w, log_y + log_h], fill=(18, 22, 28), outline=(45, 52, 65), width=2)
        
        # Log Header
        draw.rectangle([sb_x, log_y, sb_x + sb_w, log_y + 42], fill=(26, 32, 42))
        draw.text((sb_x + 20, log_y + 12), "TURN #", font=self.log_bold, fill=(170, 185, 205))
        draw.text((sb_x + 120, log_y + 12), "BATTLE ACTION & DAMAGE ROLL", font=self.log_bold, fill=(255, 215, 0))

        # Display last 11 battle actions
        visible_logs = battle_history[-11:]
        for idx, item in enumerate(visible_logs):
            row_y = log_y + 50 + idx * 43
            is_active_row = (idx == len(visible_logs) - 1)

            if is_active_row:
                draw.rectangle([sb_x + 3, row_y - 4, sb_x + sb_w - 3, row_y + 36], fill=(35, 45, 58), outline=(218, 165, 32), width=1)
            elif idx % 2 == 1:
                draw.rectangle([sb_x + 3, row_y - 4, sb_x + sb_w - 3, row_y + 36], fill=(22, 26, 34))

            draw.text((sb_x + 25, row_y + 4), f"T-{item.get('turn', idx+1)}", font=self.log_bold, fill=(0, 230, 255))
            act_txt = item.get("action", "")
            if len(act_txt) > 52:
                act_txt = act_txt[:50] + "..."
            draw.text((sb_x + 120, row_y + 4), act_txt, font=self.log_font, fill=(255, 255, 255) if is_active_row else (200, 210, 225))

        # -------------------------------------------------------------
        # 3. RIGHT PANEL: 3D-STYLE POKÉMON BATTLE STADIUM
        # -------------------------------------------------------------
        arena_x = 770
        arena_y = 68
        arena_w = 1110
        arena_h = 827

        # Arena Border
        draw.rectangle([arena_x, arena_y, arena_x + arena_w, arena_y + arena_h], fill=(24, 30, 40), outline=(65, 75, 95), width=3)

        # Stadium Field Background Gradient (Gym Battlefield)
        draw.rectangle([arena_x + 4, arena_y + 4, arena_x + arena_w - 4, arena_y + arena_h - 4], fill=(35, 42, 54))
        # Dirt battle ring
        draw.ellipse([arena_x + 120, arena_y + 240, arena_x + arena_w - 120, arena_y + arena_h - 80], fill=(85, 120, 65), outline=(120, 155, 80), width=4)

        # --- OPPONENT'S PLATFORM (Top-Right) ---
        opp_plat_x = arena_x + 580
        opp_plat_y = arena_y + 110
        draw.ellipse([opp_plat_x, opp_plat_y + 140, opp_plat_x + 420, opp_plat_y + 240], fill=(55, 65, 80), outline=(85, 100, 125), width=3)
        
        # Opponent Pokémon HUD Box
        opp_name = turn_data.get("opponent", "Charizard").upper()
        draw.rectangle([opp_plat_x - 140, opp_plat_y, opp_plat_x + 280, opp_plat_y + 110], fill=(20, 25, 34), outline=(80, 95, 115), width=2)
        draw.text((opp_plat_x - 120, opp_plat_y + 15), f"Lv. {65 if 'CHAR' in opp_name else 61}  {opp_name}", font=self.name_font, fill=(255, 255, 255))
        
        # Opponent HP Bar
        opp_hp = turn_data.get("opp_result_hp", 0)
        opp_max = turn_data.get("opp_max_hp", 204)
        self.draw_hp_bar(draw, opp_plat_x - 120, opp_plat_y + 55, 360, 18, opp_hp, opp_max)
        draw.text((opp_plat_x - 120, opp_plat_y + 80), f"HP: {opp_hp} / {opp_max}", font=self.hp_font, fill=(180, 190, 210))

        # Opponent Sprite Card (Stylized Pokémon Silhouette / Badge)
        draw.rectangle([opp_plat_x + 130, opp_plat_y + 70, opp_plat_x + 310, opp_plat_y + 210], fill=(45, 55, 72), outline=(100, 120, 150), width=3)
        draw.text((opp_plat_x + 150, opp_plat_y + 120), opp_name[:9], font=self.title_font, fill=(255, 215, 0))

        # --- MAGIKARP'S PLATFORM (Bottom-Left) ---
        mag_plat_x = arena_x + 80
        mag_plat_y = arena_y + 440
        draw.ellipse([mag_plat_x, mag_plat_y + 180, mag_plat_x + 480, mag_plat_y + 300], fill=(55, 65, 80), outline=(85, 100, 125), width=3)

        # Magikarp Sprite Card with Glowing 1 HP Gold Aura!
        draw.rectangle([mag_plat_x + 110, mag_plat_y + 100, mag_plat_x + 330, mag_plat_y + 260], fill=(60, 35, 20), outline=(255, 215, 0), width=4)
        draw.text((mag_plat_x + 135, mag_plat_y + 155), "MAGIKARP", font=self.title_font, fill=(255, 140, 0))

        # Magikarp HUD Box
        draw.rectangle([mag_plat_x + 360, mag_plat_y + 120, mag_plat_x + 780, mag_plat_y + 240], fill=(20, 25, 34), outline=(218, 165, 32), width=2)
        draw.text((mag_plat_x + 380, mag_plat_y + 135), "Lv. 100  MAGIKARP (Solo Run)", font=self.name_font, fill=(255, 215, 0))
        
        # Magikarp 1 HP Bar (Pulsing Red)
        mag_hp = turn_data.get("magikarp_result_hp", 1)
        mag_max = turn_data.get("magikarp_max_hp", 204)
        self.draw_hp_bar(draw, mag_plat_x + 380, mag_plat_y + 175, 360, 18, mag_hp, mag_max)
        draw.text((mag_plat_x + 380, mag_plat_y + 202), f"HP: {mag_hp} / {mag_max}  (SURVIVAL AURA ACTIVE!)", font=self.hp_font, fill=(235, 65, 65) if mag_hp == 1 else (180, 240, 180))

        # --- DYNAMIC TACTICAL ATTACK ARROW & POPUPS ---
        # Draw attack trajectory
        if "Magikarp uses" in turn_data.get("active_action", ""):
            # Magikarp attacks Opponent
            self.draw_arrow(draw, (mag_plat_x + 330, mag_plat_y + 140), (opp_plat_x + 130, opp_plat_y + 150), color=(235, 50, 50), width=14)
            # Impact Sticker
            draw.rectangle([arena_x + 480, arena_y + 260, arena_x + 840, arena_y + 330], fill=(220, 20, 60), outline=(255, 255, 255), width=3)
            draw.text((arena_x + 500, arena_y + 272), "!! CRITICAL HIT - 1HKO !!", font=self.crit_font, fill=(255, 255, 255))
        elif "Blue" in turn_data.get("active_action", "") and "uses" in turn_data.get("active_action", ""):
            # Opponent attacks Magikarp
            self.draw_arrow(draw, (opp_plat_x + 130, opp_plat_y + 150), (mag_plat_x + 330, mag_plat_y + 140), color=(0, 200, 255), width=14)
            # Focus sash sticker
            draw.rectangle([arena_x + 360, arena_y + 400, arena_x + 760, arena_y + 465], fill=(218, 165, 32), outline=(255, 255, 255), width=3)
            draw.text((arena_x + 380, arena_y + 412), "FOCUS SASH ACTIVATED! (1 HP)", font=self.crit_font, fill=(0, 0, 0))

        # -------------------------------------------------------------
        # 4. BOTTOM SUBTITLE & VOICE BANNER
        # -------------------------------------------------------------
        sub_y = 910
        sub_h = 145
        draw.rectangle([40, sub_y, self.width - 40, sub_y + sub_h], fill=(14, 17, 22), outline=(50, 60, 75), width=2)
        
        # Speaker Pill
        pill_col = (235, 60, 60) if active_speaker == "Red" else (0, 200, 255)
        draw.rectangle([60, sub_y + 15, 260, sub_y + 50], fill=pill_col)
        speaker_title = "TRAINER RED (AI)" if active_speaker == "Red" else "CHAMPION BLUE"
        draw.text((75, sub_y + 20), speaker_title, font=self.sub_bold, fill=(0, 0, 0))

        # Subtitle Text
        draw.text((60, sub_y + 65), f"\"{subtitle}\"", font=self.sub_font, fill=(255, 255, 255))

        return img
