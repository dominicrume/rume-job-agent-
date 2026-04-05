"""
Candidate configuration — single source of truth for all form filling.
"""

CANDIDATE = {
    "first_name": "Dominic",
    "last_name": "Orume Uririe",
    "full_name": "Dominic Orume Uririe",
    "email": "orumedominic@gmail.com",
    "phone": "+44 7402 830 944",
    "location": "Birmingham, England, United Kingdom",
    "linkedin": "",           # Add LinkedIn URL here
    "portfolio": "",          # Add portfolio/website URL here
    "cv_path": "/Users/user/job app/prompt engineer DOMINIC ORUME URIRIE (1).pdf",
    "headline": "Senior AI Engineer | Prompt Engineering · Agentic Workflows · GenAI",
    "notice_period": "Negotiable",
    "right_to_work_uk": True,
    "requires_sponsorship": False,
    "salary_expectation_gbp": "90000-130000",
    "salary_expectation_aud": "120000-150000",
    "years_experience": "7+",
}

# Human-in-the-loop: always True — no auto-submission ever
REQUIRE_HUMAN_CONFIRMATION = True

# Stealth settings
STEALTH = {
    "min_delay_ms": 80,     # min typing delay per character
    "max_delay_ms": 220,    # max typing delay per character
    "action_pause_min": 0.8,  # seconds between major actions
    "action_pause_max": 2.5,
    "headless": False,      # Always visible — you review before submitting
    "viewport": {"width": 1440, "height": 900},
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}
