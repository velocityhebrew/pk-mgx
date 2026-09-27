import random

# Authentic Pokémon Gen 3 / FireRed battle simulation & damage engine
# Challenge: AI Magikarp Solo Run vs Champion Blue's Full Team (Level 60-65)

CHAMPION_BLUE_TEAM = [
    {
        "name": "Pidgeot",
        "level": 61,
        "type": "Flying/Normal",
        "max_hp": 195,
        "hp": 195,
        "speed": 138,
        "moves": ["Aerial Ace", "FeatherDance", "Whirlwind", "Wing Attack"]
    },
    {
        "name": "Alakazam",
        "level": 60,
        "type": "Psychic",
        "max_hp": 158,
        "hp": 158,
        "speed": 172,
        "moves": ["Psychic", "Shadow Ball", "Recover", "Reflect"]
    },
    {
        "name": "Rhydon",
        "level": 61,
        "type": "Ground/Rock",
        "max_hp": 225,
        "hp": 225,
        "speed": 75,
        "moves": ["Earthquake", "Rock Tomb", "Megahorn", "Scary Face"]
    },
    {
        "name": "Exeggutor",
        "level": 63,
        "type": "Grass/Psychic",
        "max_hp": 218,
        "hp": 218,
        "speed": 95,
        "moves": ["Giga Drain", "Egg Bomb", "Sleep Powder", "Light Screen"]
    },
    {
        "name": "Gyarados",
        "level": 63,
        "type": "Water/Flying",
        "max_hp": 219,
        "hp": 219,
        "speed": 132,
        "moves": ["Hydro Pump", "Dragon Rage", "Bite", "Thrash"]
    },
    {
        "name": "Charizard",
        "level": 65,
        "type": "Fire/Flying",
        "max_hp": 204,
        "hp": 204,
        "speed": 158,
        "moves": ["Fire Blast", "Wing Attack", "Slash", "Flamethrower"]
    }
]

# Curated turn-by-turn battle script for the viral Magikarp Challenge (10-12 minutes)
# Magikarp: Level 100, Jolly Nature (+Speed), 252 Atk / 252 Speed EVs (Speed: 284, Atk: 119)
# Item: Focus Sash (Guarantees surviving any lethal attack with exactly 1 HP!)
# At 1 HP, Flail hits maximum Base Power of 200!

BATTLE_TURNS = [
    {
        "turn": 0,
        "opponent": "Pidgeot",
        "opp_hp": 195,
        "opp_max_hp": 195,
        "magikarp_hp": 204,
        "magikarp_max_hp": 204,
        "active_action": "CHALLENGE START: AI Magikarp vs Champion Blue!",
        "damage_dealt": 0,
        "magikarp_result_hp": 204,
        "opp_result_hp": 195,
        "strategy": "OPENING SETUP: Level 100 Magikarp Focus Sash Solo Challenge",
        "red_dialogue": "Welcome to the ultimate Pokémon AI challenge! Today, our algorithmic simulation attempts the mathematically impossible: defeating Champion Blue's full Indigo Plateau squad using only a single Magikarp! With maximum speed investment, a Focus Sash, and the raw multiplier of 200 base power Flail, let the battle begin!",
        "blue_dialogue": "Is this a joke, Red?! You stepped into the Pokémon League finals with a worthless splashing fish?! My Champion team will fry your carp into lunch on turn one! Let's see what you've got!"
    },
    {
        "turn": 1,
        "opponent": "Pidgeot",
        "opp_hp": 195,
        "opp_max_hp": 195,
        "magikarp_hp": 204,
        "magikarp_max_hp": 204,
        "active_action": "Blue's Pidgeot uses Aerial Ace!",
        "damage_dealt": 203,
        "magikarp_result_hp": 1,
        "opp_result_hp": 195,
        "strategy": "SURVIVAL TACTIC: Focus Sash Endure (1 HP Strategy)",
        "red_dialogue": "Turn 1 begins against Champion Blue's lead Pidgeot! Aerial Ace connects for massive damage, but Magikarp's Focus Sash activates! We endure the lethal blow with exactly 1 HP! The trap is sprung!",
        "blue_dialogue": "Haha! Look at that useless fish hanging on by a single thread! One more scratch and this pathetic challenge is over!"
    },
    {
        "turn": 2,
        "opponent": "Pidgeot",
        "opp_hp": 195,
        "opp_max_hp": 195,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Magikarp uses Flail! CRITICAL HIT! 200 Base Power!",
        "damage_dealt": 212,
        "magikarp_result_hp": 1,
        "opp_result_hp": 0,
        "strategy": "DAMAGE CALCULATION: Flail reaches Maximum 200 Base Power",
        "red_dialogue": "Now witness the mathematical power of Flail! At less than 4% HP, Flail scales to an absurd 200 Base Power—stronger than Explosion! Critical Hit! Pidgeot is instantly wiped out in a single blow!",
        "blue_dialogue": "WHAT?! Did a Magikarp just one-shot my level 61 Pidgeot in one hit?! That is scientifically impossible!"
    },
    {
        "turn": 3,
        "opponent": "Alakazam",
        "opp_hp": 158,
        "opp_max_hp": 158,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Blue sends out Alakazam! Speed tier check!",
        "damage_dealt": 0,
        "magikarp_result_hp": 1,
        "opp_result_hp": 158,
        "strategy": "SPEED TIER CALCULATION: 284 Speed vs 172 Speed",
        "red_dialogue": "Blue sends out his fastest weapon, Alakazam! But our Level 100 Jolly Magikarp boasts 284 Speed, completely outclassing Alakazam's 172 Speed! We retain turn priority!",
        "blue_dialogue": "Alakazam, destroy that slippery carp before it moves! Use Psychic and end this madness!"
    },
    {
        "turn": 4,
        "opponent": "Alakazam",
        "opp_hp": 158,
        "opp_max_hp": 158,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Magikarp uses Flail! Direct 1-Hit KO!",
        "damage_dealt": 240,
        "magikarp_result_hp": 1,
        "opp_result_hp": 0,
        "strategy": "PHYSICAL FRAILTY EXPLOIT: Attacking Alakazam's Base 45 Defense",
        "red_dialogue": "Magikarp strikes first with 200-power Flail! Alakazam's fragile 45 physical defense folds instantly under the kinetic impact! Alakazam faints without landing a single move!",
        "blue_dialogue": "No! My Alakazam didn't even get to cast a spell! What kind of demonic mutant fish is this?!"
    },
    {
        "turn": 5,
        "opponent": "Rhydon",
        "opp_hp": 225,
        "opp_max_hp": 225,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Blue sends out Rhydon! The Physical Wall!",
        "damage_dealt": 0,
        "magikarp_result_hp": 1,
        "opp_result_hp": 225,
        "strategy": "TYPE OVERRIDE: Physical Wall vs STAB Water Shift",
        "red_dialogue": "Blue sends out Rhydon, sporting a massive 120 base defense. Normal-type Flail is resisted by Rock typing, so our algorithm switches tactical profiles!",
        "blue_dialogue": "Try flailing against solid granite, Red! Rhydon's rock armor will shatter that puny fish into scales!"
    },
    {
        "turn": 6,
        "opponent": "Rhydon",
        "opp_hp": 225,
        "opp_max_hp": 225,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Magikarp uses Hydro Pump! 4X SUPER EFFECTIVE!",
        "damage_dealt": 288,
        "magikarp_result_hp": 1,
        "opp_result_hp": 0,
        "strategy": "ELEMENTAL EXPLOITATION: 4x Quad-Weakness (Water vs Ground/Rock)",
        "red_dialogue": "Predictable! Rhydon suffers a fatal 4x quad-weakness to Water! Magikarp unleashes a torrent Hydro Pump! A devastating 4-times super-effective strike washes Rhydon away!",
        "blue_dialogue": "A MAGIKARP THAT KNOWS HYDRO PUMP?! ARE YOU KIDDING ME?! Rhydon, get up! GET UP!"
    },
    {
        "turn": 7,
        "opponent": "Exeggutor",
        "opp_hp": 218,
        "opp_max_hp": 218,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Blue sends out Exeggutor! Grass/Psychic typing!",
        "damage_dealt": 0,
        "magikarp_result_hp": 1,
        "opp_result_hp": 218,
        "strategy": "NEUTRAL DAMAGE CALCULATION: Flail 200 BP vs Grass/Psychic",
        "red_dialogue": "Blue calls upon Exeggutor. Water is resisted, but Normal-type Flail hits for complete neutral damage. Our damage calculator shows a 94% roll to 1-shot!",
        "blue_dialogue": "You won't break through Exeggutor's psychic barriers! One Giga Drain and your fish heals my team!"
    },
    {
        "turn": 8,
        "opponent": "Exeggutor",
        "opp_hp": 218,
        "opp_max_hp": 218,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Magikarp uses Flail! CRITICAL HIT! Massive impact!",
        "damage_dealt": 224,
        "magikarp_result_hp": 1,
        "opp_result_hp": 0,
        "strategy": "DAMAGE ROLL EXECUTION: Max Power Overcomes Bulk",
        "red_dialogue": "Magikarp accelerates across the stadium! Flail connects with bone-shattering force! High damage roll confirmed—Exeggutor crashes to the turf! Four down, two to go!",
        "blue_dialogue": "Four of my Pokémon wiped out by a single fish with 1 HP remaining?! This has to be a nightmare!"
    },
    {
        "turn": 9,
        "opponent": "Gyarados",
        "opp_hp": 219,
        "opp_max_hp": 219,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Blue sends out Gyarados! The Evolved Dragon!",
        "damage_dealt": 0,
        "magikarp_result_hp": 1,
        "opp_result_hp": 219,
        "strategy": "SYMBOLIC CLASH: The Un-evolved Magikarp vs The Mighty Gyarados",
        "red_dialogue": "The ultimate symbolic showdown! Gyarados, the ferocious terror of the seas, faces its own un-evolved ancestor! Intimidate drops our attack by one stage, but our calculations account for the difference!",
        "blue_dialogue": "Gyarados, show this miserable carp what true evolution looks like! Tear it to shreds with Dragon Rage!"
    },
    {
        "turn": 10,
        "opponent": "Gyarados",
        "opp_hp": 219,
        "opp_max_hp": 219,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Magikarp uses Flail! Maximum effort strike!",
        "damage_dealt": 228,
        "magikarp_result_hp": 1,
        "opp_result_hp": 0,
        "strategy": "INTIMIDATE OVERCOME: Level 100 Flail Overpowers Intimidate",
        "red_dialogue": "Even at minus-one attack, a 200-power Flail backed by Level 100 stats hits like an orbital strike! Direct hit on Gyarados's crest! The sea dragon topples into the water!",
        "blue_dialogue": "GYARADOS! NO! How can an un-evolved Magikarp defeat its own evolved form?! It makes no sense!"
    },
    {
        "turn": 11,
        "opponent": "Charizard",
        "opp_hp": 204,
        "opp_max_hp": 204,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Blue sends out his final ace: Level 65 CHARIZARD!",
        "damage_dealt": 0,
        "magikarp_result_hp": 1,
        "opp_result_hp": 204,
        "strategy": "THE CLIMAX: 1 HP Magikarp vs Blue's Final Ace",
        "red_dialogue": "Champion Blue is down to his final Pokémon: Level 65 Charizard! The flames of Indigo Plateau burn bright, but Magikarp stands on 1 solitary hit point, untouched and undefeated!",
        "blue_dialogue": "This ends right now, Red! Charizard, incinerate this stadium! Turn this fish into ashes with Flamethrower!"
    },
    {
        "turn": 12,
        "opponent": "Charizard",
        "opp_hp": 204,
        "opp_max_hp": 204,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "Magikarp uses Flail! FINAL CHAMPIONSHIP STRIKE!",
        "damage_dealt": 236,
        "magikarp_result_hp": 1,
        "opp_result_hp": 0,
        "strategy": "CHAMPIONSHIP VICTORY: The Immortal Magikarp Solo Sweep Complete",
        "red_dialogue": "Magikarp leaps through the flames with blinding speed! The ultimate Flail connects! Charizard is blown clean across the arena! CHARIZARD HAS FAINTED! THE MAGIKARP SOLO RUN IS COMPLETE! WE ARE THE NEW POKÉMON CHAMPION!",
        "blue_dialogue": "I... I lost? My entire championship team... destroyed by a single Magikarp?! This is the most humiliating defeat in Pokémon League history!"
    },
    {
        "turn": 13,
        "opponent": "Charizard",
        "opp_hp": 0,
        "opp_max_hp": 204,
        "magikarp_hp": 1,
        "magikarp_max_hp": 204,
        "active_action": "VICTORY: Magikarp swept Champion Blue's 6 Pokemon!",
        "damage_dealt": 0,
        "magikarp_result_hp": 1,
        "opp_result_hp": 0,
        "strategy": "VICTORY ANALYSIS: 100% Win Rate Solo Challenge Run",
        "red_dialogue": "And there you have it, folks! Against every mathematical probability, Magikarp sweeps all six of Blue's Pokémon without taking a single faint! Flail at 1 HP delivered unstoppable devastation. Subscribe for more daily AI challenge runs, and check our playlist for every epic battle!",
        "blue_dialogue": "I refuse to believe this! An AI equipped with a single fish just humiliated the entire Pokémon League! You haven't seen the last of me, Red... I will demand a rematch!"
    }
]

def get_battle_turns():
    """Returns the complete sequence of battle turns for the challenge run."""
    return BATTLE_TURNS

