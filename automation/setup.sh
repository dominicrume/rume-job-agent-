#!/bin/bash
# Setup script for Rume Dominic Job Application Automation
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Installing Playwright browsers..."
playwright install chromium
echo ""
echo "✅ Setup complete. Usage:"
echo ""
echo "  # Apply to AI Architect role at Datacom (highest match: 78/100)"
echo "  python stealth_apply.py --url 'https://to.indeed.com/aapxg2fzcqx7' --role 'AI Architect' --company 'Datacom Connect'"
echo ""
echo "  # Apply to CTO role at Jar Pay"
echo "  python stealth_apply.py --url 'https://to.indeed.com/aand6f2fj2rz' --role 'Chief Technical Officer' --company 'Jar Pay Trading'"
echo ""
echo "  # Apply to Binance Lead Security Engineer"
echo "  python stealth_apply.py --url 'https://to.indeed.com/aammt6x4sppy' --role 'Lead Security Engineer' --company 'Binance'"
