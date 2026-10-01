# KALASETU (ಕಲಾಸೇತು / कलासेतु)
> **"See the art. Understand the story. Connect with the artist."**

**ACM x MLH Hackathon** | **Track:** Art Beyond Boundaries  
**Problem Statement:** *"What is Earth without Art? Just a Rock."*  
**Team Members:** Gagan Naik & GaneshPrasad  

---

## 🌟 Executive Summary & Problem Framing

Traditional Indian performing arts such as **Yakshagana** and **Bharatanatyam** are extraordinary living traditions rich with mythological narratives, codified mudras, intricate facial makeup (*Mukhavarnike*), and sculptural postures. 

However, first-time viewers and young audiences face steep barriers:
1. **The Story is Unclear** — *Who is this character? What mythological conflict is unfolding?*
2. **The Art is Unfamiliar** — *What does this costume, facial paint, fangs, or hand gesture mean?*
3. **Artists Struggle for Visibility** — *Regional troupes and traditional practitioners remain disconnected from digital discovery.*

**KalaSetu bridges this boundary.** Instead of building another generic entertainment feed, KalaSetu acts as the **cultural interpreter between the artist and the audience**.

```
                   KALASETU ARCHITECTURE
                             │
            ┌────────────────┴────────────────┐
            │                                 │
     AUDIENCE JOURNEY                  ARTIST JOURNEY
            │                                 │
    Upload / Snap Photo               Create Stage Profile
            │                                 │
   Gemini 2.5 Flash Vision            Performance & Story Data
            │                                 │
    Cultural Story & Mudra             Dynamic QR Generator
            │                                 │
            └────────────────┬────────────────┘
                             │
                     CULTURAL AI LAYER
                             │
                   MASTER KNOWLEDGE BASE
                             │
                     GEMINI 2.5 FLASH
                             │
                  GOOGLE SEARCH GROUNDING
```

---

## 🔁 The Core Cultural Loop

- **Audience:** `SEE → UNDERSTAND → DISCOVER`
- **Artist:** `PERFORM → SHARE → CONNECT`
- **Together:** `ARTIST ↔ AUDIENCE`

---

## 📸 The Four Authoritative Project Assets

The project incorporates 4 inspected and verified photographic assets that serve as the visual benchmark for the system:

| Identifier | Asset File | Tradition | Visual Focus & Canonical Elements |
|---|---|---|---|
| **IMAGE_SET_1** | `bharatanatyam1.jpeg` | Bharatanatyam | Solo dancer in deep seated *Muzhumandi* posture, executing *Shikhara Hasta* mudra, two-tone black/saffron Kanchipuram silk pleats, temple jewelry (*Manga Malai*, *Oddiyanam*), and red *Alta* on fingers. |
| **IMAGE_SET_2** | `bharatanatyam2.jpeg` | Bharatanatyam | Six-dancer stage ensemble in synchronized *Aramandi* diamond formations under dramatic red theatrical lighting. Demonstrates ensemble choreography and *Visiri* pleated fan symmetry. |
| **IMAGE_SET_3** | `yakshagana1.jpeg` | Yakshagana | Heroic/Royal character (*Raja Vesha*) in dynamic warrior *Mandai* stance, towering *Kedage-mandale Pagadi* headgear, Vaishnavite *Urdhva-Pundra Mukhavarnike*, embroidered *dagale* breastplate, and tiered ruffles. |
| **IMAGE_SET_4** | `yakshagana2.jpeg` | Yakshagana | Detail study of costume craftsmanship: embroidered shoulder epaulettes (*Bhujakeerthi*), wristbands (*Kadaga*), mirror medallions, and fine facial eyeliner canons. |

---

## 🚀 Key Features & Capabilities

### 1. 🎭 Audience Scene Explorer
- **Visual Evidence First**: Analyzes costume, facial makeup, mudras, stage postures, and character roles.
- **Uncertainty-Aware Interpretation**: Clearly separates visual evidence from cultural inferences; never fabricates characters, episodes, or history.
- **Mudra Detection**: Identifies single-hand (*Asamyutta*) and double-hand (*Samyutta*) gestures (e.g., *Shikhara*, *Pataka*, *Alapadma*) with canonical Sanskrit names and verified meanings.
- **Dynamic Stage Cues**: Provides viewers with practical "What to Watch For on Stage" bullet points (rhythmic tempo shifts, pirouettes, bell strikes).
- **Episodic Context**: Accepts optional performance names (e.g. *"Devi Mahatme"*, *"Varnam"*) to contextualize the scene within its traditional storyline.

### 2. 🎪 Performer & Troupe Portal
- **One-Click Stage Guide Generator**: Troupes enter their performance details, synopsis, characters, and mudra highlights.
- **Dynamic QR Code Generation**: Generates high-resolution, branded venue QR codes linking directly to a shareable stage guide.
- **Mobile-First Auditorium Experience (`?stage=...`)**: Designed specifically for an audience member standing in a theatre holding a smartphone.
- **Artist Booking & Contact**: Connects audience members and festival curators directly to the troupe via phone and email.

### 3. 💡 Cultural AI Copilot
- **Authoritative Q&A**: Answers deep cultural questions on regional traditions (e.g., *Badagutittu* vs. *Tenkutittu*, *Aramandi* anatomy, demon fangs and *Chutti* borders).
- **Google Search Grounding**: Leverages real-time Google Search grounding with verified source titles and clickable citations.
- **Curated vs. Web Distinction**: Explicitly labels internal Master Knowledge from external web citations.

### 4. 🛡️ Graceful Hackathon Demo Mode
- If an API key is not yet supplied or during network fluctuations, the application gracefully operates in **Demo Mode** using verified, pre-baked analyses for the 4 image sets and demo troupe profiles.
- Judges experience zero tracebacks or broken screens.

---

## 🛠️ Technology Stack

- **Language:** Python 3.10+ (tested on Python 3.11)
- **Framework:** Streamlit (>= 1.38.0)
- **AI SDK:** Official Google GenAI SDK (`google-genai>=1.0.0`)
- **AI Model:** `gemini-2.5-flash`
- **Vision & Image Processing:** Pillow (PIL)
- **QR Generation:** `qrcode[pil]`
- **State & Storage:** `st.session_state` (zero external database overhead)

---

## 📦 Installation & Setup

### 1. Clone or Open the Workspace
```bash
cd path/to/hackathon
```

### 2. Create Virtual Environment & Install Dependencies
```bash
# Using standard venv
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Or using uv (recommended for speed)
uv venv --python 3.11
uv pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
KALASETU_PUBLIC_URL=http://localhost:8501
```
*(You can also enter your Gemini API key directly into the secure sidebar input in the web interface).*

### 4. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🎯 10-Second Judge Walkthrough

1. **Overview Tab:** Read the problem statement and review the 4 authoritative reference image sets.
2. **Audience Scene Explorer Tab:**
   - Click one of the 4 authoritative preset buttons (e.g. **"Use Yakshagana Hero"** or **"Use Bharatanatyam Solo"**).
   - Click **"Analyze Performance with KalaSetu"**.
   - Notice the two-column breakdown: visual evidence, costume/makeup/mudra cards, cultural story, and stage cues to watch for.
3. **For Artists & Troupes Tab:**
   - Click **"Load Demo Profile: Kateel Yakshagana Mela"**.
   - Click **"Publish & Generate KalaSetu Stage Guide"**.
   - Observe the live QR code and click **"Preview Mobile Stage Guide Directly In App"** to see the mobile reader view.
4. **Ask Cultural AI Tab:**
   - Click one of the suggestion chips (e.g., *"Why do Yakshagana demons wear artificial fangs?"*).
   - View the grounded cultural response with citations.

---

## 📜 Ethical AI & Cultural Respect Statement

KalaSetu treats traditional Indian performing arts as sacred cultural heritage. The AI model is constrained by strict temperature limits and Master Knowledge guidance to interpret and explain rather than hallucinate. Unsubstantiated claims are explicitly flagged with transparent confidence and uncertainty disclosures.
