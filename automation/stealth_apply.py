"""
Stealth Application Automation — Rume Dominic Job Search Agent
=============================================================
Uses Playwright with human-like interaction patterns to pre-fill job
application forms. NEVER submits automatically — always pauses for
human confirmation before the final submit action.

Usage:
    python stealth_apply.py --url "https://to.indeed.com/aapxg2fzcqx7" --role "AI Architect" --company "Datacom"

Requirements:
    pip install playwright python-slugify
    playwright install chromium
"""

import asyncio
import random
import time
import argparse
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright, Page
except ImportError:
    print("ERROR: Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

from config import CANDIDATE, STEALTH, REQUIRE_HUMAN_CONFIRMATION


# ---------------------------------------------------------------------------
# Human-like interaction helpers
# ---------------------------------------------------------------------------

async def human_delay(min_ms: int = None, max_ms: int = None):
    """Random pause to simulate human think time."""
    lo = min_ms or STEALTH["action_pause_min"] * 1000
    hi = max_ms or STEALTH["action_pause_max"] * 1000
    await asyncio.sleep(random.uniform(lo, hi) / 1000)


async def human_type(page: Page, selector: str, text: str):
    """Type text character by character with random delays."""
    await page.click(selector)
    await human_delay(200, 500)
    for char in text:
        await page.keyboard.type(char)
        delay = random.uniform(STEALTH["min_delay_ms"], STEALTH["max_delay_ms"]) / 1000
        await asyncio.sleep(delay)
    await human_delay(300, 700)


async def safe_fill(page: Page, selector: str, value: str, label: str = ""):
    """Fill a field if it exists, skip silently if not found."""
    try:
        element = await page.query_selector(selector)
        if element:
            await element.scroll_into_view_if_needed()
            await human_delay(400, 900)
            await element.click()
            await page.keyboard.press("Control+A")
            await page.keyboard.press("Delete")
            await human_type(page, selector, value)
            print(f"  ✅ Filled: {label or selector}")
        else:
            print(f"  ⚠️  Not found: {label or selector}")
    except Exception as e:
        print(f"  ❌ Error filling {label}: {e}")


async def safe_upload(page: Page, selector: str, file_path: str):
    """Upload a file to an input[type=file] element."""
    try:
        if not Path(file_path).exists():
            print(f"  ❌ CV file not found: {file_path}")
            return
        await page.set_input_files(selector, file_path)
        await human_delay(1000, 2000)
        print(f"  ✅ Uploaded CV: {file_path}")
    except Exception as e:
        print(f"  ❌ Error uploading CV: {e}")


# ---------------------------------------------------------------------------
# Site-specific form fillers
# ---------------------------------------------------------------------------

async def fill_indeed(page: Page):
    """Fill Indeed Easy Apply forms."""
    print("\n[Indeed] Filling application form...")

    # Name fields
    await safe_fill(page, 'input[name="applicant.name"]', CANDIDATE["full_name"], "Full Name")
    await safe_fill(page, 'input[id*="firstName"], input[name*="firstName"]', CANDIDATE["first_name"], "First Name")
    await safe_fill(page, 'input[id*="lastName"], input[name*="lastName"]', CANDIDATE["last_name"], "Last Name")

    # Contact
    await safe_fill(page, 'input[name="applicant.phoneNumber"], input[id*="phone"]', CANDIDATE["phone"], "Phone")
    await safe_fill(page, 'input[name="applicant.email"], input[type="email"]', CANDIDATE["email"], "Email")

    # Location
    await safe_fill(page, 'input[id*="location"], input[name*="location"]', CANDIDATE["location"], "Location")

    # CV Upload
    await safe_upload(page, 'input[type="file"]', CANDIDATE["cv_path"])

    # Experience / years
    await safe_fill(page, 'input[id*="years"], input[name*="yearsExperience"]', CANDIDATE["years_experience"], "Years Experience")

    # Salary
    await safe_fill(page, 'input[id*="salary"], input[name*="salary"]', CANDIDATE["salary_expectation_gbp"], "Salary Expectation")

    print("[Indeed] Form pre-fill complete.")


async def fill_workday(page: Page):
    """Fill Workday application forms."""
    print("\n[Workday] Filling application form...")

    await safe_fill(page, 'input[data-automation-id="legalNameSection_firstName"]', CANDIDATE["first_name"], "First Name")
    await safe_fill(page, 'input[data-automation-id="legalNameSection_lastName"]', CANDIDATE["last_name"], "Last Name")
    await safe_fill(page, 'input[data-automation-id="email"]', CANDIDATE["email"], "Email")
    await safe_fill(page, 'input[data-automation-id="phone"]', CANDIDATE["phone"], "Phone")
    await safe_fill(page, 'input[data-automation-id="addressSection_city"]', "Birmingham", "City")

    await safe_upload(page, 'input[type="file"]', CANDIDATE["cv_path"])
    print("[Workday] Form pre-fill complete.")


async def fill_greenhouse(page: Page):
    """Fill Greenhouse application forms."""
    print("\n[Greenhouse] Filling application form...")

    await safe_fill(page, '#first_name', CANDIDATE["first_name"], "First Name")
    await safe_fill(page, '#last_name', CANDIDATE["last_name"], "Last Name")
    await safe_fill(page, '#email', CANDIDATE["email"], "Email")
    await safe_fill(page, '#phone', CANDIDATE["phone"], "Phone")
    await safe_fill(page, 'input[name="job_application[location]"]', CANDIDATE["location"], "Location")

    await safe_upload(page, 'input[type="file"]', CANDIDATE["cv_path"])
    print("[Greenhouse] Form pre-fill complete.")


async def fill_lever(page: Page):
    """Fill Lever application forms."""
    print("\n[Lever] Filling application form...")

    await safe_fill(page, 'input[name="name"]', CANDIDATE["full_name"], "Full Name")
    await safe_fill(page, 'input[name="email"]', CANDIDATE["email"], "Email")
    await safe_fill(page, 'input[name="phone"]', CANDIDATE["phone"], "Phone")
    await safe_fill(page, 'input[name="location"]', CANDIDATE["location"], "Location")
    await safe_fill(page, 'input[name="urls[LinkedIn]"]', CANDIDATE["linkedin"], "LinkedIn")

    await safe_upload(page, 'input[type="file"]', CANDIDATE["cv_path"])
    print("[Lever] Form pre-fill complete.")


async def fill_generic(page: Page):
    """Best-effort generic form filler for unknown portals."""
    print("\n[Generic] Attempting best-effort form fill...")

    field_map = {
        'input[type="text"][name*="name" i], input[placeholder*="name" i]': CANDIDATE["full_name"],
        'input[type="email"], input[name*="email" i]': CANDIDATE["email"],
        'input[type="tel"], input[name*="phone" i], input[placeholder*="phone" i]': CANDIDATE["phone"],
        'input[name*="location" i], input[placeholder*="location" i]': CANDIDATE["location"],
        'input[name*="linkedin" i], input[placeholder*="linkedin" i]': CANDIDATE["linkedin"],
        'input[name*="salary" i], input[placeholder*="salary" i]': CANDIDATE["salary_expectation_gbp"],
    }

    for selector, value in field_map.items():
        if value:
            await safe_fill(page, selector, value, selector[:40])

    await safe_upload(page, 'input[type="file"]', CANDIDATE["cv_path"])
    print("[Generic] Best-effort fill complete.")


def detect_platform(url: str) -> str:
    """Detect ATS platform from URL."""
    url_lower = url.lower()
    if "indeed.com" in url_lower or "to.indeed.com" in url_lower:
        return "indeed"
    if "myworkdayjobs.com" in url_lower or "workday.com" in url_lower:
        return "workday"
    if "greenhouse.io" in url_lower or "boards.greenhouse.io" in url_lower:
        return "greenhouse"
    if "jobs.lever.co" in url_lower:
        return "lever"
    return "generic"


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

async def apply_to_role(url: str, role: str, company: str):
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  RUME DOMINIC — STEALTH APPLY AGENT                      ║
╠══════════════════════════════════════════════════════════╣
║  Role    : {role[:48].ljust(48)} ║
║  Company : {company[:48].ljust(48)} ║
║  Email   : {CANDIDATE['email'].ljust(48)} ║
╚══════════════════════════════════════════════════════════╝
  ⚠️  HUMAN-IN-THE-LOOP ACTIVE — Auto-submit is DISABLED
""")

    platform = detect_platform(url)
    print(f"Platform detected: {platform.upper()}")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=STEALTH["headless"],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
            ]
        )

        context = await browser.new_context(
            viewport=STEALTH["viewport"],
            user_agent=STEALTH["user_agent"],
            locale="en-GB",
            timezone_id="Europe/London",
        )

        # Remove webdriver flag
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
        """)

        page = await context.new_page()

        print(f"\nNavigating to: {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await human_delay(1500, 3000)

        # Platform-specific fill
        fillers = {
            "indeed": fill_indeed,
            "workday": fill_workday,
            "greenhouse": fill_greenhouse,
            "lever": fill_lever,
            "generic": fill_generic,
        }
        await fillers[platform](page)

        # ── HUMAN CONFIRMATION GATE ──────────────────────────────────────
        print("""
╔══════════════════════════════════════════════════════════╗
║  ✋  HUMAN REVIEW REQUIRED                               ║
║                                                          ║
║  The browser is open and pre-filled.                     ║
║  Please:                                                 ║
║    1. Review all fields for accuracy                     ║
║    2. Add/edit cover letter if prompted                  ║
║    3. Click SUBMIT yourself when ready                   ║
║                                                          ║
║  Press ENTER here only to CLOSE the browser after you   ║
║  have finished (submitted or abandoned).                 ║
╚══════════════════════════════════════════════════════════╝
""")
        input("  → Press ENTER to close browser: ")
        await browser.close()
        print("\n✅ Session closed. Update your tracker dashboard.")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rume Dominic — Stealth Job Application Agent")
    parser.add_argument("--url", required=True, help="Job application URL")
    parser.add_argument("--role", default="AI Engineer", help="Role title")
    parser.add_argument("--company", default="Company", help="Company name")
    args = parser.parse_args()

    asyncio.run(apply_to_role(args.url, args.role, args.company))
