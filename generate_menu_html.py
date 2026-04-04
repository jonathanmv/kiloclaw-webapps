#!/usr/bin/env python3
"""Generate static index.html from weekly menu markdown — Airbnb-inspired design."""
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

# Airbnb-inspired color palette
AIRBNB_RED = '#ff385c'
AIRBNB_DARK = '#222222'
AIRBNB_SECONDARY = '#6a6a6a'
AIRBNB_LIGHT_SURFACE = '#f2f2f2'
AIRBNB_WHITE = '#ffffff'

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Week {week} — Family Menu</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#ff385c">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Family Menu">
    <link rel="apple-touch-icon" href="/favicon.svg">
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
    <style>
        :root {{
            --red: #ff385c;
            --dark: #222222;
            --secondary: #6a6a6a;
            --surface: #f2f2f2;
            --white: #ffffff;
            --shadow-card: rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px, rgba(0,0,0,0.10) 0px 4px 8px;
            --shadow-hover: rgba(0,0,0,0.08) 0px 4px 12px;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--white);
            color: var(--dark);
            min-height: 100vh;
        }}

        /* ── Header ── */
        .header {{
            background: var(--white);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid rgba(0,0,0,0.06);
            padding: 0 24px;
        }}
        .header-inner {{
            max-width: 1100px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 64px;
        }}
        .logo {{
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: var(--dark);
        }}
        .logo-icon {{
            width: 32px;
            height: 32px;
            background: var(--red);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
        }}
        .logo-text {{
            font-size: 15px;
            font-weight: 600;
            letter-spacing: -0.18px;
        }}
        .header-badge {{
            background: var(--surface);
            color: var(--dark);
            font-size: 12px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 20px;
            letter-spacing: 0;
        }}

        /* ── Hero ── */
        .hero {{
            background: linear-gradient(135deg, #fff5f7 0%, #fff 100%);
            padding: 48px 24px 40px;
            text-align: center;
            border-bottom: 1px solid rgba(0,0,0,0.04);
        }}
        .hero-emoji {{
            font-size: 48px;
            margin-bottom: 12px;
            display: block;
        }}
        .hero h1 {{
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.44px;
            color: var(--dark);
            margin-bottom: 8px;
        }}
        .hero p {{
            font-size: 15px;
            color: var(--secondary);
            font-weight: 400;
        }}

        /* ── Day filter pills ── */
        .day-filter {{
            display: flex;
            gap: 8px;
            padding: 16px 24px;
            overflow-x: auto;
            justify-content: center;
            flex-wrap: wrap;
            background: var(--white);
            position: sticky;
            top: 64px;
            z-index: 90;
            border-bottom: 1px solid rgba(0,0,0,0.06);
        }}
        .day-filter::-webkit-scrollbar {{ display: none; }}
        .day-pill {{
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
            border: 1px solid rgba(0,0,0,0.08);
            background: var(--white);
            color: var(--secondary);
        }}
        .day-pill:hover {{
            border-color: var(--dark);
            color: var(--dark);
        }}
        .day-pill.active {{
            background: var(--dark);
            color: var(--white);
            border-color: var(--dark);
        }}

        /* ── Main content ── */
        .content {{
            max-width: 900px;
            margin: 0 auto;
            padding: 32px 24px 64px;
        }}

        /* ── Day section ── */
        .day-section {{
            margin-bottom: 40px;
            scroll-margin-top: 160px;
        }}
        .day-section.hidden {{ display: none; }}
        .day-heading {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
        }}
        .day-heading .icon {{ font-size: 22px; }}
        .day-heading .name {{
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.44px;
            color: var(--dark);
        }}
        .day-heading .today-tag {{
            background: var(--red);
            color: white;
            font-size: 10px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* ── Event banner (no-cooking etc.) ── */
        .event-banner {{
            background: linear-gradient(135deg, #fff5f7, #fff);
            border: 1px solid rgba(255,56,92,0.15);
            border-radius: 12px;
            padding: 20px 24px;
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 16px;
        }}
        .event-banner .event-icon {{ font-size: 28px; }}
        .event-banner .event-text {{
            font-size: 15px;
            font-weight: 600;
            color: var(--dark);
        }}
        .event-banner .event-sub {{
            font-size: 13px;
            color: var(--secondary);
            margin-top: 2px;
        }}

        /* ── Meal cards ── */
        .meals-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 12px;
        }}
        .meal-card {{
            background: var(--white);
            border-radius: 16px;
            padding: 20px;
            box-shadow: var(--shadow-card);
            transition: box-shadow 0.2s ease;
        }}
        .meal-card:hover {{
            box-shadow: var(--shadow-hover);
        }}
        .meal-card-label {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--red);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .meal-card-items {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .meal-card-items li {{
            font-size: 14px;
            font-weight: 400;
            color: var(--dark);
            line-height: 1.4;
            padding-left: 14px;
            position: relative;
        }}
        .meal-card-items li::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 7px;
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: var(--red);
            opacity: 0.6;
        }}

        /* ── Footer ── */
        .footer {{
            text-align: center;
            padding: 24px;
            font-size: 12px;
            color: #b0b0b0;
            border-top: 1px solid rgba(0,0,0,0.04);
        }}
        .footer span {{ color: var(--red); }}

        /* ── Responsive ── */
        @media (max-width: 600px) {{
            .hero h1 {{ font-size: 22px; }}
            .header-inner {{ padding: 0; }}
            .logo-text {{ display: none; }}
            .content {{ padding: 20px 16px 48px; }}
            .meals-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header class="header">
        <div class="header-inner">
            <a class="logo" href="#">
                <div class="logo-icon">🍽️</div>
                <span class="logo-text">Family Menu</span>
            </a>
            <span class="header-badge">Week {week}</span>
        </div>
    </header>

    <!-- Hero -->
    <section class="hero">
        <span class="hero-emoji">🍴</span>
        <h1>Weekly Meal Plan</h1>
        <p>Week {week} — What's cooking in our kitchen</p>
    </section>

    <!-- Day filter pills -->
    <nav class="day-filter" id="dayFilter">
        <button class="day-pill active" data-day="all">All days</button>
        {day_pills}
    </nav>

    <!-- Content -->
    <main class="content">
        {days_html}
    </main>

    <!-- Footer -->
    <footer class="footer">
        Made with <span>♥</span> by Bob · OpenClaw Family Kitchen · Week {week}
    </footer>

    <script>
        // Highlight today's card
        const todayName = new Date().toLocaleDateString('en-US', {{weekday: 'long'}});
        const todaySection = document.querySelector(`[data-day-name="{today_name}"]`);
        if (todaySection) {{
            todaySection.scrollIntoView({{behavior: 'smooth', block: 'start'}});
            const tag = document.createElement('span');
            tag.className = 'today-tag';
            tag.textContent = 'Today';
            todaySection.querySelector('.day-heading').appendChild(tag);
        }}

        // Filter pills
        const pills = document.querySelectorAll('.day-pill');
        const sections = document.querySelectorAll('.day-section[data-day-name]');
        pills.forEach(pill => {{
            pill.addEventListener('click', () => {{
                pills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                const selected = pill.dataset.day;
                sections.forEach(sec => {{
                    sec.classList.toggle('hidden', selected !== 'all' && sec.dataset.dayName !== selected);
                }});
            }});
        }});
    </script>
</body>
</html>"""

DAY_PILL_TEMPLATE = '<button class="day-pill" data-day="{day_name}">{icon} {day_name}</button>'

EVENT_BANNER = """
        <div class="event-banner">
            <span class="event-icon">🎉</span>
            <div>
                <div class="event-text">{text}</div>
            </div>
        </div>"""

MEAL_CARD_TEMPLATE = """
        <div class="meal-card">
            <div class="meal-card-label">{meal_icon} {meal_name}</div>
            <ul class="meal-card-items">
                {items_html}
            </ul>
        </div>"""

def parse_menu(content):
    """Returns a dict: { day_name: { 'event': None|'text', 'meals': { meal_name: [items] } } }"""
    days = {}
    current_day = None
    current_meal = None
    for line in content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('## '):
            current_day = line[3:].strip()
            current_meal = None
            if current_day not in days:
                days[current_day] = {'event': None, 'meals': {}}
        elif line.startswith('- 🎉') and current_day:
            days[current_day]['event'] = line[4:].strip().strip('*')
        elif line.startswith('**') and current_day:
            current_meal = line.strip('*')
            days[current_day]['meals'][current_meal] = []
        elif line.startswith('- ') and current_day and current_meal:
            days[current_day]['meals'][current_meal].append(line[2:].strip())
    return days

MEAL_ICONS = {
    'Breakfast': '☀️',
    'Lunch':     '🌅',
    'Dinner':    '🌙',
    'Snack':     '🍎',
    'Brunch':    '🍳',
}

def render_day(day_name, day_data):
    icon = DAY_ICONS.get(day_name, '📅')

    # Event banner
    event_html = ''
    if day_data.get('event'):
        event_html = EVENT_BANNER.format(text=day_data['event'])

    # Meal cards
    meals_html = ''
    for meal_name, items in day_data['meals'].items():
        if not items:
            continue
        meal_icon = MEAL_ICONS.get(meal_name, '🍽️')
        items_html = ''.join(f'<li>{item}</li>' for item in items)
        meals_html += MEAL_CARD_TEMPLATE.format(
            meal_icon=meal_icon,
            meal_name=meal_name,
            items_html=items_html
        )

    if not meals_html and not event_html:
        return ''

    return f"""
        <section class="day-section" data-day-name="{day_name}" id="day-{day_name.lower()}">
            <div class="day-heading">
                <span class="icon">{icon}</span>
                <span class="name">{day_name}</span>
            </div>
            {event_html}
            <div class="meals-grid">{meals_html}</div>
        </section>"""

def main():
    path, week = get_current_week_file()
    if not os.path.exists(path):
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        content = f.read()

    days = parse_menu(content)

    # Build day pills
    day_pills = ''.join(
        DAY_PILL_TEMPLATE.format(day_name=name, icon=DAY_ICONS.get(name, '📅'))
        for name in days
    )

    # Build day sections
    days_html = ''.join(
        render_day(name, data) for name, data in days.items()
    )

    # Today's day name for scroll targeting
    today_name = datetime.date.today().strftime('%A')

    html = HTML_TEMPLATE.format(
        week=week,
        day_pills=day_pills,
        days_html=days_html,
        today_name=today_name,
    )

    out_path = '/root/.openclaw/workspace/kiloclaw-webapps/index.html'
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"Generated {out_path} ({len(html):,} bytes)")

if __name__ == '__main__':
    main()