#!/usr/bin/env python3
"""Generate static index.html from weekly menu markdown."""
import datetime, re, sys, os

MENU_DIR = '/root/.openclaw/workspace'

def get_current_week_file():
    today = datetime.date.today()
    week = today.isocalendar()[1]
    filename = f"weekly_menu_w{week}.md"
    path = os.path.join(MENU_DIR, filename)
    return path, week

DAY_ICONS = {
    'Monday': '🌙', 'Tuesday': '🌅', 'Wednesday': '☀️',
    'Thursday': '🌤️', 'Friday': '🌻', 'Saturday': '🌴', 'Sunday': '📅'
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Week {week} — Family Menu</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f7f7f7; color: #222; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 2rem; }}
        header {{ text-align: center; margin-bottom: 2rem; }}
        h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .week-badge {{ background: #e0f0e8; color: #2a7a4a; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }}
        .day-card {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
        .day-card.today {{ border: 2px solid #4caf50; }}
        .day-header {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem; }}
        .day-header .emoji {{ font-size: 1.4rem; }}
        .today .day-header::after {{ content: 'TODAY'; background: #4caf50; color: white; font-size: 0.6rem; padding: 2px 6px; border-radius: 4px; }}
        .meal-section {{ margin-bottom: 1rem; }}
        .meal-section:last-child {{ margin-bottom: 0; }}
        .meal-label {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #888; font-weight: 700; margin-bottom: 0.3rem; }}
        .meal-items {{ list-style: none; }}
        .meal-items li {{ padding: 0.25rem 0; color: #333; }}
        .meal-items li::before {{ content: '•'; color: #4caf50; font-weight: bold; margin-right: 0.5rem; }}
        .note {{ background: #fff8e1; border-left: 3px solid #ffc107; padding: 0.5rem 0.8rem; border-radius: 0 6px 6px 0; font-size: 0.85rem; margin-bottom: 0.8rem; }}
        .footer {{ text-align: center; margin-top: 2rem; font-size: 0.75rem; color: #aaa; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🍽️ Weekly Menu</h1>
            <span class="week-badge">Week {week}</span>
        </header>
        {days_html}
        <div class="footer">OpenClaw Family Kitchen — Week {week}</div>
    </div>
</body>
</html>"""

DAY_CARD_TEMPLATE = """
        <div class="day-card{today_class}">
            <div class="day-header">
                <span class="emoji">{icon}</span>
                {day_name}
            </div>
            {note_html}
            {meals_html}
        </div>"""

def parse_menu(content):
    days = {}
    current_day = None
    current_section = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## '):
            current_day = line[3:].strip()
            current_section = None
            if current_day not in days:
                days[current_day] = {'notes': '', 'meals': {}}
        elif line.startswith('**') and current_day:
            current_section = line.strip('*')
            days[current_day]['meals'][current_section] = []
        elif line.startswith('- ') and current_day and current_section:
            days[current_day]['meals'][current_section].append(line[2:].strip())
        elif line.startswith('- 🎉') and current_day:
            days[current_day]['notes'] = line[4:].strip().strip('*')
    return days

def render_day(day_name, day_data, is_today):
    icon = DAY_ICONS.get(day_name, '📅')
    today_class = ' today' if is_today else ''
    note_html = f'<div class="note">{day_data["notes"]}</div>' if day_data['notes'] else ''
    meals_html = ''
    for meal_name, items in day_data['meals'].items():
        items_html = ''.join(f'<li>{item}</li>' for item in items)
        meals_html += f'''
            <div class="meal-section">
                <div class="meal-label">{meal_name}</div>
                <ul class="meal-items">{items_html}</ul>
            </div>'''
    return DAY_CARD_TEMPLATE.format(
        today_class=today_class, icon=icon, day_name=day_name,
        note_html=note_html, meals_html=meals_html
    )

def main():
    path, week = get_current_week_file()
    if not os.path.exists(path):
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        content = f.read()
    days = parse_menu(content)
    today_name = datetime.date.today().strftime('%A')
    days_html = ''
    for day_name, day_data in days.items():
        is_today = (day_name == today_name)
        days_html += render_day(day_name, day_data, is_today)
    html = HTML_TEMPLATE.format(week=week, days_html=days_html)
    out_path = os.path.join(MENU_DIR, 'index.html')
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"Generated {out_path}")

if __name__ == '__main__':
    main()
