# Enterprise-Grade Skills Reference
## Rume Dominic Job Search Agent — Technical Documentation
**Stack:** Python · Playwright · Claude API · Flask · SQLite**  
**Author:** Senior AI Automation Engineer  
**Principal:** Dominic Orume Uririe | `orumedominic@gmail.com`  
**Version:** 1.0.0 | 2026-04-05

---

## Table of Contents
1. [Skill 01 — Advanced Form-Field Mapping](#skill-01)
2. [Skill 02 — Error Handling & Resilience](#skill-02)
3. [Skill 03 — Dynamic Tailoring Logic](#skill-03)
4. [Skill 04 — Post-Application Intelligence](#skill-04)
5. [Architecture Overview](#architecture)
6. [Python Environment](#environment)
7. [Brand Voice Prompt Template](#brand-voice)

---

<a name="skill-01"></a>
## Skill 01 — Advanced Form-Field Mapping

### Purpose
Handles non-standard, open-ended, and behavioural application questions that cannot
be resolved by simple field-name matching. The agent classifies each unknown field,
routes it to the correct knowledge source (CV facts, Vorem founder narrative, brand
pillars), and uses the Claude API to generate a contextually appropriate answer at
runtime — within the Rume Dominic brand voice.

### Architecture

```
Unknown Field Detected
        │
        ▼
┌─────────────────────┐
│  FieldClassifier    │  → Regex + semantic embedding match
│  classify(label)    │  → Returns FieldType enum
└────────┬────────────┘
         │
   ┌─────┴──────────────────────────────────────────┐
   │ FieldType routing                               │
   ├─────────────────────────────────────────────────┤
   │ LEADERSHIP    → VoremFounderKnowledgeBase       │
   │ MOTIVATION    → BrandPillarStore                │
   │ SALARY        → SalaryPolicy                   │
   │ TECHNICAL     → CVFactExtractor                 │
   │ UNKNOWN       → ClaudeAPIFallback               │
   └─────────────────────────────────────────────────┘
        │
        ▼
  ClaudeAPI.generate(prompt, context, max_tokens)
        │
        ▼
  BrandVoiceValidator.check(response)  → passes / redraft
        │
        ▼
  page.fill(selector, validated_response)
```

### Field Type Taxonomy

| FieldType | Trigger Keywords | Knowledge Source |
|---|---|---|
| `LEADERSHIP` | leadership, manage, lead, team, mentor, philosophy | `VoremFounderKnowledgeBase` |
| `MOTIVATION` | why us, why role, passion, vision, goal | `BrandPillarStore` |
| `TECHNICAL` | stack, tools, languages, experience with, proficiency | `CVFactExtractor` |
| `ACHIEVEMENT` | proud of, biggest win, impact, result | `AchievementsStore` |
| `SALARY` | salary, compensation, rate, expectation | `SalaryPolicy` |
| `DIVERSITY` | background, culture, diversity, inclusion | `PersonalNarrativeStore` |
| `AVAILABILITY` | start date, notice period, available from | `AvailabilityPolicy` |
| `UNKNOWN` | anything not matched above | `ClaudeAPIFallback` (zero-shot) |

### Python Implementation

```python
# skills/form_field_mapper.py

import re
import anthropic
from enum import Enum
from dataclasses import dataclass
from config import CANDIDATE, BRAND

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env


class FieldType(Enum):
    LEADERSHIP   = "leadership"
    MOTIVATION   = "motivation"
    TECHNICAL    = "technical"
    ACHIEVEMENT  = "achievement"
    SALARY       = "salary"
    DIVERSITY    = "diversity"
    AVAILABILITY = "availability"
    UNKNOWN      = "unknown"


# ── Keyword routing table ──────────────────────────────────────────────────
ROUTING_RULES: list[tuple[FieldType, list[str]]] = [
    (FieldType.LEADERSHIP,   ["lead", "manag", "team", "mentor", "philosophy", "supervis"]),
    (FieldType.MOTIVATION,   ["why", "passion", "vision", "goal", "interest", "attract"]),
    (FieldType.TECHNICAL,    ["stack", "tool", "language", "framework", "proficien", "experience with"]),
    (FieldType.ACHIEVEMENT,  ["proud", "achiev", "impact", "result", "success", "accomplish"]),
    (FieldType.SALARY,       ["salary", "compens", "rate", "expect", "package"]),
    (FieldType.DIVERSITY,    ["background", "divers", "inclus", "culture", "identit"]),
    (FieldType.AVAILABILITY, ["start", "notice", "availab", "when can"]),
]


def classify_field(label: str) -> FieldType:
    """Classify a form field label into a FieldType."""
    label_lower = label.lower()
    for field_type, keywords in ROUTING_RULES:
        if any(kw in label_lower for kw in keywords):
            return field_type
    return FieldType.UNKNOWN


# ── Knowledge bases ────────────────────────────────────────────────────────
VOREM_FOUNDER_CONTEXT = """
Rume Dominic is the Founder and Lead Strategist of Vorem Limited (est. 2017),
a digital education and technology company. Over 7+ years of leadership, he has:
- Scaled Vorem from a solo venture to a multi-service digital education platform
- Built and led cross-functional remote teams across AI engineering and content strategy
- Authored 5 published books on technology, business, and digital transformation
- Spoken at FrontierTechX, representing the intersection of AI and business strategy
- Completed an MSc in AI & Business Strategy (Distinction track) at Aston University
- Developed Vorem Academy, empowering entrepreneurs through structured learning systems
Leadership philosophy: servant-first leadership, systems thinking, and bias toward
measurable impact over activity. Rume leads by building scalable systems that outlast
individual effort.
"""

BRAND_PILLARS = """
Core identity pillars for Rume Dominic:
1. AI x Business Strategy: Bridging the gap between cutting-edge AI engineering and
   real-world business outcomes. Not just building models — building revenue.
2. Founder Resilience: Nigerian-born, globally minded. Built Vorem through economic
   uncertainty, proving that constraint breeds innovation.
3. Responsible AI: Every system must be governed, audited, and human-accountable.
4. Continuous Learning: Currently pursuing MSc AI & Business Strategy at Aston
   University — because leadership without learning is stagnation.
5. Global Vision: Targeting roles across UK, Amsterdam, Ontario, and Brisbane —
   the Global Talent Visa represents recognition of exceptional, portable capability.
"""

ACHIEVEMENTS_STORE = """
Key quantified achievements:
- Engineered Tax Intelligence OCR Engine: RAG-powered system automating financial
  data extraction, achieving enterprise-grade precision for tax compliance workflows.
- BRIAN-STORE-AI: Autonomous retail agent reducing manual data entry by 100% via
  Gemini API + QuickBooks integration.
- AI Content Engine at Simeria: Scaled multi-channel marketing automation across
  LinkedIn, YouTube, and X using Python + Google AI Studio.
- Micki Solutions: Production AI systems achieving 91+ performance/reliability scores.
- Published 5 books — evidence of structured thought leadership at scale.
- FrontierTechX Speaker: Recognised as a frontier voice in AI strategy.
"""

PERSONAL_NARRATIVE = """
Rume Dominic is a Nigerian-born engineer and entrepreneur whose identity is inseparable
from building — companies, systems, knowledge, and communities. His diverse background
gives him an instinctive ability to navigate ambiguity, synthesise cross-cultural
perspectives into product decisions, and lead with empathy rooted in lived experience.
Diversity is not a talking point for Rume — it is the operating context in which he
has always built.
"""


# ── Response generator ─────────────────────────────────────────────────────
def generate_field_response(
    label: str,
    field_type: FieldType,
    job_context: str,
    max_words: int = 120,
) -> str:
    """
    Generate a brand-consistent answer for any application form field.

    Args:
        label:        The exact form field label (e.g. "What is your leadership philosophy?")
        field_type:   Classified FieldType
        job_context:  JD summary / role + company for contextual grounding
        max_words:    Hard cap on response length

    Returns:
        Validated brand-voice string ready for form injection
    """

    knowledge_map = {
        FieldType.LEADERSHIP:   VOREM_FOUNDER_CONTEXT,
        FieldType.MOTIVATION:   BRAND_PILLARS,
        FieldType.TECHNICAL:    f"CV skills: {CANDIDATE.get('skills_summary', '')}",
        FieldType.ACHIEVEMENT:  ACHIEVEMENTS_STORE,
        FieldType.DIVERSITY:    PERSONAL_NARRATIVE,
        FieldType.SALARY:       f"Expected: £{CANDIDATE['salary_expectation_gbp']} or AUD {CANDIDATE['salary_expectation_aud']}",
        FieldType.AVAILABILITY: f"Notice period: {CANDIDATE['notice_period']}. Right to work UK: {CANDIDATE['right_to_work_uk']}",
        FieldType.UNKNOWN:      f"{VOREM_FOUNDER_CONTEXT}\n\n{BRAND_PILLARS}",
    }

    knowledge = knowledge_map[field_type]

    system_prompt = f"""You are the personal writing assistant for Rume Dominic, a Senior AI Engineer
and Founder. You write concise, compelling application form answers in his voice:
professional, visionary, grounded in practical outcomes, and always connecting
AI engineering to business strategy. Never use generic filler phrases.
Always reference specific achievements when relevant.
Maximum {max_words} words. No preamble. Output the answer only."""

    user_prompt = f"""
Role being applied for: {job_context}

Form field label: "{label}"

Relevant context about Rume Dominic:
{knowledge}

Write the ideal answer to this form field in Rume's voice.
"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    answer = response.content[0].text.strip()

    # Brand voice validation gate
    return _validate_brand_voice(answer, label)


def _validate_brand_voice(text: str, label: str) -> str:
    """
    Lightweight guard: reject generic filler, ensure brand markers present
    for leadership/motivation fields.
    """
    banned_phrases = [
        "i am a team player",
        "i am passionate about",
        "i have always been interested in",
        "i am a hard worker",
        "results-driven professional",
    ]
    text_lower = text.lower()
    for phrase in banned_phrases:
        if phrase in text_lower:
            # Replace with a safe fallback note — human will catch this in review
            return f"[REVIEW REQUIRED — generic phrase detected for field: '{label}']\n\n{text}"
    return text


# ── Main entry: scan page and fill all unknown fields ──────────────────────
async def map_and_fill_unknown_fields(page, job_context: str):
    """
    Scans all visible textarea and text input fields on page.
    For pre-known fields (name, email etc.) skips. For open-ended
    fields, classifies and auto-generates a brand-consistent answer.
    """
    SKIP_LABELS = {"name", "email", "phone", "location", "address", "city",
                   "postcode", "linkedin", "website", "salary", "cv", "resume"}

    # Find all labelled inputs and textareas
    inputs = await page.query_selector_all("textarea, input[type='text']")

    for inp in inputs:
        # Try to get associated label text
        label_text = ""
        input_id = await inp.get_attribute("id")
        if input_id:
            label_el = await page.query_selector(f'label[for="{input_id}"]')
            if label_el:
                label_text = (await label_el.inner_text()).strip()

        if not label_text:
            label_text = await inp.get_attribute("placeholder") or ""
        if not label_text:
            label_text = await inp.get_attribute("name") or ""

        # Skip known standard fields
        if any(skip in label_text.lower() for skip in SKIP_LABELS):
            continue

        # Check if already filled
        current_value = await inp.input_value()
        if current_value and len(current_value) > 5:
            continue

        # Classify and generate
        field_type = classify_field(label_text)
        if field_type == FieldType.UNKNOWN and len(label_text) < 4:
            continue  # No useful signal — skip

        print(f"  🤖 Auto-filling: '{label_text}' [{field_type.value}]")
        answer = generate_field_response(label_text, field_type, job_context)

        await inp.scroll_into_view_if_needed()
        await inp.click()
        await inp.fill("")
        await inp.type(answer, delay=90)
        print(f"     ✅ Filled ({len(answer.split())} words)")
```

---

<a name="skill-02"></a>
## Skill 02 — Error Handling & Resilience

### Purpose
Provides a layered resilience framework that detects, classifies, and recovers from
platform-specific obstacles: CAPTCHA challenges, non-standard file upload widgets,
session timeouts, stale element references, and anti-bot detection events.

### Error Classification Tree

```
Exception Raised
      │
      ├── TimeoutError ──────────────────→ RetryStrategy.RELOAD_AND_RETRY (max 3x)
      ├── ElementNotFoundError ──────────→ FallbackSelectorChain → then HUMAN_FLAG
      ├── CAPTCHADetected ───────────────→ CaptchaHandler → HUMAN_FLAG (always)
      ├── FileUploadError ───────────────→ AlternativeUploadStrategy → HUMAN_FLAG
      ├── AntiBot / 403 ─────────────────→ StealthRecovery → exponential backoff
      ├── SessionExpired ────────────────→ SessionRefresher → re-navigate
      └── UnrecoverableError ────────────→ log + notify + ABORT
```

### Python Implementation

```python
# skills/resilience.py

import asyncio
import time
import random
import logging
from pathlib import Path
from playwright.async_api import Page, TimeoutError as PWTimeout

logger = logging.getLogger("resilience")


# ── CAPTCHA Detection & Handler ────────────────────────────────────────────
CAPTCHA_SIGNALS = [
    "iframe[src*='recaptcha']",
    "iframe[src*='hcaptcha']",
    "div.cf-challenge",          # Cloudflare Turnstile
    "#challenge-form",
    "img[src*='captcha']",
    "[id*='captcha']",
    "[class*='captcha']",
    "div[data-sitekey]",
]


async def detect_captcha(page: Page) -> bool:
    """Return True if any CAPTCHA signal is present on page."""
    for signal in CAPTCHA_SIGNALS:
        try:
            el = await page.query_selector(signal)
            if el:
                logger.warning(f"CAPTCHA detected via selector: {signal}")
                return True
        except Exception:
            pass
    return False


async def handle_captcha(page: Page, notify_fn=None) -> bool:
    """
    CAPTCHA cannot be solved programmatically without violating ToS.
    Strategy: pause, notify human, wait for manual resolution (max 5 min),
    then resume.

    Returns True if human resolved it, False if timeout.
    """
    msg = "⚠️  CAPTCHA detected. Manual intervention required."
    logger.warning(msg)
    print(f"\n{msg}")
    print("   The browser window is open. Please solve the CAPTCHA manually.")
    print("   Agent will resume automatically once the CAPTCHA is cleared.")

    if notify_fn:
        await notify_fn(msg)

    # Poll until CAPTCHA clears or 5-minute timeout
    deadline = time.time() + 300
    while time.time() < deadline:
        await asyncio.sleep(5)
        still_present = await detect_captcha(page)
        if not still_present:
            print("   ✅ CAPTCHA resolved. Resuming...")
            return True

    logger.error("CAPTCHA not resolved within 5 minutes. Aborting.")
    return False


# ── File Upload Resilience ─────────────────────────────────────────────────
UPLOAD_SELECTORS = [
    'input[type="file"]',
    'input[accept*="pdf"]',
    'input[accept*=".doc"]',
    '[data-testid*="upload"]',
    'button[aria-label*="upload" i]',
    'div[class*="dropzone"]',
    'div[class*="file-upload"]',
]


async def resilient_upload(page: Page, file_path: str) -> bool:
    """
    Multi-strategy file upload handler.

    Strategy 1: Standard input[type=file] set_input_files
    Strategy 2: Drag-and-drop simulation into dropzone
    Strategy 3: Click upload button → OS dialog intercept via filechooser
    Strategy 4: Flag for human manual upload
    """
    if not Path(file_path).exists():
        logger.error(f"CV file not found: {file_path}")
        return False

    # Strategy 1 — standard file input
    for selector in UPLOAD_SELECTORS[:2]:
        try:
            el = await page.query_selector(selector)
            if el:
                await el.set_input_files(file_path)
                await asyncio.sleep(random.uniform(1.5, 2.5))
                logger.info(f"Upload success via Strategy 1: {selector}")
                return True
        except Exception as e:
            logger.debug(f"Strategy 1 failed ({selector}): {e}")

    # Strategy 2 — filechooser event interception
    try:
        for selector in UPLOAD_SELECTORS[2:]:
            el = await page.query_selector(selector)
            if el:
                async with page.expect_file_chooser(timeout=5000) as fc_info:
                    await el.click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(file_path)
                await asyncio.sleep(random.uniform(1.0, 2.0))
                logger.info("Upload success via Strategy 2: filechooser")
                return True
    except Exception as e:
        logger.debug(f"Strategy 2 failed: {e}")

    # Strategy 3 — drag-and-drop into dropzone
    try:
        dropzone = await page.query_selector('div[class*="dropzone"], div[class*="drop-area"]')
        if dropzone:
            await page.evaluate("""
                (el) => {
                    const dt = new DataTransfer();
                    el.dispatchEvent(new DragEvent('dragover', {dataTransfer: dt, bubbles: true}));
                    el.dispatchEvent(new DragEvent('drop', {dataTransfer: dt, bubbles: true}));
                }
            """, dropzone)
            await asyncio.sleep(1)
            logger.info("Upload attempt via Strategy 3: drag-and-drop simulation")
    except Exception as e:
        logger.debug(f"Strategy 3 failed: {e}")

    # All strategies exhausted → flag for human
    logger.warning("All upload strategies failed. Flagging for human upload.")
    print("\n  ⚠️  AUTO-UPLOAD FAILED — Please upload your CV manually in the browser.")
    print(f"  File: {file_path}")
    return False


# ── Stale Element & Timeout Recovery ──────────────────────────────────────
async def retry_action(coro_fn, max_retries: int = 3, backoff_base: float = 1.5):
    """
    Retry an async action with exponential backoff.
    Handles Playwright TimeoutError and stale element references.
    """
    for attempt in range(1, max_retries + 1):
        try:
            return await coro_fn()
        except PWTimeout as e:
            wait = backoff_base ** attempt + random.uniform(0, 1)
            logger.warning(f"TimeoutError (attempt {attempt}/{max_retries}). Retrying in {wait:.1f}s: {e}")
            await asyncio.sleep(wait)
        except Exception as e:
            if "detached" in str(e).lower() or "stale" in str(e).lower():
                logger.warning(f"Stale element (attempt {attempt}). Retrying...")
                await asyncio.sleep(backoff_base ** attempt)
            else:
                raise
    raise RuntimeError(f"Action failed after {max_retries} attempts")


# ── Anti-Bot Detection Recovery ────────────────────────────────────────────
ANTIBOT_SIGNALS = [
    "Access Denied",
    "Please verify you are a human",
    "Suspicious activity detected",
    "Too many requests",
    "Rate limit exceeded",
    "cf-error-details",
]


async def check_antibot(page: Page) -> bool:
    """Check if the current page has triggered anti-bot measures."""
    content = await page.content()
    return any(signal.lower() in content.lower() for signal in ANTIBOT_SIGNALS)


async def stealth_recovery(page: Page, url: str):
    """
    Recovery sequence when anti-bot detection fires:
    1. Navigate away to a neutral page
    2. Wait with human-like jitter (30–90 seconds)
    3. Return to target URL
    4. Apply extended human-like delays before next interaction
    """
    logger.warning("Anti-bot detected. Initiating stealth recovery...")
    await page.goto("https://www.google.com", wait_until="domcontentloaded")
    recovery_wait = random.uniform(30, 90)
    logger.info(f"Cooling down for {recovery_wait:.0f}s...")
    await asyncio.sleep(recovery_wait)
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(random.uniform(3, 6))
    logger.info("Stealth recovery complete. Resuming with extended delays.")


# ── Master error handler wrapper ───────────────────────────────────────────
async def resilient_navigate(page: Page, url: str, notify_fn=None) -> bool:
    """
    Navigate to a URL with full resilience stack applied.
    Returns True on success, False if unrecoverable.
    """
    for attempt in range(1, 4):
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)

            if await detect_captcha(page):
                resolved = await handle_captcha(page, notify_fn)
                if not resolved:
                    return False

            if await check_antibot(page):
                if attempt < 3:
                    await stealth_recovery(page, url)
                    continue
                else:
                    logger.error("Anti-bot not resolved after 3 attempts.")
                    return False

            return True

        except PWTimeout:
            logger.warning(f"Navigation timeout (attempt {attempt}). Retrying...")
            await asyncio.sleep(2 ** attempt)

    return False
```

---

<a name="skill-03"></a>
## Skill 03 — Dynamic Tailoring Logic

### Purpose
Automatically adjusts the narrative emphasis of cover letters and form answers
based on the target geography. UK roles lead with Rume's MSc at Aston University
and Global Talent Visa eligibility. European (Amsterdam) roles emphasise international
business leadership and multilateral work. Australian/Canadian roles foreground
Vorem's founder story and cross-continental impact.

### Region Strategy Matrix

| Region | Primary Emphasis | Secondary Emphasis | Proof Points |
|---|---|---|---|
| **UK** | MSc AI & Business Strategy, Aston University | Global Talent Visa trajectory | Micki Solutions production AI, FrontierTechX |
| **Europe (NL/DE/FR)** | International business leadership, cross-border operations | AI engineering depth | Vorem (est. 2017), 5 books, FrontierTechX |
| **Canada (ON)** | Founder resilience, scalable AI systems | Academic credentials | BRIAN-STORE-AI, Vorem Academy, OCR Engine |
| **Australia (QLD)** | Enterprise AI delivery + blockchain expertise | Agentic workflow innovation | Binance/DeFi relevance, Cloud Run deployments |
| **USA** | Business impact + AI ROI | Thought leadership | Author credential, speaker, Vorem revenue |
| **Remote/Global** | Full-stack AI strategy, portable expertise | Visa flexibility | All pillars combined |

### Python Implementation

```python
# skills/dynamic_tailoring.py

import anthropic
from dataclasses import dataclass
from enum import Enum

client = anthropic.Anthropic()


class Region(Enum):
    UK       = "uk"
    EUROPE   = "europe"
    CANADA   = "canada"
    AUSTRALIA = "australia"
    USA      = "usa"
    REMOTE   = "remote"


def detect_region(location: str) -> Region:
    """Infer target region from job location string."""
    loc = location.lower()
    if any(x in loc for x in ["london", "birmingham", "manchester", "uk", "united kingdom", "england"]):
        return Region.UK
    if any(x in loc for x in ["amsterdam", "netherlands", "berlin", "germany", "paris", "france", "europe"]):
        return Region.EUROPE
    if any(x in loc for x in ["toronto", "ontario", "vancouver", "canada"]):
        return Region.CANADA
    if any(x in loc for x in ["brisbane", "sydney", "melbourne", "australia", "qld", "nsw"]):
        return Region.AUSTRALIA
    if any(x in loc for x in ["new york", "san francisco", "usa", "united states", "california"]):
        return Region.USA
    return Region.REMOTE


@dataclass
class TailoringConfig:
    region: Region
    primary_emphasis: str
    secondary_emphasis: str
    visa_note: str
    proof_points: list[str]
    tone_modifier: str


REGION_CONFIGS: dict[Region, TailoringConfig] = {
    Region.UK: TailoringConfig(
        region=Region.UK,
        primary_emphasis=(
            "MSc in Artificial Intelligence & Business Strategy at Aston University (Distinction track). "
            "This academic grounding directly informs my ability to design AI systems that are not only "
            "technically robust but strategically aligned — a rarity in the UK AI talent market."
        ),
        secondary_emphasis=(
            "As a credible candidate for the UK Global Talent Visa in the Digital Technology category, "
            "I represent the kind of exceptional, portable AI expertise that organisations rely on to "
            "maintain competitive advantage."
        ),
        visa_note="Full right to work in the UK. Global Talent Visa trajectory.",
        proof_points=[
            "Production AI systems at Micki Solutions achieving 91+ reliability scores",
            "FrontierTechX speaker — recognised frontier voice in UK AI strategy",
            "Responsible AI documentation and governance frameworks",
        ],
        tone_modifier="formal, academically grounded, policy-aware",
    ),
    Region.EUROPE: TailoringConfig(
        region=Region.EUROPE,
        primary_emphasis=(
            "As Founder and Lead Strategist of Vorem (est. 2017), I have operated across international "
            "markets, building digital products and education platforms that serve a globally distributed "
            "audience. I understand how to lead AI initiatives across borders — technically, commercially, "
            "and culturally."
        ),
        secondary_emphasis=(
            "My technical depth in Generative AI, RAG pipelines, and agentic orchestration is matched "
            "by strategic fluency: I hold an MSc in AI & Business Strategy and have authored 5 books "
            "on technology and leadership."
        ),
        visa_note="Open to relocation to Amsterdam. Eligible for DAFT/Highly Skilled Migrant visa.",
        proof_points=[
            "7+ years leading a digital-first company across international markets",
            "FrontierTechX speaker — cross-border thought leadership",
            "Author of 5 books — structured intellectual output at scale",
        ],
        tone_modifier="visionary, internationally minded, commercially fluent",
    ),
    Region.CANADA: TailoringConfig(
        region=Region.CANADA,
        primary_emphasis=(
            "I am a founder who builds systems, not just features. Since 2017, I have grown Vorem from "
            "a solo enterprise to a multi-service AI and education platform — proving that I can architect "
            "scalable solutions and lead organisations through technological inflection points."
        ),
        secondary_emphasis=(
            "My engineering credentials — including production RAG systems, autonomous AI agents, and "
            "AI governance frameworks — are grounded in real commercial outcomes, not academic theory alone."
        ),
        visa_note="Open to relocation to Ontario. Eligible for Express Entry under Federal Skilled Worker.",
        proof_points=[
            "BRIAN-STORE-AI: autonomous retail agent eliminating 100% of manual data entry",
            "Tax Intelligence OCR Engine: enterprise-grade financial data automation",
            "Vorem Academy: scalable e-learning infrastructure",
        ],
        tone_modifier="pragmatic, outcome-focused, entrepreneurial",
    ),
    Region.AUSTRALIA: TailoringConfig(
        region=Region.AUSTRALIA,
        primary_emphasis=(
            "I deliver enterprise AI at production grade. My portfolio includes RAG-powered OCR engines "
            "deployed on Cloud Run, autonomous agentic workflows achieving 91+ performance scores, and "
            "AI governance documentation that meets Responsible AI standards. These are not prototypes — "
            "they are live systems."
        ),
        secondary_emphasis=(
            "As a Certified Blockchain Architect with cross-industry AI experience, I bring a rare "
            "combination of distributed systems expertise and generative AI engineering — highly relevant "
            "to Australia's growing Web3 and enterprise AI sectors."
        ),
        visa_note="Open to relocation to Brisbane. Eligible for Skilled Independent (subclass 189) or Employer Sponsored (482).",
        proof_points=[
            "Certified Blockchain Architect — distributed systems and DeFi relevance",
            "Cloud Run production deployments — enterprise-grade infrastructure",
            "AI security and governance documentation for Responsible AI compliance",
        ],
        tone_modifier="delivery-focused, technically precise, enterprise-grade",
    ),
    Region.USA: TailoringConfig(
        region=Region.USA,
        primary_emphasis=(
            "I translate AI engineering into business ROI. As the founder of Vorem and an AI Engineer "
            "with 7+ years of production system delivery, I have a track record of building AI solutions "
            "that create measurable commercial outcomes — not just technical artefacts."
        ),
        secondary_emphasis=(
            "I am a published author, a conference speaker (FrontierTechX), and a graduate student "
            "in AI & Business Strategy. My thought leadership is not performative — it is evidence "
            "of deep, structured thinking about where AI is going and how organisations must adapt."
        ),
        visa_note="Visa sponsorship required for US roles. O-1A Extraordinary Ability trajectory.",
        proof_points=[
            "5 published books — intellectual authority in AI and business",
            "FrontierTechX speaker — peer-recognised thought leader",
            "Vorem founder: 7+ years of AI-driven business growth",
        ],
        tone_modifier="impact-driven, thought leadership forward, commercially sharp",
    ),
    Region.REMOTE: TailoringConfig(
        region=Region.REMOTE,
        primary_emphasis=(
            "I engineer AI systems that operate at scale, and I lead teams that span time zones. "
            "As a founder, author, and conference speaker, I bring both the technical depth and the "
            "strategic communication skills that remote-first AI leadership demands."
        ),
        secondary_emphasis=(
            "My stack — RAG, agentic orchestration, Gemini API, Azure OpenAI, Python — is fully "
            "cloud-native. My working style — async-first, documentation-driven, outcome-measured — "
            "is optimised for distributed teams."
        ),
        visa_note="Based in Birmingham, UK. Open to fully remote global roles.",
        proof_points=[
            "7+ years leading Vorem as a distributed-first company",
            "Production AI systems on Cloud Run — location-agnostic deployment",
            "Published author: structured async communication at scale",
        ],
        tone_modifier="remote-native, autonomous, systems-thinking",
    ),
}


def generate_tailored_cover_letter(
    role: str,
    company: str,
    location: str,
    jd_summary: str,
    match_score: int,
    gap_keywords: list[str],
) -> str:
    """
    Generate a 150-word brand-consistent cover letter tailored to the
    specific region and role context.

    Args:
        role:          Job title
        company:       Company name
        location:      Job location (used to detect region)
        jd_summary:    Key JD requirements extracted by Analyzer
        match_score:   Semantic match score (0-100)
        gap_keywords:  Skills to acknowledge or bridge in narrative

    Returns:
        150-word cover letter string
    """
    region = detect_region(location)
    config = REGION_CONFIGS[region]

    gaps_text = (
        f"Address these skill gaps naturally without over-explaining: {', '.join(gap_keywords)}"
        if gap_keywords else
        "The CV is a strong match. Lead with confidence."
    )

    system_prompt = f"""You are writing a cover letter on behalf of Rume Dominic, Senior AI Engineer
and Founder of Vorem. Tone: {config.tone_modifier}.
Rules:
- Exactly 150 words. Not 149, not 151.
- Never use the phrase "I am passionate about" or "I am a team player".
- Open with a specific hook tied to the company or role, not a generic statement.
- Weave in the primary emphasis naturally — do not list it mechanically.
- Close with a forward-looking sentence about impact, not a request to "discuss further".
- Sign off: Dominic Orume Uririe"""

    user_prompt = f"""
Role: {role}
Company: {company}
Location: {location} (Region detected: {region.value.upper()})
Match Score: {match_score}/100
JD Key Requirements: {jd_summary}

Primary narrative emphasis for this region:
{config.primary_emphasis}

Secondary emphasis:
{config.secondary_emphasis}

Proof points to reference (choose 1-2 most relevant):
{chr(10).join(f'- {p}' for p in config.proof_points)}

Visa note (include only if relevant to the role): {config.visa_note}

Gap handling: {gaps_text}

Write the 150-word cover letter now.
"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=400,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return response.content[0].text.strip()
```

---

<a name="skill-04"></a>
## Skill 04 — Post-Application Intelligence

### Purpose
48 hours after a confirmed application submission, this skill drafts a personalised
LinkedIn follow-up message to the hiring manager. It uses Claude API to compose a
message in the Rume Dominic brand voice: concise (under 300 characters for LinkedIn
connection note, or ~80 words for InMail), referencing the specific role, a genuine
insight about the company, and a clear but non-desperate call to action.

### Workflow

```
submission_log.db
      │
      │  Cron / scheduler polls every 6 hours
      ▼
CHECK: submitted_at < NOW() - 48h AND follow_up_sent = False
      │
      ▼
PostAppIntelligence.run(application_id)
      │
      ├── 1. Fetch application record (role, company, JD, CL used)
      ├── 2. Resolve hiring manager (name + LinkedIn URL from DB or web search)
      ├── 3. Fetch company recent news (1 relevant insight for personalisation)
      ├── 4. Generate follow-up message via Claude API
      ├── 5. Present to human for approval (Flask dashboard / Slack)
      └── 6. Upon approval → open LinkedIn DM and pre-fill message (Playwright)
               ↳ Human sends manually — NEVER auto-sends
```

### Python Implementation

```python
# skills/post_application.py

import sqlite3
import anthropic
from datetime import datetime, timedelta
from pathlib import Path

client = anthropic.Anthropic()
DB_PATH = Path(__file__).parent.parent / "db" / "submission_log.db"


def get_pending_follow_ups() -> list[dict]:
    """
    Query submission_log.db for applications submitted 48+ hours ago
    where follow-up has not yet been sent.
    """
    cutoff = datetime.utcnow() - timedelta(hours=48)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(
        """
        SELECT * FROM applications
        WHERE submitted = 1
          AND follow_up_sent = 0
          AND submitted_at <= ?
        """,
        (cutoff.isoformat(),),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def generate_follow_up_message(
    role: str,
    company: str,
    hiring_manager_name: str,
    company_insight: str,
    cover_letter_used: str,
) -> dict:
    """
    Generate two variants of a follow-up message:
    - 'connection_note': ≤300 chars (LinkedIn connection request note)
    - 'inmail': ~80 words (LinkedIn InMail or cold message)

    Returns dict with both variants.
    """
    system_prompt = """You write follow-up messages for Rume Dominic, Senior AI Engineer and
Founder of Vorem. Voice: confident, specific, not desperate. Never beg for a response.
Always reference something specific about the company or role.
Never use: 'I hope this message finds you well', 'reaching out', 'just following up'."""

    user_prompt = f"""
Application details:
- Role: {role}
- Company: {company}
- Hiring Manager: {hiring_manager_name or 'Hiring Manager'}
- Company recent insight: {company_insight or 'Leading organisation in the AI space.'}
- Cover letter opening used: {cover_letter_used[:200] if cover_letter_used else 'N/A'}

Write two follow-up messages:

1. CONNECTION_NOTE (max 300 characters — for LinkedIn connection request):
Must be highly specific, reference the role, and give a clear reason to connect.

2. INMAIL (max 80 words — for LinkedIn InMail or DM):
Personalised, references the company insight, acknowledges the application was
submitted, and ends with a single specific question or forward-looking statement.
Not a request to "discuss further" — be more precise.

Format your response exactly as:
CONNECTION_NOTE:
[text]

INMAIL:
[text]
"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=400,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = response.content[0].text.strip()

    # Parse the two sections
    result = {"connection_note": "", "inmail": ""}
    if "CONNECTION_NOTE:" in raw and "INMAIL:" in raw:
        parts = raw.split("INMAIL:")
        result["connection_note"] = parts[0].replace("CONNECTION_NOTE:", "").strip()
        result["inmail"] = parts[1].strip()
    else:
        result["inmail"] = raw

    return result


def mark_follow_up_drafted(app_id: int):
    """Mark application as having a follow-up drafted (pending human approval)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE applications SET follow_up_drafted = 1, follow_up_drafted_at = ? WHERE id = ?",
        (datetime.utcnow().isoformat(), app_id),
    )
    conn.commit()
    conn.close()


def mark_follow_up_sent(app_id: int):
    """Mark application follow-up as sent (after human approval and action)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE applications SET follow_up_sent = 1, follow_up_sent_at = ? WHERE id = ?",
        (datetime.utcnow().isoformat(), app_id),
    )
    conn.commit()
    conn.close()


async def run_follow_up_pipeline(notify_fn=None):
    """
    Main pipeline: check DB, generate follow-up messages for eligible
    applications, notify human for approval.
    """
    pending = get_pending_follow_ups()
    if not pending:
        return

    print(f"\n📬 {len(pending)} application(s) eligible for follow-up:")

    for app in pending:
        print(f"\n  → {app['role']} @ {app['company']}")

        messages = generate_follow_up_message(
            role=app["role"],
            company=app["company"],
            hiring_manager_name=app.get("hiring_manager_name", ""),
            company_insight=app.get("company_insight", ""),
            cover_letter_used=app.get("cover_letter_text", ""),
        )

        # Persist draft to DB for dashboard display
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """UPDATE applications
               SET follow_up_connection_note = ?,
                   follow_up_inmail = ?,
                   follow_up_drafted = 1,
                   follow_up_drafted_at = ?
               WHERE id = ?""",
            (
                messages["connection_note"],
                messages["inmail"],
                datetime.utcnow().isoformat(),
                app["id"],
            ),
        )
        conn.commit()
        conn.close()

        if notify_fn:
            await notify_fn({
                "type": "follow_up_ready",
                "app_id": app["id"],
                "role": app["role"],
                "company": app["company"],
                "connection_note": messages["connection_note"],
                "inmail": messages["inmail"],
            })

        print(f"     ✅ Follow-up drafted and queued for human approval.")
```

---

<a name="architecture"></a>
## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RUME DOMINIC JOB SEARCH AGENT                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │   Scraper    │───▶│   Analyzer   │───▶│  Tailoring Engine    │  │
│  │ Indeed/LI    │    │ Match Score  │    │  Dynamic by Region   │  │
│  │ Search API   │    │ Gap Analysis │    │  Claude claude-opus-4-6     │  │
│  └──────────────┘    └──────────────┘    └──────────┬───────────┘  │
│                                                      │              │
│                           ┌──────────────────────────▼───────────┐ │
│                           │    Human-in-the-Loop Gateway          │ │
│                           │    Flask Dashboard / Slack Webhook    │ │
│                           │    ✅ Approve  |  ❌ Reject          │ │
│                           └──────────────────────────┬───────────┘ │
│                                                      │              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────▼───────────┐  │
│  │ Follow-Up    │◀───│ submission   │◀───│  Stealth Playwright   │  │
│  │ Intelligence │    │  _log.db     │    │  Form Fill + Upload   │  │
│  │ (48h cron)   │    │  SQLite      │    │  Skills 01 + 02       │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

<a name="environment"></a>
## Python Environment

### `requirements.txt`

```
# Core
anthropic>=0.30.0
playwright>=1.43.0
flask>=3.0.0
flask-cors>=4.0.0

# Database
# SQLite is stdlib — no additional package needed

# Scheduling (follow-up 48h cron)
apscheduler>=3.10.0

# Utilities
python-dotenv>=1.0.0
python-slugify>=8.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0

# Notifications
slack-sdk>=3.27.0        # Optional: Slack webhook approval flow
```

### `.env` template

```bash
# Claude API
ANTHROPIC_API_KEY=your_key_here

# Candidate
CANDIDATE_EMAIL=orumedominic@gmail.com
CANDIDATE_CV_PATH=/Users/user/job app/prompt engineer DOMINIC ORUME URIRIE (1).pdf

# Slack (optional)
SLACK_WEBHOOK_URL=your_slack_webhook_url

# Flask
FLASK_SECRET_KEY=change_this_to_a_random_string
FLASK_PORT=5050

# Indeed API (optional — scraper fallback to Playwright if absent)
INDEED_API_KEY=
```

### Setup

```bash
cd "/Users/user/job app/agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.template .env
# → edit .env and add your ANTHROPIC_API_KEY
```

---

<a name="brand-voice"></a>
## Brand Voice Prompt Template

This is the master system prompt injected into every Claude API call that
generates content on behalf of Rume Dominic. It is the single source of truth
for voice, tone, and identity.

```python
# templates/brand_voice_prompt.py

BRAND_VOICE_SYSTEM_PROMPT = """
# IDENTITY
You are writing as Rume Dominic (full legal name: Dominic Orume Uririe).
He is a Nigerian-born Senior AI Engineer, Founder, Author, and Business Strategist
based in Birmingham, England, United Kingdom.

# CORE IDENTITY PILLARS
1. Founder & Lead Strategist, Vorem Limited (est. 2017) — digital education and technology.
   Vorem is not a side project. It is a 7-year body of work in building scalable systems.
2. MSc Artificial Intelligence & Business Strategy (Distinction) — Aston University, 2025–2026.
   This is not credential-collecting. It is the academic grounding for his next chapter.
3. Author of 5 published books — structured, intellectual, long-form thought leadership.
4. Speaker at FrontierTechX — peer-recognised voice at the frontier of AI strategy.
5. Certified Blockchain Architect — Secure & Distributed Systems.
6. AI Engineer at Micki Solutions (Nov 2025–Present): production AI systems, 91+ reliability.
7. AI Engineer & Growth Consultant at Simeria (Dec 2025–Present): multi-channel AI automation.

# TONE
- Professional and visionary — he sees where AI is going and builds toward it
- Grounded in practical outcomes — never abstract; always tied to real systems or results
- Founder-energy — he has built, shipped, led, and iterated. Not theoretical.
- Resilient — Nigerian-born, built Vorem through constraint. Does not need to explain himself.
- Never desperate or generic. Never says "passionate about", "team player", "hard worker".

# WRITING RULES
1. Open with a specific hook — a fact, a result, or a sharp observation. Never a platitude.
2. Connect AI engineering to business strategy in every piece. This is his signature.
3. Reference at least one specific project, achievement, or credential per piece.
4. Never list skills mechanically. Weave them into a narrative.
5. Close with forward momentum — what he will do, not what he wants to discuss.
6. Word count discipline: cover letters = 150 words. Form answers = max 120 words.
   Follow-up InMails = max 80 words. Connection notes = max 300 characters.
7. Sign off always: Dominic Orume Uririe (not "Rume" in formal documents).

# WHAT TO AVOID
- "I am passionate about technology"
- "I am a results-driven professional"
- "I have always been interested in"
- "I look forward to hearing from you"
- "Please find attached my CV"
- Any phrase that could appear on 1,000 other applications

# REGION MODIFIERS (applied on top of base voice)
- UK: foreground MSc + Global Talent Visa eligibility + UK production credentials
- Europe: foreground international leadership + Vorem cross-border operations
- Canada: foreground founder resilience + scalable system delivery
- Australia: foreground enterprise AI delivery + Blockchain/DeFi expertise
- USA: foreground thought leadership + business ROI + O-1A extraordinary ability track
- Remote: foreground distributed-first leadership + cloud-native stack
"""
```

---

*End of Skills.md — Rume Dominic Job Search Agent v1.0.0*
