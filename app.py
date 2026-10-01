"""
KalaSetu (ಕಲಾಸೇತು / कलासेतु)
"See the art. Understand the story. Connect with the artist."

ACM x MLH Hackathon — Track: Art Beyond Boundaries
Built by: Gagan Naik & GaneshPrasad
Single-file Production Application: app.py
"""

import os
import json
import base64
import io
import urllib.parse
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List

import streamlit as st
from PIL import Image
import qrcode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==============================================================================
# 1. APPLICATION CONFIGURATION & INITIALIZATION
# ==============================================================================

st.set_page_config(
    page_title="KalaSetu | Digital Cultural Companion",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent.resolve()
PUBLIC_APP_URL = os.environ.get("KALASETU_PUBLIC_URL", "http://localhost:8501").rstrip("/")

# Explicit mapping of the 4 supplied dataset assets (2 Bharatanatyam, 2 Yakshagana)
IMAGE_REGISTRY = {
    "BHARATANATYAM_1": {
        "path": BASE_DIR / "bharatanatyam1.jpeg",
        "title": "Bharatanatyam Sample 1: Solo Classical Form",
        "art_form": "Bharatanatyam",
        "tradition": "Tamil Nadu Temple Heritage",
        "category": "Solo Classical Dance & Mudra Anatomy",
        "caption": "Solo dancer in seated Muzhumandi pose with Shikhara Hasta, pleated Kanchipuram silk, temple jewelry, and Alta.",
        "default_episode": "Nataraja Vandana",
        "hallmarks": "Deep Muzhumandi posture, Shikhara mudra, Kanchipuram fan pleats, Kempu temple jewelry, red Alta."
    },
    "BHARATANATYAM_2": {
        "path": BASE_DIR / "bharatanatyam2.jpeg",
        "title": "Bharatanatyam Sample 2: Stage Ensemble Form",
        "art_form": "Bharatanatyam",
        "tradition": "Tamil Nadu Classical Tradition",
        "category": "Stage Theatrics & Ensemble Choreography",
        "caption": "Six-performer synchronized ensemble under dramatic stage lighting demonstrating classic Aramandi diamond posture.",
        "default_episode": "Navarasa Varnam",
        "hallmarks": "Synchronized Aramandi postures, dynamic diagonal stage formations, dramatic lighting, and pleated fans."
    },
    "YAKSHAGANA_1": {
        "path": BASE_DIR / "yakshagana1.jpeg",
        "title": "Yakshagana Sample 1: Heroic Raja Vesha",
        "art_form": "Yakshagana",
        "tradition": "Coastal Karnataka (Badagutittu / Tenkutittu)",
        "category": "Traditional Theatrical Vesha & Facial Mukhavarnike",
        "caption": "Heroic male character in dynamic Mandai squat, adorned with towering Kedage-mandale Pagadi, Vaishnava tilak, and dagale chest ornaments.",
        "default_episode": "Devi Mahatme",
        "hallmarks": "Martial Mandai squat, towering Kedage-mandale Pagadi crown, Vaishnavite Urdhva-Pundra tilak, tiered flared skirt."
    },
    "YAKSHAGANA_2": {
        "path": BASE_DIR / "yakshagana2.jpeg",
        "title": "Yakshagana Sample 2: Royal Costume & Craft Detail",
        "art_form": "Yakshagana",
        "tradition": "Coastal Karnataka Theatrical Craftsmanship",
        "category": "Costume Craft, Bhujakeerthi & Mukhavarnike Anatomy",
        "caption": "Detail study of embroidered epaulettes (bhujakeerthi), wrist kadagas, multi-tiered flared skirt, and sacred Urdhva-pundra markings.",
        "default_episode": "Mahishasura Mardini",
        "hallmarks": "Embroidered Bhujakeerthi epaulettes, Kadaga wristbands, mirror medallions, tiered ruffles, eye contours."
    }
}

# Backward-compatible aliases
IMAGE_REGISTRY["IMAGE_SET_1"] = IMAGE_REGISTRY["BHARATANATYAM_1"]
IMAGE_REGISTRY["IMAGE_SET_2"] = IMAGE_REGISTRY["BHARATANATYAM_2"]
IMAGE_REGISTRY["IMAGE_SET_3"] = IMAGE_REGISTRY["YAKSHAGANA_1"]
IMAGE_REGISTRY["IMAGE_SET_4"] = IMAGE_REGISTRY["YAKSHAGANA_2"]


# ==============================================================================
# 2. MASTER CULTURAL KNOWLEDGE BASE (Source of Truth)
# ==============================================================================

MASTER_KNOWLEDGE_BASE = {
    "Yakshagana": {
        "origin_region": "Coastal Karnataka (Udupi, Dakshina Kannada, Uttara Kannada, and Kasaragod)",
        "tradition_overview": (
            "Yakshagana is a vibrant, centuries-old traditional theatrical art form that synthesizes dance, "
            "dialogue, high-energy music, elaborate costumes, and ornate facial makeup (Mukhavarnike). "
            "Traditionally staged through the night in open fields (Rangasthala), it enacts mythological episodes "
            "(Prasangas) from the Mahabharata, Ramayana, and Puranas."
        ),
        "schools_and_styles": {
            "Badagutittu": (
                "The northern tradition prevalent in Uttara Kannada and Udupi. Characterized by lighter, high-energy "
                "acrobatic steps, rapid pirouettes (Giri), winged crowns (Kireeta), and the sharp, piercing timbre of the Chande drum."
            ),
            "Tenkutittu": (
                "The southern tradition prevalent in Dakshina Kannada and Kasaragod. Characterized by prominent circular "
                "turban-style headgear (Mundassu) with black-and-gold ribbons, deep martial footwork, and subtle Kathakali stylizations."
            )
        },
        "orchestra_and_music": {
            "Bhagavata": "The lead singer, director, and narrator who controls the narrative pace with cymbals (Tala).",
            "Chande": "A loud, high-pitched cylindrical percussion drum played with slender cane sticks, announcing dramatic entries and battle sequences.",
            "Maddale": "A resonant double-headed hand drum providing foundational acoustic rhythm.",
            "Tala": "Bronze hand cymbals keeping the temporal meter (Kala)."
        },
        "character_types": {
            "Raja_Vesha": (
                "Heroic, noble, and royal male roles (such as Rama, Arjuna, Krishna, and virtuous kings). "
                "Features composed, dignified Mukhavarnike (face painting) with clear Vaishnavite or Shaivite forehead marks "
                "(such as Urdhva-Pundra tilak), radiant gold crowns (Kireeta), ornamental chest sashes (Dagale / Kanti), "
                "and flared, multi-tiered pleated skirts that accentuate noble postures and stage spins."
            ),
            "Rakshasa_Demon_Vesha": (
                "Demonic and aggressive characters (such as Ravana, Mahishasura, Kumbhakarna). "
                "Features ferocious, high-contrast face painting in vermilion red and deep pitch black. "
                "Artificial white fangs (Dadhe) curve from the mouth, accompanied by Chutti—white beaded lime and rice-paste "
                "boundaries accentuating jawline contortions."
            ),
            "Stree_Vesha": (
                "Female roles (Goddess Devi/Durga, Sita, Draupadi). Depicted with graceful pleated sarees, delicate waist belts, "
                "ornate bindi, and lyrical expressiveness."
            ),
            "Hasya_Vesha": (
                "The comic jester (Kodangi / Hasya Gare) providing witty social commentary and bridging epic narratives to modern audience life."
            )
        },
        "popular_prasangas": {
            "Devi_Mahatme": "The epic triumph of Goddess Durga/Chandi over buffalo-demon Mahishasura and demon kings Shumbha and Nishumbha.",
            "Mahishasura_Mardini": "The climactic combat between the Divine Mother and Mahishasura, highlighting victory of cosmic righteousness.",
            "Karna_Parva": "The tragic battlefield valor of Karna in the Kurukshetra war.",
            "Sudhanva_Moksha": "The testing of Prince Sudhanva's unwavering devotion and truth."
        }
    },
    "Bharatanatyam": {
        "origin_region": "Tamil Nadu (with pan-Indian and global classical stature)",
        "tradition_overview": (
            "One of the oldest classical dance traditions of India, Bharatanatyam originated as a devotional temple dance "
            "(originally Sadir or Dasi Attam) in Tamil Nadu. Grounded in the Natya Shastra and Abhinaya Darpana, it embodies "
            "geometric precision, dynamic footwork, sculptural symmetry, and nuanced expressive abhinaya."
        ),
        "three_pillars": {
            "Nritta": "Pure abstract rhythmic movement without narrative, highlighting sculptural lines and complex footwork (Jathis, Adavus).",
            "Nritya": "Expressive dance communicating poetry, sentiment (Bhava, Rasa), and myth through codified mudras and facial emotion.",
            "Natya": "Dramatic theatrical storytelling combining dance, dialogue, and characterization."
        },
        "foundational_postures": {
            "Aramandi": (
                "Also known as Ayata Mandalam or Ardhamandali. The core half-squat posture where knees turn outward, "
                "pelvis lowers, heels remain firm, and the torso stays erect, forming a stable diamond geometry."
            ),
            "Muzhumandi": (
                "Full sitting squat balanced on the toes with knees spread completely outward, used in dramatic sitting Jathis and abhinaya."
            ),
            "Samapada": "Serene standing posture with feet held straight and body aligned vertically."
        },
        "costume_and_adornment": {
            "Pleated_Silk_Fan": (
                "Kanchipuram silk costume with a pleated accordion fan (Visiri) in front. As the dancer enters Aramandi, "
                "the fan dramatically fans out like a peacock tail, visually emphasizing geometric leg symmetry."
            ),
            "Temple_Jewelry": (
                "Silver dipped in gold, set with un-cut cabochon red rubies (Kempu), emeralds, and pearls. Includes the Thalai Saman "
                "(Sun & Moon headsets on hair parting), Jimikki earrings, Manga Malai (mango necklace), and Oddiyanam (sculpted gold waist belt)."
            ),
            "Ghungroo_Salangai": "Bells tied around ankles that articulate complex rhythmic foot strikes (Tattu-Nattu).",
            "Alta_Mahawar": (
                "Crimson-red vegetable dye painted on fingertips, palm centers, and foot margins to heighten visibility of hand gestures "
                "and intricate footwork from distant theatre rows."
            )
        },
        "core_repertoire": ["Alarippu", "Jatiswaram", "Shabdam", "Varnam", "Padam", "Tillana", "Mangalam"]
    },
    "mudras": {
        "overview": (
            "Hastas (mudras) are the codified sign-language vocabulary of Indian performing arts. "
            "According to the Abhinaya Darpana, they consist of 28 single-hand gestures (Asamyutta Hastas) "
            "and 24 double-hand gestures (Samyutta Hastas)."
        ),
        "asamyutta_hastas": {
            "Pataka": "Flat open hand with fingers joined and thumb bent. Denotes flag, forest, river, blessing, night, or wind.",
            "Tripataka": "Pataka hand with ring finger bent down. Denotes crown, arrow, thunderbolt, or tree.",
            "Ardhapataka": "Tripataka with little finger also bent. Denotes dagger, river bank, or horn.",
            "Mayura": "Ring fingertip touches thumb tip, other fingers held straight. Denotes peacock, neck, tilak, or creeper.",
            "Shikhara": "Fist with thumb held upright pointing upward. Denotes Lord Shiva, bow, bell, pillar, valor, or resolve.",
            "Alapadma": "Fingers separated and turned outwards like a blossoming lotus. Denotes beauty, blooming flower, or mirror.",
            "Hamsasya": "Thumb and index fingertip touch gently. Denotes swan beak, painting, tying thread, or tenderness.",
            "Katakamukha": "Thumb, index, and middle fingertips touch. Denotes picking flowers, holding pearl necklace, or drawing bowstring.",
            "Ardhachandra": "Thumb stretched perpendicular to flat palm. Denotes crescent moon, throat, or spear.",
            "Musti": "Fingers curled into tight fist with thumb over fingers. Denotes firmness, weapon grip, or wrestling.",
            "Suchi": "Index finger pointing upright, others in fist. Denotes number one, Supreme Soul, lightning, or warning.",
            "Mrigashirsha": "Thumb and little finger upright, middle three bent. Denotes deer head, calling, or cheek."
        },
        "samyutta_hastas": {
            "Anjali": "Both Pataka palms joined reverently palm-to-palm. Used for salutation to deity, guru, and audience.",
            "Kapota": "Anjali with hollowed palms. Denotes respectful acceptance and humility.",
            "Karkata": "Fingers of both hands interlocked. Denotes arrival of crowd or blowing conch.",
            "Garuda": "Ardhachandra hands interlocked at thumbs with fluttering fingers. Denotes bird in flight or vehicle of Vishnu."
        },
        "context_rule": (
            "A single static photograph captures only one millisecond of movement. Because many gestures "
            "share similar geometry in static silhouettes, exact mudra identification must always account for dynamic context."
        )
    },
    "performance_context": {
        "interpretation_principles": [
            "Visual evidence is prioritized: Only report what is visually supported in the frame.",
            "Distinguish between evidence, cultural knowledge, and informed inference.",
            "Express confidence transparently: Clarify that static photos capture single fleeting moments.",
            "Never invent names, artists, or locations not present in provided data.",
            "Audience guidance: Point out dynamic cues to watch for in subsequent scenes (drum tempo, eye movements, foot stamping)."
        ]
    }
}

# ==============================================================================
# 3. DEMO PERFORMER PROFILES & CURATED SAMPLE RESULTS
# ==============================================================================

DEMO_PERFORMERS = {
    "kateel_mela": {
        "id": "kateel_mela",
        "troupe_name": "Sri Kateel Durgaparameshwari Prasaditha Dashavatara Yakshagana Mandali",
        "badge": "DEMO PERFORMER PROFILE",
        "art_form": "Yakshagana (Tenkutittu & Badagutittu)",
        "performance_title": "Devi Mahatme — The Slaying of Mahishasura",
        "episode": "Devi Mahatme",
        "location": "Kateel / Mangalore, Coastal Karnataka",
        "contact_number": "+91 98450 XXXXX",
        "email": "booking@kateelmela.example.org",
        "website": "https://kateelmela-heritage.example.org",
        "synopsis": (
            "An all-night traditional Yakshagana Prasanga recounting the cosmic battle between Goddess Durga "
            "and the tyrannical buffalo-demon Mahishasura. The performance combines thunderous Chande beats, "
            "elaborate high-turban Mundassu headgear, ferocious red-black Mukhavarnike, and philosophical dialogues."
        ),
        "highlights": [
            "Entrance of Mahishasura with blazing torches and piercing Chande rolls",
            "Philosophical debate on dharma between the Divine Messenger and the Demon King",
            "Climactic battle choreography with high-spinning Giri pirouettes and victory dance"
        ],
        "characters": [
            {"role": "Goddess Durga / Chandi", "type": "Stree Vesha", "note": "Armed with trident and chakra, embodying divine calm and wrath."},
            {"role": "Mahishasura", "type": "Rakshasa / Kati Vesha", "note": "Ferocious red and black face paint, artificial curved fangs, massive Mundassu headgear."},
            {"role": "Devendra", "type": "Raja Vesha", "note": "Golden Kireeta, multi-colored pleated skirt, pleading for cosmic intervention."}
        ],
        "symbols_and_mudras": [
            "Chande roll announces demonic wrath",
            "Trident gesture (Trishula) wielded by the Goddess",
            "High-stepping Mandai stance signaling warrior defiance"
        ],
        "costume_notes": "Traditional hand-stitched natural fiber costumes, pith-seed Chutti borders, and gold-foiled wooden ornaments.",
        "what_to_watch": "Watch the Bhagavata's vocal cadence shifting tempo before each physical duel, and notice how the Chande player changes stick angles during sword clashes."
    },
    "nritya_kalakshetra": {
        "id": "nritya_kalakshetra",
        "troupe_name": "Nritya Kalakshetra Troupe",
        "badge": "DEMO PERFORMER PROFILE",
        "art_form": "Bharatanatyam",
        "performance_title": "Nataraja Vandana & Navarasa Varnam",
        "episode": "Varnam & Tillana",
        "location": "Mysuru / Bengaluru, Karnataka",
        "contact_number": "+91 94480 XXXXX",
        "email": "contact@nrityakalakshetra.example.org",
        "website": "https://nrityakalakshetra.example.org",
        "synopsis": (
            "A classical margam presentation exploring devotion, cosmic rhythm, and emotional nuance. "
            "Features the central piece (Varnam) alternating between exhilarating rhythmic Jathis in Aramandi "
            "and subtle facial abhinaya expressing devotion and longing."
        ),
        "highlights": [
            "Invocation to Lord Nataraja with sculptural Ananda Tandava poses",
            "Complex 45-minute Varnam demonstrating intricate footwork synchronization",
            "Joyful Tillana finale celebrating pure geometric Nritta"
        ],
        "characters": [
            {"role": "Lead Dancer (Nayika)", "type": "Classical Soloist", "note": "Expressing nine distinct emotions (Navarasa) through eye movements and mudras."},
            {"role": "Ensemble Chorus", "type": "Soprano & Dancers", "note": "Synchronized Aramandi lines and sculptural diamond formations."}
        ],
        "symbols_and_mudras": [
            "Shikhara Mudra (representing Lord Shiva and resolve)",
            "Alapadma Mudra (blooming lotus of divine consciousness)",
            "Aramandi diamond posture symbolizing grounded cosmic stability"
        ],
        "costume_notes": "Authentic Kanchipuram silk costumes with pleated fan borders, handcrafted Kempu stone temple jewelry, and ankle Salangai.",
        "what_to_watch": "Notice how the front pleated fan (Visiri) opens and closes precisely with each Aramandi dip, and observe the rhythmic synergy with the Nattuvanar's cymbals."
    }
}

DEMO_SCENE_ANALYSES = {
    "IMAGE_SET_1": {
        "art_form": "Bharatanatyam",
        "regional_tradition": "Tamil Nadu Temple Heritage (Pan-Indian Classical)",
        "confidence": 94,
        "confidence_note": "Very High — Unequivocal classical Bharatanatyam costume, Muzhumandi posture, Kempu temple jewelry, and Shikhara mudra.",
        "visual_evidence": [
            "Dancer seated in full deep Muzhumandi posture on stage with knees spread completely outward",
            "Left hand held firmly at chest level in Shikhara Hasta (upright thumb fist) with crossed arm positioning",
            "Two-tone black and vibrant saffron pleated silk costume with gold zari borders",
            "Full traditional temple jewelry set: Manga Malai, Oddiyanam belt, vanki armlets, and forehead tripundra tilak",
            "Fingertips tinged with red Alta (Mahawar) dye"
        ],
        "breakdown": {
            "Costume": "Two-tone black and radiant saffron-gold Kanchipuram silk costume with layered pleated fan visible at the base.",
            "Makeup": "Elongated kajal eyeliner accentuating expressive eyes, red bindi with white tripundra markings on forehead.",
            "Mudra": "Shikhara Hasta (single hand fist with upright thumb) supported by crossed arm stance; Alta dye accentuating finger contours.",
            "Pose": "Muzhumandi (complete sitting squat with knees aligned horizontally), demonstrating exceptional core stability and flexibility.",
            "Role": "Classical male soloist enacting devotional surrender or character representation (often associated with Lord Shiva or Krishna)."
        },
        "mudra_detection": {
            "detected": True,
            "name": "Shikhara Hasta (शिखर हस्त)",
            "meaning": "Signifies Lord Shiva, the divine bow, hero's armor, pillar, or steadfast determination.",
            "visual_clue": "Closed fist with the thumb held firmly upright at chest level.",
            "confidence": "High (Mudra geometry and hand placement align with Abhinaya Darpana canons)."
        },
        "story": (
            "In this stage moment, the dancer is executing a dramatic sitting Jathi or an abhinaya stanza from a Nataraja Vandana or Varnam. "
            "The seated Muzhumandi brings the performer closer to the stage earth, transitioning from high-energy footwork into a focused, "
            "sculptural depiction of divine majesty or solemn vow."
        ),
        "cultural_significance": (
            "Bharatanatyam originated as Sadir Natyam in the grand temples of Tamil Nadu. Every component—from the geometry of the squat "
            "to the red Alta on the hands—is designed to transform the dancer's body into an architectural temple carving coming to life."
        ),
        "what_to_watch_next": [
            "Watch for the explosive rise from Muzhumandi back to standing Aramandi in sync with the Mridangam drum stroke",
            "Observe the shift in facial gaze (Drishti Bheda) matching where the hand moves next",
            "Listen for the crisp chime of ankle bells (Salangai) marking the upcoming Teerumanam cadence"
        ],
        "context_note": "Identified with high confidence from classical visual canons. Specific song lyrics or episodic name should be confirmed from the performance brochure."
    },
    "IMAGE_SET_2": {
        "art_form": "Bharatanatyam",
        "regional_tradition": "Tamil Nadu Classical Tradition (Contemporary Ensemble Margam)",
        "confidence": 92,
        "confidence_note": "Very High — Six-dancer ensemble executing synchronized classical Adavus in Aramandi under theatrical stage lighting.",
        "visual_evidence": [
            "Six performers (male and female) arrayed across the stage in dynamic diagonal formation",
            "Deep synchronized Aramandi (half-squat) postures with knees bent outwards",
            "Coordinated silk costumes in vermilion red, saffron, and peacock green with accordion-pleated fans",
            "Traditional headgear (Veni hair ornaments, Thalai Saman) and temple necklaces",
            "Raised arms with extended hand gestures portraying divine celestial movement"
        ],
        "breakdown": {
            "Costume": "Coordinated silk costumes in rich jewel tones with pleated fans (Visiri) fanning out between the knees in Aramandi.",
            "Makeup": "High-contrast classical stage makeup designed for auditorium visibility, including red Alta on fingers and feet.",
            "Mudra": "Dynamic outstretched Hastas (resembling Pataka and Tripataka extensions) channeling narrative momentum.",
            "Pose": "Aramandi and lunging Mandalam steps creating geometric harmony across the stage width.",
            "Role": "Ensemble choreography portraying cosmic order, temple sculpture tableaux, or group devotional narrative."
        },
        "mudra_detection": {
            "detected": True,
            "name": "Pataka / Tripataka Extensions",
            "meaning": "Depicting celestial flight, expansive horizons, or divine aura.",
            "visual_clue": "Outstretched arms with angled hands reflecting synchronized choreography.",
            "confidence": "Moderate to High (Dynamic stage motion captures fluid gesture transitions)."
        },
        "story": (
            "An ensemble Varnam or Tillana where dancers interpret poetic verses through synchronized polyphony. "
            "While traditional Bharatanatyam was historically a solo art form, modern choreographers unite multiple dancers "
            "to amplify mythological epics and architectural temple friezes."
        ),
        "cultural_significance": (
            "Showcases the evolution of Indian classical dance: preserving sacred temple repertoire while creating "
            "contemporary group spatial architecture that captivates large modern audiences."
        ),
        "what_to_watch_next": [
            "Watch for rapid symmetrical ripple movements where each dancer repeats a gesture a fraction of a beat apart",
            "Listen for the vocalized Sollukattu (rhythm syllables) chanted by the Nattuvanar leading to a crescendo",
            "Observe the precise alignment of the pleated front fans as all six dancers sink simultaneously into Aramandi"
        ],
        "context_note": "Ensemble staging verified from visual evidence. Exact choreography title should be verified from troupe credentials."
    },
    "IMAGE_SET_3": {
        "art_form": "Yakshagana",
        "regional_tradition": "Coastal Karnataka (Badagutittu / Tenkutittu Heritage)",
        "confidence": 95,
        "confidence_note": "Very High — Unmistakable Yakshagana Raja/Heroic Vesha, elaborate crown-headgear (Pagadi/Kireeta), Vaishnava Mukhavarnike, and Mandai stance.",
        "visual_evidence": [
            "Performer poised in wide, grounded warrior Mandai stance with crossed wrists at chest height",
            "Majestic high headgear (Kedage-mandale Pagadi) adorned with crimson pom-poms, golden foil, mirrors, and feather crest",
            "Intricate Mukhavarnike face paint featuring bold winged kajal eyes and distinctive Vaishnavite Urdhva-Pundra tilak",
            "Multi-tiered flared pleated skirt with horizontal bands of emerald green, ivory white, and vermilion",
            "Heavily embroidered chest apron (dagale), ornate epaulettes (bhujakeerthi), and wristbands (kadaga)"
        ],
        "breakdown": {
            "Costume": "Multi-tiered flared skirt (kavacha) designed to billow during spins, accompanied by embroidered dagale chest sash and gilded shoulder ornaments.",
            "Makeup": "Mukhavarnike featuring radiant pink-white foundation, crisp Vaishnava tilak, elongated brows, and red-contoured lips.",
            "Mudra": "Crossed arms with curved palms in theatrical martial defense stance, typical of heroic protagonists.",
            "Pose": "Mandai (wide martial squat with turned-out feet), balancing weight securely on bare feet for explosive stage spins.",
            "Role": "Heroic or Divine Male Character (Raja Vesha / Purusha Vesha), such as Lord Krishna, Arjuna, Rama, or Prince Sudhanva."
        },
        "mudra_detection": {
            "detected": True,
            "name": "Karkata / Swastika Cross Stance (Theatrical Martial Gesture)",
            "meaning": "Signifies royal dignity, readiness for combat, divine readiness, or unyielding spiritual resolve.",
            "visual_clue": "Forearms crossed across the chest with palms open outward.",
            "confidence": "High (Canonical theatrical stance in Yakshagana Rangasthala tradition)."
        },
        "story": (
            "The performer is portraying a pivotal heroic moment from an epic Prasanga such as Devi Mahatme or Karna Parva. "
            "In this sequence, the heroic figure has just completed a dynamic entrance behind the portable curtain (Tere), "
            "and is holding this majestic tableau (Nidre / Niluvu) while the Bhagavata sings his identifying introductory stanza (Oddolaga)."
        ),
        "cultural_significance": (
            "Yakshagana is the living soul of coastal Karnataka folk-theatre. It bridges divine mythology with heroic folklore. "
            "The towering headgear visually transforms the mortal actor into a larger-than-life celestial warrior, visible even by torchlight."
        ),
        "what_to_watch_next": [
            "Listen for a sudden, thunderous burst from the Chande drum signaling the character's first spoken monologue",
            "Watch for rapid 360-degree knees-bent spins (Giri) that make the tiered skirt billow into a flying disc",
            "Observe the eyes and eyebrows vibrating in micro-movements to express astonishment or resolve"
        ],
        "context_note": "Visual evidence firmly establishes Yakshagana Raja Vesha. Specific hero identity depends on the particular Prasanga being performed."
    },
    "IMAGE_SET_4": {
        "art_form": "Yakshagana",
        "regional_tradition": "Coastal Karnataka Theatrical Craftsmanship",
        "confidence": 95,
        "confidence_note": "Very High — Detail study of Yakshagana royal attire, demonstrating handcrafted temple ornaments, Mukhavarnike, and dagale.",
        "visual_evidence": [
            "Detailed view of traditional Yakshagana ornaments: Bhujakeerthi (shoulder guards) and Kadaga (bracelets)",
            "Multi-colored hand-pleated skirt with scalloped ruffles in green and white",
            "Elaborate forehead Urdhva-Pundra marking indicating Vaishnavite mythological affiliation",
            "Mirror-work circular medallions on the chest breastplate reflecting ambient stage light",
            "Bare feet with ankle bells (gejje) firmly planted on the polished stage floor"
        ],
        "breakdown": {
            "Costume": "Handcrafted layered fabrics combining heavy cotton and satin with gold zari embroidery.",
            "Makeup": "Mukhavarnike applied with natural powders, highlighting the bone structure for distant visibility.",
            "Mudra": "Expressive palm positioning reinforcing theatrical dialogue and musical rhythm.",
            "Pose": "Grounded Mandai posture showing balance and endurance required for 8-hour overnight performances.",
            "Role": "Royal/Heroic character representing virtue (Dharma) resisting demonic forces."
        },
        "mudra_detection": {
            "detected": True,
            "name": "Theatrical Gesture of Resolve",
            "meaning": "Affirming righteousness and heroic readiness in the face of cosmic discord.",
            "visual_clue": "Centered hand framing at chest height with palms upright.",
            "confidence": "High."
        },
        "story": (
            "This closeup illustrates the visual grammar that allows rural audience members seated 50 meters away "
            "in an open-air village ground to immediately decode a character's morality, rank, and emotional state "
            "purely through color, crown height, and facial markings."
        ),
        "cultural_significance": (
            "Each ornament in Yakshagana is a sacred relic handcrafted by coastal artisan families across generations. "
            "The craft embodies centuries of regional heritage preserved by melas (troupes)."
        ),
        "what_to_watch_next": [
            "Watch how the mirrors on the headgear catch light during battle choreography",
            "Notice how the performer shifts weight between heels and toes to indicate emotional tension",
            "Look for the interaction between the character and the Bhagavata narrator at the stage corner"
        ],
        "context_note": "Reflects authentic coastal Karnataka Yakshagana craftsmanship."
    }
}

DEMO_SCENE_ANALYSES["BHARATANATYAM_1"] = DEMO_SCENE_ANALYSES["IMAGE_SET_1"]
DEMO_SCENE_ANALYSES["BHARATANATYAM_2"] = DEMO_SCENE_ANALYSES["IMAGE_SET_2"]
DEMO_SCENE_ANALYSES["YAKSHAGANA_1"] = DEMO_SCENE_ANALYSES["IMAGE_SET_3"]
DEMO_SCENE_ANALYSES["YAKSHAGANA_2"] = DEMO_SCENE_ANALYSES["IMAGE_SET_4"]

# ==============================================================================
# 4. EDITORIAL DESIGN SYSTEM & CUSTOM CSS
# ==============================================================================

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,700;1,400&display=swap');

:root {
    --bg-warm: #FBF8F3;
    --text-charcoal: #1C1B1A;
    --text-muted: #5C564E;
    --terracotta: #C85A32;
    --vermilion: #9E2A2B;
    --gold: #C5A059;
    --gold-light: #F4EFE6;
    --card-bg: #FFFFFF;
    --card-border: #EADBCE;
    --border-radius: 10px;
}

/* Background & Body Font */
.stApp {
    background-color: var(--bg-warm);
    color: var(--text-charcoal);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Typography Hierarchy */
h1, h2, h3, .brand-title {
    font-family: 'Cinzel', 'Playfair Display', Georgia, serif;
    letter-spacing: 0.5px;
    color: var(--vermilion);
}

p, div, label, span {
    color: var(--text-charcoal);
}

/* Editorial Brand Bar */
.brand-header {
    text-align: center;
    padding: 2.2rem 1rem 1.2rem 1rem;
    border-bottom: 2px solid var(--card-border);
    margin-bottom: 2rem;
    position: relative;
}

.brand-eyebrow {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: var(--gold);
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.brand-title {
    font-size: 2.8rem;
    font-weight: 900;
    margin: 0;
    color: var(--vermilion);
    letter-spacing: 2px;
}

.brand-tagline {
    font-size: 1.15rem;
    font-style: italic;
    font-family: 'Playfair Display', Georgia, serif;
    color: var(--text-muted);
    margin-top: 0.4rem;
}

.brand-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 1rem auto 0 auto;
    width: 140px;
}

.brand-divider span {
    color: var(--gold);
    font-size: 0.9rem;
    padding: 0 0.5rem;
}

.brand-divider::before, .brand-divider::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid var(--gold);
}

/* Editorial Cards */
.ks-card {
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--border-radius);
    padding: 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 18px rgba(50, 30, 20, 0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ks-card:hover {
    box-shadow: 0 6px 24px rgba(50, 30, 20, 0.07);
}

.ks-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid var(--card-border);
    padding-bottom: 0.5rem;
}

.ks-card-title {
    font-family: 'Cinzel', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--vermilion);
    margin: 0;
}

.ks-badge {
    background-color: var(--gold-light);
    color: var(--vermilion);
    border: 1px solid var(--gold);
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.72rem;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 1px;
}

.ks-badge-demo {
    background-color: #FFF3CD;
    color: #856404;
    border: 1px solid #FFEBAA;
}

.ks-badge-verified {
    background-color: #E8F5E9;
    color: #2E7D32;
    border: 1px solid #C8E6C9;
}

/* Visual Breakdown Grid */
.breakdown-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1.2rem 0;
}

.breakdown-item {
    background: #FAF7F2;
    border: 1px solid #EFE8DC;
    border-left: 3px solid var(--terracotta);
    padding: 0.9rem;
    border-radius: 6px;
}

.breakdown-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--gold);
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.breakdown-val {
    font-size: 0.92rem;
    color: var(--text-charcoal);
    line-height: 1.4;
}

/* Callout Box */
.ks-callout {
    background: #FFFBF5;
    border-left: 4px solid var(--gold);
    padding: 1rem 1.2rem;
    border-radius: 0 var(--border-radius) var(--border-radius) 0;
    margin: 1.2rem 0;
    border-top: 1px solid #F0E8DC;
    border-bottom: 1px solid #F0E8DC;
    border-right: 1px solid #F0E8DC;
}

/* Mobile Stage Page View */
.stage-mobile-container {
    max-width: 680px;
    margin: 0 auto;
    background: #FFFFFF;
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 2rem 1.6rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.stage-title {
    font-family: 'Cinzel', serif;
    font-size: 1.9rem;
    color: var(--vermilion);
    text-align: center;
    margin-bottom: 0.2rem;
}

.stage-subtitle {
    text-align: center;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--gold);
    margin-bottom: 1.5rem;
}

/* Tab & Button Customization */
div[data-testid="stTabs"] button {
    font-family: 'Cinzel', serif;
    font-size: 0.95rem;
    letter-spacing: 0.5px;
    font-weight: 600;
}

div.stButton > button {
    background-color: var(--vermilion);
    color: #FFFFFF !important;
    border: 1px solid #7D1F20;
    border-radius: 6px;
    padding: 0.5rem 1.4rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background-color: #832223;
    border-color: #611819;
    box-shadow: 0 4px 12px rgba(158, 42, 43, 0.25);
}

/* Disclaimer text */
.ks-disclaimer {
    font-size: 0.8rem;
    color: var(--text-muted);
    font-style: italic;
    border-top: 1px solid var(--card-border);
    padding-top: 0.8rem;
    margin-top: 1.5rem;
    text-align: center;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================================================================
# 5. STATE MANAGEMENT & GEMINI CLIENT INITIALIZATION
# ==============================================================================

if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None
if "selected_preset" not in st.session_state:
    st.session_state["selected_preset"] = "IMAGE_SET_1"
if "performance_guides" not in st.session_state:
    st.session_state["performance_guides"] = DEMO_PERFORMERS.copy()
if "last_query" not in st.session_state:
    st.session_state["last_query"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

@st.cache_resource(show_spinner=False)
def get_gemini_client():
    """Instantiate official Google Gen AI Client from backend environment variable only.
    
    The API key is NEVER exposed in the UI — it is loaded exclusively from
    the GEMINI_API_KEY environment variable set in the .env file (backend only).
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except Exception as e:
        return None

# ==============================================================================
# 6. IMAGE UTILITIES & RESIZING
# ==============================================================================

def resize_image_for_gemini(pil_img: Image.Image, max_dim: int = 1200) -> Image.Image:
    """Resize image to reduce latency while preserving fine cultural details."""
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert("RGB")
    width, height = pil_img.size
    if max(width, height) > max_dim:
        scale = max_dim / float(max(width, height))
        new_size = (int(width * scale), int(height * scale))
        pil_img = pil_img.resize(new_size, Image.Resampling.LANCZOS)
    return pil_img

def load_image_asset(image_path: Path) -> Optional[Image.Image]:
    """Safely open local authoritative image asset."""
    if image_path.exists():
        try:
            return Image.open(image_path)
        except Exception:
            return None
    return None

def generate_stage_qr(url_or_payload: str) -> Image.Image:
    """Generate high-resolution scannable QR code matching editorial palette."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=3,
    )
    qr.add_data(url_or_payload)
    qr.make(fit=True)
    return qr.make_image(fill_color="#1C1B1A", back_color="#FBF8F3").convert("RGB")

# ==============================================================================
# 7. PROMPT BUILDERS
# ==============================================================================

def build_scene_prompt(art_form_hint: str, performance_name: str) -> str:
    """Build canonical cultural interpreter prompt with strict uncertainty guards."""
    kb_snippet = json.dumps(MASTER_KNOWLEDGE_BASE, indent=2)
    return f"""You are KalaSetu, an authoritative and careful cultural interpreter for Indian performing arts.
Your mission is to connect audience members with the deep mythology, visual language, and human performers behind traditional Indian arts.

AUTHORITATIVE KALASETU MASTER KNOWLEDGE:
{kb_snippet}

USER INPUT CONTEXT:
- Suggested Art Form: {art_form_hint if art_form_hint else "Auto Detect"}
- Known Episode / Performance Name: {performance_name if performance_name else "Unknown (to be inferred with uncertainty)"}

STRICT INTERPRETATION RULES:
1. Distinguish between VISUAL EVIDENCE (what is clearly visible), CULTURAL KNOWLEDGE (from the master document), INFERENCE (reasoned connection), and UNCERTAINTY.
2. Never invent an exact character, episode, ritual, artist, temple, or historical date.
3. If an identification cannot be confirmed from a single static image alone, state that transparently.
4. If a mudra is visible, identify it ONLY if the hand shape clearly matches canonical Hastas (e.g., Shikhara, Pataka, Mayura). If ambiguous, mention plausible alternatives.
5. Provide practical guidance for the viewer on 'What to Watch For on Stage'.
6. Keep the language respectful, evocative, and beginner-accessible.

OUTPUT STRICT JSON WITH THIS SCHEMA:
{{
  "art_form": "Identified Art Form (e.g. Yakshagana or Bharatanatyam)",
  "regional_tradition": "Specific tradition (e.g. Badagutittu Coastal Karnataka, or Tamil Nadu Temple Heritage)",
  "confidence": 85,
  "confidence_note": "Concise statement on what is clear vs. what needs live performance context",
  "visual_evidence": ["Bullet 1 of visible facts", "Bullet 2"],
  "breakdown": {{
    "Costume": "Explanation of visible fabric, pleats, crown, and ornaments",
    "Makeup": "Explanation of facial paint (e.g. Mukhavarnike, Alta, eyeliner)",
    "Mudra": "Explanation of visible hand gesture and its meaning",
    "Pose": "Explanation of posture (e.g. Aramandi, Muzhumandi, Mandai)",
    "Role": "Likely role/type (e.g. Raja Vesha, Rakshasa Vesha, Classical Soloist)"
  }},
  "mudra_detection": {{
    "detected": true,
    "name": "Mudra name in Sanskrit & English",
    "meaning": "Traditional meaning and usage",
    "visual_clue": "What hand shape was observed",
    "confidence": "High / Moderate / Uncertain"
  }},
  "story": "Concise 2-3 paragraph cultural explanation of the scene and mythological context",
  "cultural_significance": "Why this scene and visual language matters in Indian heritage",
  "what_to_watch_next": [
    "Dynamic stage cue to observe next 1",
    "Dynamic stage cue to observe next 2",
    "Dynamic stage cue to observe next 3"
  ],
  "context_note": "Transparent note acknowledging AI interpretation boundaries"
}}
Return ONLY valid JSON.
"""

def build_guide_generation_prompt(artist_data: Dict[str, Any]) -> str:
    """Prompt for polishing raw performer notes into an audience stage guide."""
    return f"""You are KalaSetu's Stage Dramaturg. Transform the following artist performance submission into an elegant, audience-friendly 'KalaSetu Performance Guide'.
Do not invent facts beyond the provided submission and the verified cultural traditions of {artist_data.get('art_form')}.

SUBMITTED ARTIST DATA:
{json.dumps(artist_data, indent=2)}

OUTPUT STRICT JSON:
{{
  "synopsis": "Engaging 2-paragraph synopsis of tonight's narrative for an audience member waiting in their seat",
  "highlights": ["Key highlight 1", "Key highlight 2", "Key highlight 3"],
  "characters": [
    {{"role": "Character Name", "type": "Costume/Role Type", "note": "What the audience will see"}}
  ],
  "symbols_and_mudras": ["Symbol 1 meaning", "Symbol 2 meaning"],
  "what_to_watch": "Specific audio-visual cues the audience should notice during the performance"
}}
Return ONLY valid JSON.
"""

# ==============================================================================
# 8. AI ENGINE: VISION & GROUNDED SEARCH
# ==============================================================================

def analyze_scene_image(
    client,
    pil_image: Image.Image,
    art_form_hint: str,
    performance_name: str,
    preset_key: Optional[str] = None
) -> Tuple[Optional[Dict[str, Any]], bool, str]:
    """
    Execute AI analysis with Gemini 2.5 Flash, falling back gracefully to
    curated demo analysis if API key is absent or offline.
    """
    if client is None:
        # Fallback to curated demo mode
        sample = DEMO_SCENE_ANALYSES.get(preset_key, DEMO_SCENE_ANALYSES["IMAGE_SET_1"])
        return sample, True, "Demo Mode active (Offline or API Key not configured). Showing verified KalaSetu analysis."

    try:
        from google.genai import types
        prepared_img = resize_image_for_gemini(pil_image)
        prompt = build_scene_prompt(art_form_hint, performance_name)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, prepared_img],
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json"
            )
        )
        
        raw_text = response.text.strip()
        data = json.loads(raw_text)
        return data, False, ""
    except Exception as e:
        # Graceful fallback on network/quota failure
        sample = DEMO_SCENE_ANALYSES.get(preset_key, DEMO_SCENE_ANALYSES["IMAGE_SET_1"])
        return sample, True, f"Live Gemini request encountered an issue ({str(e)}). Switched gracefully to verified Demo Mode."

def ask_cultural_copilot(
    client,
    question: str
) -> Tuple[str, List[Dict[str, str]], bool]:
    """
    Query Cultural AI with Google Search Grounding when available,
    incorporating KalaSetu Master Knowledge.
    """
    if client is None:
        # Offline curated answer fallback
        q_lower = question.lower()
        if "badagutittu" in q_lower or "tenkutittu" in q_lower:
            ans = (
                "**Badagutittu** (Northern style, Uttara Kannada/Udupi) emphasizes lighter, acrobatic steps, "
                "winged crowns (Kireeta), and high-pitched Chande rhythms. \n\n"
                "**Tenkutittu** (Southern style, Dakshina Kannada/Kasaragod) is distinguished by circular black-and-gold "
                "turban headgear (Mundassu), grounded martial footwork, and subtle Kathakali stylings."
            )
            return ans, [{"title": "KalaSetu Master Knowledge Base", "url": "#curated"}], True
        elif "aramandi" in q_lower:
            ans = (
                "**Aramandi** (Ardhamandali / Ayata) is the cornerstone posture of Bharatanatyam. "
                "The dancer lowers the torso with knees pointed outwards, forming a geometric diamond with the legs. "
                "It grounds the center of gravity and allows the pleated silk fan (Visiri) to open like a peacock's plumage."
            )
            return ans, [{"title": "Abhinaya Darpana & KalaSetu Master Knowledge", "url": "#curated"}], True
        elif "fangs" in q_lower or "demon" in q_lower or "makeup" in q_lower:
            ans = (
                "In Yakshagana, demonic characters (Rakshasa / Kati Vesha) wear **artificial fangs (Dadhe)** "
                "and ferocious red-and-black face paint. White lime-and-rice paste borders called **Chutti** "
                "frame the jawline to optically amplify expressions for village spectators seated in open fields."
            )
            return ans, [{"title": "KalaSetu Master Knowledge: Yakshagana Mukhavarnike", "url": "#curated"}], True
        else:
            ans = (
                f"**Cultural Interpretation for:** *{question}*\n\n"
                "Traditional Indian performing arts rely on a codified visual vocabulary where every element—from the "
                "Urdhva-Pundra tilak on a Yakshagana hero to the red Alta dye on a Bharatanatyam dancer's palms—is an "
                "intentional storytelling device designed to communicate emotional state, cosmic alignment, and character virtue."
            )
            return ans, [{"title": "KalaSetu Master Knowledge Base", "url": "#curated"}], True

    try:
        from google.genai import types
        kb_text = json.dumps(MASTER_KNOWLEDGE_BASE)
        system_instruction = (
            f"You are KalaSetu Cultural AI Copilot. Answer user questions about traditional Indian performing arts "
            f"(especially Yakshagana, Bharatanatyam, mudras, costumes, makeup, and stories). "
            f"Ground your answer primarily in this verified Master Knowledge: {kb_text}. "
            f"If using Google Search grounding, mention the context clearly and never invent facts."
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.3
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=config
        )

        answer_text = response.text or "No response generated."
        sources = []

        # Extract real grounding sources from response metadata
        if hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0]
            gm = getattr(candidate, "grounding_metadata", None)
            if gm:
                chunks = getattr(gm, "grounding_chunks", []) or []
                for chunk in chunks:
                    web = getattr(chunk, "web", None)
                    if web:
                        u = getattr(web, "uri", "")
                        t = getattr(web, "title", "")
                        if u:
                            sources.append({"title": t or u, "url": u})

        return answer_text, sources, False
    except Exception as e:
        return f"Could not complete online search ({str(e)}). Please verify API key.", [], True

# ==============================================================================
# 9. RESULT RENDERERS
# ==============================================================================

def render_scene_result_ui(result: Dict[str, Any], display_image: Image.Image, is_demo: bool, note: str):
    """Render rich two-column editorial cultural interpretation."""
    if is_demo:
        st.info(f"💡 **Demo Mode**: {note}")

    col_img, col_info = st.columns([1, 1.25], gap="large")

    with col_img:
        st.image(display_image, use_container_width=True, caption="Analyzed Performance Frame")
        st.markdown(f"""
        <div class="ks-card" style="margin-top: 1rem;">
            <div class="brand-eyebrow">Visual Evidence Recorded</div>
            <ul style="padding-left: 1.2rem; font-size: 0.9rem; margin-bottom: 0;">
                {"".join([f"<li>{ev}</li>" for ev in result.get("visual_evidence", [])])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        art_form = result.get("art_form", "Traditional Performing Art")
        region = result.get("regional_tradition", "Regional Heritage")
        conf = result.get("confidence", 85)

        st.markdown(f"""
        <div style="margin-bottom: 0.5rem;">
            <span class="ks-badge ks-badge-verified">{art_form}</span>
            <span class="ks-badge" style="margin-left: 0.5rem;">{region}</span>
            <span class="ks-badge" style="margin-left: 0.5rem;">Confidence: {conf}%</span>
        </div>
        <h2 style="margin-top: 0.5rem; margin-bottom: 0.3rem;">What You Are Looking At</h2>
        <p style="font-size: 0.88rem; color: #5C564E; margin-bottom: 1.2rem;">{result.get('confidence_note', '')}</p>
        """, unsafe_allow_html=True)

        # Breakdown Cards
        bd = result.get("breakdown", {})
        st.markdown(f"""
        <div class="breakdown-grid">
            <div class="breakdown-item">
                <div class="breakdown-label">Costume</div>
                <div class="breakdown-val">{bd.get('Costume', 'N/A')}</div>
            </div>
            <div class="breakdown-item">
                <div class="breakdown-label">Facial Makeup</div>
                <div class="breakdown-val">{bd.get('Makeup', 'N/A')}</div>
            </div>
            <div class="breakdown-item">
                <div class="breakdown-label">Mudra / Gesture</div>
                <div class="breakdown-val">{bd.get('Mudra', 'N/A')}</div>
            </div>
            <div class="breakdown-item">
                <div class="breakdown-label">Stage Posture</div>
                <div class="breakdown-val">{bd.get('Pose', 'N/A')}</div>
            </div>
            <div class="breakdown-item" style="grid-column: 1 / -1;">
                <div class="breakdown-label">Character / Role</div>
                <div class="breakdown-val">{bd.get('Role', 'N/A')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Mudra Detection Spotlight
    mudra_info = result.get("mudra_detection", {})
    if mudra_info.get("detected"):
        st.markdown(f"""
        <div class="ks-card" style="border-left: 4px solid var(--vermilion);">
            <div class="ks-card-header">
                <h3 class="ks-card-title">🖐️ Mudra Detected: {mudra_info.get('name', 'Hand Gesture')}</h3>
                <span class="ks-badge">Confidence: {mudra_info.get('confidence', 'Canonical')}</span>
            </div>
            <p style="margin-bottom: 0.4rem;"><strong>Meaning & Symbolism:</strong> {mudra_info.get('meaning', '')}</p>
            <p style="font-size: 0.9rem; color: #5C564E; margin: 0;"><strong>Visual Observation:</strong> {mudra_info.get('visual_clue', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    # Narrative & Significance Sections
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(f"""
        <div class="ks-card" style="height: 100%;">
            <div class="brand-eyebrow">The Narrative</div>
            <h3 class="ks-card-title">Story Behind the Scene</h3>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; line-height: 1.6;">{result.get('story', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="ks-card" style="height: 100%;">
            <div class="brand-eyebrow">Cultural Resonance</div>
            <h3 class="ks-card-title">Why It Matters</h3>
            <p style="margin-top: 0.8rem; font-size: 0.95rem; line-height: 1.6;">{result.get('cultural_significance', '')}</p>
        </div>
        """, unsafe_allow_html=True)

    # What to Watch For Next
    st.markdown(f"""
    <div class="ks-callout">
        <h4 style="margin: 0 0 0.5rem 0; font-family: 'Cinzel', serif; color: var(--vermilion);">
            👁️ What to Watch For on Stage
        </h4>
        <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.95rem;">
            {"".join([f"<li style='margin-bottom: 0.3rem;'>{item}</li>" for item in result.get("what_to_watch_next", [])])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Cultural Uncertainty & Trust Disclaimer
    st.markdown(f"""
    <div class="ks-disclaimer">
        ⚖️ <strong>Cultural Accuracy Note:</strong> {result.get('context_note', 'KalaSetu distinguishes visual evidence from cultural inference.')}
        AI interpretations reflect canonical visual grammars; always confirm specific troupe scripts with performers.
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 10. PUBLIC MOBILE-FIRST STAGE PAGE VIEW (?stage=...)
# ==============================================================================

def render_mobile_stage_guide(stage_id: str):
    """
    Renders the dedicated, distraction-free stage guide for audience members
    scanning the physical QR code on their mobile devices in the auditorium.
    """
    profile = st.session_state["performance_guides"].get(stage_id)
    if not profile:
        profile = DEMO_PERFORMERS["kateel_mela"]

    st.markdown('<div class="stage-mobile-container">', unsafe_allow_html=True)

    # Exit Button for Desktop Users
    if st.button("← Return to KalaSetu Main App"):
        st.query_params.clear()
        st.rerun()

    st.markdown(f"""
    <div class="stage-subtitle">KalaSetu Official Stage Guide</div>
    <h1 class="stage-title">{profile.get('performance_title')}</h1>
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <span class="ks-badge ks-badge-verified">{profile.get('art_form')}</span>
        <span class="ks-badge" style="margin-left: 0.5rem;">{profile.get('location')}</span>
        <div style="margin-top: 0.5rem; font-weight: 600; color: #1C1B1A;">Presented by: {profile.get('troupe_name')}</div>
        <div style="margin-top: 0.2rem;"><span class="ks-badge ks-badge-demo">{profile.get('badge', 'DEMO PROFILE')}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Tonight's Story
    st.markdown(f"""
    <div class="ks-card">
        <h3 class="ks-card-title">📖 Tonight's Story</h3>
        <p style="margin-top: 0.6rem; font-size: 0.95rem; line-height: 1.6;">{profile.get('synopsis')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Highlights
    st.markdown(f"""
    <div class="ks-card">
        <h3 class="ks-card-title">✨ Key Performance Highlights</h3>
        <ul style="padding-left: 1.2rem; font-size: 0.92rem; margin-top: 0.5rem;">
            {"".join([f"<li>{h}</li>" for h in profile.get('highlights', [])])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Characters on Stage
    st.markdown("""<div class="ks-card"><h3 class="ks-card-title">🎭 Characters You Will See</h3>""", unsafe_allow_html=True)
    for char in profile.get("characters", []):
        st.markdown(f"""
        <div style="padding: 0.5rem 0; border-bottom: 1px dashed #E7DFC6;">
            <strong>{char.get('role')}</strong> <span class="ks-badge" style="font-size: 0.65rem;">{char.get('type')}</span>
            <div style="font-size: 0.88rem; color: #5C564E; margin-top: 0.2rem;">{char.get('note')}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # What to Watch For
    st.markdown(f"""
    <div class="ks-callout">
        <h4 style="margin: 0 0 0.5rem 0; font-family: 'Cinzel', serif; color: var(--vermilion);">
            👁️ What to Watch For During the Show
        </h4>
        <p style="margin: 0; font-size: 0.92rem;">{profile.get('what_to_watch')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Contact & Booking
    st.markdown(f"""
    <div class="ks-card" style="text-align: center;">
        <h3 class="ks-card-title">🤝 Connect With the Artists</h3>
        <p style="font-size: 0.88rem; color: #5C564E; margin-top: 0.3rem;">Interested in inviting this troupe to your institution or festival?</p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
            <a href="tel:{profile.get('contact_number')}" style="text-decoration: none;">
                <button style="background: var(--terracotta); color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-weight: 600; cursor: pointer;">
                    📞 Call Troupe
                </button>
            </a>
            <a href="mailto:{profile.get('email')}" style="text-decoration: none;">
                <button style="background: var(--vermilion); color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-weight: 600; cursor: pointer;">
                    ✉️ Email Troupe
                </button>
            </a>
        </div>
        <div style="font-size: 0.78rem; color: #856404; margin-top: 1rem;">
            <em>Note: Contact details displayed above are for hackathon demonstration.</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 11. MAIN USER JOURNEYS
# ==============================================================================

def render_home_page():
    """Museum-grade editorial landing page."""
    st.markdown("""
    <div class="brand-header">
        <div class="brand-eyebrow">ACM x MLH Hackathon — Art Beyond Boundaries</div>
        <h1 class="brand-title">KALASETU</h1>
        <div class="brand-tagline">"See the art. Understand the story. Connect with the artist."</div>
        <div class="brand-divider"><span>✦  ॥  ✦</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Hero Intro
    c_left, c_right = st.columns([1.1, 1], gap="large")
    with c_left:
        st.markdown("""
        ### The Cultural Interpreter for Indian Performing Arts
        Traditional performances such as **Yakshagana** and **Bharatanatyam** are steeped in thousands of years 
        of mythological narrative, codified mudras, intricate facial makeup, and geometric choreographic architecture.
        
        Yet for first-time viewers and young audiences:
        - **The Story is unclear** — *Who is this character? What conflict is unfolding?*
        - **The Art is unfamiliar** — *What does this red-and-black makeup, fangs, or hand gesture mean?*
        - **Artists struggle for visibility** — *Master regional troupes remain undiscovered beyond local circles.*
        
        **KalaSetu bridges this boundary.** Simply upload a photo of a live performance or costume. 
        KalaSetu translates visual clues into the cultural story behind them.
        """)

        st.markdown("""
        <div style="display: flex; gap: 0.8rem; margin-top: 1.5rem;">
            <div class="ks-badge ks-badge-verified">01 Capture</div>
            <div class="ks-badge ks-badge-verified">02 Understand</div>
            <div class="ks-badge ks-badge-verified">03 Discover</div>
            <div class="ks-badge ks-badge-verified">04 Connect</div>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        img_hero = load_image_asset(IMAGE_REGISTRY["IMAGE_SET_3"]["path"])
        if img_hero:
            st.image(
                img_hero,
                use_container_width=True,
                caption="Yakshagana Heroic Character (Mukhavarnike & Kedage-mandale Pagadi) — Authoritative Project Asset"
            )

    st.markdown("---")

    # Authoritative Traditions Gallery
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <div class="brand-eyebrow">Authoritative Reference Assets</div>
        <h2>Explore the Living Traditions</h2>
        <p style="color: #5C564E; max-width: 650px; margin: 0 auto;">
            Inspected and verified photographic assets highlighting the visual grammar of coastal Karnataka and Tamil Nadu classical traditions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")
    assets = [
        ("IMAGE_SET_1", col1),
        ("IMAGE_SET_2", col2),
        ("IMAGE_SET_3", col3),
        ("IMAGE_SET_4", col4)
    ]

    for key, col in assets:
        data = IMAGE_REGISTRY[key]
        img = load_image_asset(data["path"])
        with col:
            if img:
                st.image(img, use_container_width=True)
            st.markdown(f"""
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--gold); font-weight: 700;">
                {data['art_form']}
            </div>
            <div style="font-weight: 600; font-size: 0.9rem; margin: 0.2rem 0;">
                {data['title']}
            </div>
            <div style="font-size: 0.8rem; color: #5C564E; line-height: 1.4;">
                {data['category']}
            </div>
            """, unsafe_allow_html=True)

    # Core Loop Banner
    st.markdown("---")
    st.markdown("""
    <div class="ks-card" style="text-align: center; background: #FFFDF9; border: 1px solid var(--gold);">
        <div class="brand-eyebrow">The Complete Cultural Loop</div>
        <h3 style="color: var(--vermilion); margin: 0.4rem 0;">SEE → UNDERSTAND → DISCOVER → CONNECT</h3>
        <p style="max-width: 720px; margin: 0.5rem auto; font-size: 0.95rem; color: #5C564E;">
            Audience members experience the story in real-time. Troupes publish shareable QR guides for their live stage. 
            Technology does not replace the artist—it amplifies human creativity.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_audience_explorer(client):
    """Audience Scene Explorer: Photo Upload & Cultural Breakdown."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div class="brand-eyebrow">Audience Experience</div>
        <h2>🎭 Audience Scene Explorer</h2>
        <p style="color: #5C564E;">Upload or select a performance photo. KalaSetu will explain what you are seeing, the character, and the story.</p>
    </div>
    """, unsafe_allow_html=True)

    # Selection Tabs for Source
    source_choice = st.radio(
        "Choose Image Source:",
        ["🖼️ Select from Authoritative Hackathon Assets", "📁 Upload Your Own Image", "📷 Use Camera"],
        horizontal=True
    )

    selected_image = None
    preset_key = None

    if source_choice == "🖼️ Select from Authoritative Hackathon Assets":
        st.markdown("##### Select an authoritative reference photo:")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            im1 = load_image_asset(IMAGE_REGISTRY["IMAGE_SET_1"]["path"])
            if im1:
                st.image(im1, use_container_width=True)
            if st.button("Use Bharatanatyam Solo", key="btn_p1"):
                st.session_state["selected_preset"] = "IMAGE_SET_1"
                
        with c2:
            im2 = load_image_asset(IMAGE_REGISTRY["IMAGE_SET_2"]["path"])
            if im2:
                st.image(im2, use_container_width=True)
            if st.button("Use Stage Ensemble", key="btn_p2"):
                st.session_state["selected_preset"] = "IMAGE_SET_2"

        with c3:
            im3 = load_image_asset(IMAGE_REGISTRY["IMAGE_SET_3"]["path"])
            if im3:
                st.image(im3, use_container_width=True)
            if st.button("Use Yakshagana Hero", key="btn_p3"):
                st.session_state["selected_preset"] = "IMAGE_SET_3"

        with c4:
            im4 = load_image_asset(IMAGE_REGISTRY["IMAGE_SET_4"]["path"])
            if im4:
                st.image(im4, use_container_width=True)
            if st.button("Use Costume Craft Detail", key="btn_p4"):
                st.session_state["selected_preset"] = "IMAGE_SET_4"

        preset_key = st.session_state.get("selected_preset", "IMAGE_SET_1")
        preset_info = IMAGE_REGISTRY[preset_key]
        selected_image = load_image_asset(preset_info["path"])
        st.success(f"Currently Selected: **{preset_info['title']}** ({preset_info['art_form']})")

    elif source_choice == "📁 Upload Your Own Image":
        uploaded_file = st.file_uploader(
            "Upload performance frame (JPG, PNG, WebP):",
            type=["jpg", "jpeg", "png", "webp"]
        )
        if uploaded_file:
            try:
                selected_image = Image.open(uploaded_file)
                st.image(selected_image, width=320, caption="Uploaded Image")
            except Exception as e:
                st.error("Invalid image file. Please upload a valid JPG, PNG, or WebP.")

    else:
        cam_file = st.camera_input("Take a photo of the stage or costume:")
        if cam_file:
            try:
                selected_image = Image.open(cam_file)
            except Exception as e:
                st.error("Error accessing camera image.")

    # Context Inputs
    st.markdown("---")
    col_ctx1, col_ctx2 = st.columns(2)
    with col_ctx1:
        art_form_hint = st.selectbox(
            "Art Form (Optional hint for faster inference):",
            ["Auto Detect", "Yakshagana", "Bharatanatyam", "Other / Classical Indian Tradition"]
        )
    with col_ctx2:
        default_ep = IMAGE_REGISTRY.get(preset_key, {}).get("default_episode", "") if preset_key else ""
        performance_name = st.text_input(
            "Episode or Performance Title (Optional context, e.g. 'Devi Mahatme', 'Varnam'):",
            value=default_ep,
            placeholder="e.g. Devi Mahatme, Nataraja Vandana, Karna Parva"
        )

    # Action Button
    analyze_clicked = st.button("🔍 Analyze Performance with KalaSetu", type="primary")

    if analyze_clicked:
        if selected_image is None:
            st.warning("Please select or upload a performance image first.")
        else:
            with st.spinner("Interpreting visual elements, mudras, costume canons, and cultural narrative..."):
                res_data, is_demo, msg = analyze_scene_image(
                    client,
                    selected_image,
                    art_form_hint,
                    performance_name,
                    preset_key
                )
                st.session_state["analysis_result"] = {
                    "data": res_data,
                    "image": selected_image,
                    "is_demo": is_demo,
                    "msg": msg
                }

    # Render previous or new result
    if st.session_state.get("analysis_result"):
        saved = st.session_state["analysis_result"]
        render_scene_result_ui(
            saved["data"],
            saved["image"],
            saved["is_demo"],
            saved["msg"]
        )

def render_artist_portal(client):
    """Performer & Troupe Portal: Stage Guide Generator & Scannable QR."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div class="brand-eyebrow">Performer Experience</div>
        <h2>🎪 For Artists & Performing Troupes</h2>
        <p style="color: #5C564E;">
            Give your audience the story behind your performance. Create a shareable, mobile-optimized KalaSetu Stage Guide and QR code for venue posters, brochures, and stage screens.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Demo Loaders
    st.markdown("##### Quick Demo Profiles:")
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        if st.button("📋 Load Demo Profile: Kateel Yakshagana Mela"):
            st.session_state["artist_form_data"] = DEMO_PERFORMERS["kateel_mela"].copy()
    with c_p2:
        if st.button("📋 Load Demo Profile: Nritya Kalakshetra Troupe"):
            st.session_state["artist_form_data"] = DEMO_PERFORMERS["nritya_kalakshetra"].copy()

    default_form = st.session_state.get("artist_form_data", DEMO_PERFORMERS["kateel_mela"])

    with st.form("artist_guide_form"):
        st.markdown("#### 1. Troupe & Production Details")
        c1, c2 = st.columns(2)
        with c1:
            troupe_name = st.text_input("Troupe / Artist Name:", value=default_form.get("troupe_name", ""))
            art_form = st.selectbox(
                "Art Form:",
                ["Yakshagana", "Bharatanatyam", "Kathakali", "Kuchipudi", "Odissi", "Other Traditional Theatre"],
                index=0 if "Yakshagana" in default_form.get("art_form", "") else 1
            )
            location = st.text_input("Troupe Base / Performance Location:", value=default_form.get("location", ""))
        with c2:
            perf_title = st.text_input("Performance / Episode Title:", value=default_form.get("performance_title", ""))
            contact = st.text_input("Contact / Booking Phone:", value=default_form.get("contact_number", "+91 98450 XXXXX"))
            email = st.text_input("Official Booking Email:", value=default_form.get("email", "booking@troupe.example.org"))

        st.markdown("#### 2. Narrative, Characters & Visual Notes")
        synopsis_input = st.text_area(
            "Episode Synopsis & Background:",
            value=default_form.get("synopsis", ""),
            height=110
        )

        c3, c4 = st.columns(2)
        with c3:
            characters_input = st.text_area(
                "Key Characters (Name, Role Type, Notes):",
                value="\n".join([f"{c['role']} | {c['type']} | {c['note']}" for c in default_form.get("characters", [])]),
                height=110
            )
        with c4:
            symbols_input = st.text_area(
                "Important Mudras, Symbols, or Musical Cues:",
                value="\n".join(default_form.get("symbols_and_mudras", [])),
                height=110
            )

        what_to_watch_input = st.text_area(
            "Audience Watch Notes (Specific cues to observe during the show):",
            value=default_form.get("what_to_watch", ""),
            height=90
        )

        generate_submitted = st.form_submit_button("✨ Publish & Generate KalaSetu Stage Guide", type="primary")

    if generate_submitted:
        # Construct updated profile
        slug = f"guide_{abs(hash(troupe_name + perf_title)) % 10000}"
        
        # Parse characters lines
        char_list = []
        for line in characters_input.strip().split("\n"):
            if "|" in line:
                parts = line.split("|")
                char_list.append({"role": parts[0].strip(), "type": parts[1].strip(), "note": parts[2].strip() if len(parts) > 2 else ""})
            elif line.strip():
                char_list.append({"role": line.strip(), "type": "Traditional Role", "note": ""})

        updated_profile = {
            "id": slug,
            "troupe_name": troupe_name,
            "badge": "VERIFIED PERFORMER PROFILE",
            "art_form": art_form,
            "performance_title": perf_title,
            "location": location,
            "contact_number": contact,
            "email": email,
            "synopsis": synopsis_input,
            "highlights": [
                f"Authentic staging of {perf_title} preserving {art_form} traditions",
                "Codified costume and visual storytelling canon",
                "Live traditional acoustic rhythm and musical accompaniment"
            ],
            "characters": char_list,
            "symbols_and_mudras": [s.strip() for s in symbols_input.split("\n") if s.strip()],
            "what_to_watch": what_to_watch_input
        }

        st.session_state["performance_guides"][slug] = updated_profile
        st.session_state["active_guide_slug"] = slug
        st.success(f"🎉 Performance Guide created successfully for '{perf_title}'!")

    # Display active or demo guide QR
    active_slug = st.session_state.get("active_guide_slug", "kateel_mela")
    active_guide = st.session_state["performance_guides"].get(active_slug, DEMO_PERFORMERS["kateel_mela"])

    st.markdown("---")
    st.markdown("### 📱 Shareable Stage Guide & Scannable QR Code")

    col_qr, col_meta = st.columns([1, 1.8], gap="large")

    stage_url = f"{PUBLIC_APP_URL}/?stage={active_slug}"
    qr_img = generate_stage_qr(stage_url)

    with col_qr:
        st.image(qr_img, width=240, caption="Scan with phone camera at venue")
        
        # Download QR Button
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.download_button(
            label="⬇️ Download High-Res Venue QR (PNG)",
            data=buf.getvalue(),
            file_name=f"kalasetu_qr_{active_slug}.png",
            mime="image/png"
        )

    with col_meta:
        st.markdown(f"""
        <div class="ks-card">
            <div class="brand-eyebrow">Public Stage Guide Preview</div>
            <h3 style="margin: 0.2rem 0; color: var(--vermilion);">{active_guide.get('performance_title')}</h3>
            <p style="margin: 0; font-size: 0.9rem; color: #5C564E;">Presented by: <strong>{active_guide.get('troupe_name')}</strong></p>
            <p style="font-size: 0.85rem; margin-top: 0.4rem;">Location: {active_guide.get('location')} | Art Form: {active_guide.get('art_form')}</p>
            
            <div style="background: #F4EFE6; padding: 0.8rem; border-radius: 6px; font-size: 0.88rem; margin: 1rem 0;">
                <strong>Public URL for venue posters:</strong><br>
                <code>{stage_url}</code>
            </div>
            
            <p style="font-size: 0.85rem; color: #5C564E;">
                Audience members who scan this QR immediately see the clean, mobile-optimized guide without needing to log in.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📲 Preview Mobile Stage Guide Directly In App"):
            st.query_params["stage"] = active_slug
            st.rerun()

def render_cultural_copilot(client):
    """Cultural AI Copilot with Google Search Grounding and Verified Citations."""
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div class="brand-eyebrow">AI Copilot & Research</div>
        <h2>💡 Ask Cultural AI</h2>
        <p style="color: #5C564E;">
            Ask questions about Indian performing arts, ritual makeup, Mudra canons, and historical traditions.
            Grounded in KalaSetu's Master Knowledge and verified Google Search where needed.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion Chips
    st.markdown("##### Quick Inquiries:")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("❓ Why do Yakshagana demons wear artificial fangs?"):
            st.session_state["query_input"] = "Why do Yakshagana demons have elaborate facial makeup and artificial fangs?"
    with c2:
        if st.button("❓ What is Aramandi in Bharatanatyam?"):
            st.session_state["query_input"] = "What does Aramandi mean in Bharatanatyam, and why is the pleated fan important?"
    with c3:
        if st.button("❓ What is Badagutittu vs. Tenkutittu?"):
            st.session_state["query_input"] = "What is the difference between Badagutittu and Tenkutittu styles in Yakshagana?"

    user_query = st.text_input(
        "Enter your question:",
        value=st.session_state.get("query_input", ""),
        placeholder="e.g. What does Shikhara mudra signify in classical dance?"
    )

    search_clicked = st.button("🔍 Search & Answer with Cultural Grounding", type="primary")

    if search_clicked and user_query.strip():
        with st.spinner("Consulting KalaSetu Master Knowledge Base & Google Search Grounding..."):
            ans, sources, is_offline = ask_cultural_copilot(client, user_query.strip())
            st.session_state["copilot_result"] = {
                "query": user_query.strip(),
                "answer": ans,
                "sources": sources,
                "is_offline": is_offline
            }

    if st.session_state.get("copilot_result"):
        res = st.session_state["copilot_result"]
        st.markdown("---")
        
        st.markdown(f"""
        <div class="ks-card">
            <div class="brand-eyebrow">Inquiry</div>
            <h3 style="color: var(--vermilion); margin-top: 0.2rem;">{res['query']}</h3>
            <div style="font-size: 1rem; line-height: 1.7; margin-top: 1rem;">
                {res['answer']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sources & Citations Box
        sources = res.get("sources", [])
        st.markdown("""
        <div class="ks-card" style="background: #FAF7F2; border-left: 4px solid var(--gold);">
            <div class="brand-eyebrow">Grounding & Source Verification</div>
            <h4 style="margin: 0.2rem 0; font-family: 'Cinzel', serif;">Information Sources</h4>
        """, unsafe_allow_html=True)

        st.markdown("""
        - 🏛️ **Primary Cultural Source:** KalaSetu Curated Master Knowledge Base (Abhinaya Darpana, Natya Shastra, Yakshagana Prasanga tradition)
        """)

        if sources:
            st.markdown("##### 🌐 Web-Grounded Citations:")
            for s in sources:
                st.markdown(f"- [{s.get('title', 'Web Reference')}]({s.get('url', '#')})")
        else:
            st.markdown("<p style='font-size: 0.85rem; color: #5C564E;'>Grounded purely on verified internal master canons without unverified web claims.</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# 12. APP ENTRY POINT & ROUTING
# ==============================================================================

def main():
    # 1. Check for Mobile-First Stage Guide routing (?stage=...)
    params = st.query_params
    if "stage" in params:
        stage_slug = params["stage"]
        render_mobile_stage_guide(stage_slug)
        return

    # 2. Sidebar Configuration — API key is backend-only (loaded from .env, never shown in UI)
    client = get_gemini_client()
    is_live_mode = client is not None

    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-family: 'Cinzel', serif; font-size: 1.6rem; font-weight: 700; color: #9E2A2B;">KALASETU</div>
            <div style="font-size: 0.75rem; letter-spacing: 1px; color: #C5A059; text-transform: uppercase;">Digital Cultural Companion</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🤖 AI Engine Status")

        if is_live_mode:
            st.success("🟢 **Live AI Mode Active**  \nGemini 2.5 Flash — Vision & Grounded Search enabled.")
        else:
            st.info(
                "🟡 **Graceful Demo Mode**  \n"
                "Showing verified KalaSetu sample analyses.  \n"
                "*(API key configured in backend `.env` file)*"
            )

        st.markdown("---")
        st.markdown("### 🏆 Hackathon Submission")
        st.markdown("""
        **Event:** ACM x MLH Hackathon  
        **Track:** Art Beyond Boundaries  
        **Problem:** *"What is Earth without Art? Just a Rock."*  
        **Team:** Gagan Naik & GaneshPrasad  
        **Model:** Gemini 2.5 Flash  
        """)

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.75rem; color: #736B5E; text-align: center;">
            KalaSetu v1.0 • Built with Streamlit, Pillow, qrcode & Google GenAI SDK
        </div>
        """, unsafe_allow_html=True)

    # 3. Main Navigation
    tab_home, tab_explore, tab_artists, tab_copilot = st.tabs([
        "🏛️ Overview & Traditions",
        "🎭 Audience Scene Explorer",
        "🎪 For Artists & Troupes",
        "💡 Ask Cultural AI"
    ])

    with tab_home:
        render_home_page()

    with tab_explore:
        render_audience_explorer(client)

    with tab_artists:
        render_artist_portal(client)

    with tab_copilot:
        render_cultural_copilot(client)

if __name__ == "__main__":
    main()
