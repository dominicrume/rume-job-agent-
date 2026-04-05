#!/bin/bash
set -e
echo "═══════════════════════════════════════════════════"
echo " Rume Dominic Job Search Agent — Full Setup"
echo "═══════════════════════════════════════════════════"

cd "$(dirname "$0")"

python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q -r requirements.txt

echo "Installing Playwright Chromium browser..."
playwright install chromium

echo "Initialising database..."
python db/init_db.py

if [ ! -f .env ]; then
  cp .env.template .env
  echo ""
  echo "⚠️  .env file created from template."
  echo "    Add your ANTHROPIC_API_KEY to .env before running the agent."
fi

echo ""
echo "✅ Setup complete."
echo ""
echo "Next steps:"
echo "  1. Edit .env → add ANTHROPIC_API_KEY"
echo "  2. source venv/bin/activate"
echo "  3. python dashboard/app.py          ← start approval dashboard"
echo "  4. python skills/post_application.py ← run follow-up checker"
echo ""
echo "Apply to your top role (AI Architect, 78/100):"
echo "  python ../automation/stealth_apply.py \\"
echo "    --url 'https://to.indeed.com/aapxg2fzcqx7' \\"
echo "    --role 'AI Architect' --company 'Datacom Connect'"
