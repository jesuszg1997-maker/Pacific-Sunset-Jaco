from __future__ import annotations

import calendar
from datetime import date, timedelta

import streamlit as st


st.set_page_config(
    page_title="Pacific Sunset Jaco",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="collapsed",
)


PHOTOS = [
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=85",
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=85",
    "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=1200&q=85",
]

MONTH_NAMES = list(calendar.month_name)
WEEKDAY_LABELS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]


def add_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --paper: #fbfaf7;
                --ink: #1d2525;
                --muted: #65706f;
                --line: #e5e0d8;
                --accent: #0f766e;
                --accent-soft: #d8efeb;
                --sun: #d88c3a;
            }

            .stApp {
                background:
                    radial-gradient(circle at 12% 8%, rgba(216, 140, 58, 0.08), transparent 28rem),
                    linear-gradient(180deg, #fffdf9 0%, var(--paper) 100%);
                color: var(--ink);
            }

            .block-container {
                max-width: 1180px;
                padding: 2.25rem 2rem 3rem;
            }

            div[data-testid="stToolbar"],
            div[data-testid="stDecoration"],
            div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0;
                position: fixed;
            }

            .photo-strip {
                display: grid;
                grid-template-columns: 1.35fr 0.85fr 0.85fr;
                gap: 0.75rem;
                min-height: 330px;
                margin-bottom: 2rem;
            }

            .photo-card {
                min-height: 330px;
                border-radius: 8px;
                background-position: center;
                background-size: cover;
                box-shadow: 0 18px 55px rgba(38, 48, 49, 0.12);
                overflow: hidden;
                position: relative;
            }

            .photo-card:first-child {
                min-height: 430px;
            }

            .photo-card::after {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(180deg, transparent 45%, rgba(0, 0, 0, 0.28));
            }

            .title-row {
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                gap: 1.5rem;
                margin: 0 0 1.5rem;
            }

            .eyebrow {
                color: var(--accent);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.08rem;
                margin-bottom: 0.35rem;
                text-transform: uppercase;
            }

            .page-title {
                color: var(--ink);
                font-size: clamp(2.3rem, 5vw, 4.8rem);
                font-weight: 650;
                letter-spacing: 0;
                line-height: 0.96;
                margin: 0;
            }

            .subtitle {
                color: var(--muted);
                font-size: 1.05rem;
                line-height: 1.65;
                margin: 0;
                max-width: 33rem;
            }

            .info-grid {
                border-bottom: 1px solid var(--line);
                border-top: 1px solid var(--line);
                display: grid;
                gap: 0;
                grid-template-columns: repeat(4, 1fr);
                margin: 1.5rem 0 3rem;
            }

            .info-item {
                border-right: 1px solid var(--line);
                padding: 1.15rem 1.25rem;
            }

            .info-item:last-child {
                border-right: 0;
            }

            .info-value {
                color: var(--ink);
                font-size: 1.35rem;
                font-weight: 650;
                line-height: 1.1;
                margin-bottom: 0.3rem;
            }

            .info-label {
                color: var(--muted);
                font-size: 0.9rem;
            }

            .section-kicker {
                color: var(--accent);
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.08rem;
                margin-bottom: 0.4rem;
                text-transform: uppercase;
            }

            .calendar-shell {
                border-top: 1px solid var(--line);
                padding-top: 2rem;
            }

            .calendar-heading {
                align-items: center;
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                margin-bottom: 1rem;
            }

            .calendar-title {
                color: var(--ink);
                font-size: 2rem;
                font-weight: 650;
                letter-spacing: 0;
                margin: 0;
            }

            .selected-date {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 8px;
                color: var(--ink);
                font-weight: 600;
                padding: 0.75rem 1rem;
                text-align: right;
            }

            .calendar-weekdays,
            .calendar-grid {
                display: grid;
                gap: 0.45rem;
                grid-template-columns: repeat(7, minmax(0, 1fr));
            }

            .weekday {
                color: var(--muted);
                font-size: 0.78rem;
                font-weight: 700;
                padding: 0.35rem 0;
                text-align: center;
                text-transform: uppercase;
            }

            .calendar-cell {
                align-items: center;
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 8px;
                color: var(--muted);
                display: flex;
                justify-content: center;
                min-height: 3.25rem;
            }

            .calendar-cell.is-selected {
                background: var(--accent-soft);
                border-color: var(--accent);
                color: var(--ink);
                font-weight: 700;
            }

            div[data-testid="stButton"] > button {
                border-radius: 8px;
                border: 1px solid var(--line);
                box-shadow: none;
                color: var(--ink);
                font-weight: 650;
                min-height: 3.25rem;
                transition: 140ms ease;
                width: 100%;
            }

            div[data-testid="stButton"] > button:hover {
                border-color: var(--accent);
                color: var(--accent);
                transform: translateY(-1px);
            }

            div[data-testid="stButton"] > button:focus:not(:active) {
                border-color: var(--accent);
                color: var(--accent);
                box-shadow: 0 0 0 0.2rem rgba(15, 118, 110, 0.14);
            }

            @media (max-width: 840px) {
                .block-container {
                    padding: 1.25rem 1rem 2.5rem;
                }

                .photo-strip {
                    grid-template-columns: 1fr;
                    min-height: unset;
                }

                .photo-card,
                .photo-card:first-child {
                    min-height: 230px;
                }

                .title-row,
                .calendar-heading {
                    align-items: flex-start;
                    flex-direction: column;
                }

                .info-grid {
                    grid-template-columns: repeat(2, 1fr);
                }

                .info-item {
                    border-bottom: 1px solid var(--line);
                }

                .info-item:nth-child(even) {
                    border-right: 0;
                }
            }

            @media (max-width: 520px) {
                .info-grid {
                    grid-template-columns: 1fr;
                }

                .info-item {
                    border-right: 0;
                }

                .calendar-cell,
                div[data-testid="stButton"] > button {
                    min-height: 2.8rem;
                    padding-left: 0.25rem;
                    padding-right: 0.25rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def month_delta(base: date, delta: int) -> date:
    month_index = base.month - 1 + delta
    year = base.year + month_index // 12
    month = month_index % 12 + 1
    day = min(base.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def ensure_calendar_state() -> None:
    today = date.today()
    st.session_state.setdefault("selected_date", today)
    st.session_state.setdefault("calendar_month", date(today.year, today.month, 1))


def render_photo_strip() -> None:
    photo_cards = "".join(
        f'<div class="photo-card" style="background-image: url({photo});"></div>'
        for photo in PHOTOS
    )
    st.markdown(f'<div class="photo-strip">{photo_cards}</div>', unsafe_allow_html=True)


def render_intro() -> None:
    st.markdown(
        """
        <div class="title-row">
            <div>
                <div class="eyebrow">Jaco, Costa Rica</div>
                <h1 class="page-title">Pacific Sunset Jaco</h1>
            </div>
            <p class="subtitle">
                A calm apartment stay near the beach, shaped for slow mornings,
                open-air evenings, and an easy walk into town.
            </p>
        </div>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-value">2</div>
                <div class="info-label">Bedrooms</div>
            </div>
            <div class="info-item">
                <div class="info-value">4</div>
                <div class="info-label">Guests</div>
            </div>
            <div class="info-item">
                <div class="info-value">5 min</div>
                <div class="info-label">To the beach</div>
            </div>
            <div class="info-item">
                <div class="info-value">Sunset</div>
                <div class="info-label">Balcony view</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_calendar() -> None:
    selected = st.session_state["selected_date"]
    visible_month = st.session_state["calendar_month"]

    st.markdown(
        f"""
        <div class="calendar-shell">
            <div class="calendar-heading">
                <div>
                    <div class="section-kicker">Availability</div>
                    <h2 class="calendar-title">{MONTH_NAMES[visible_month.month]} {visible_month.year}</h2>
                </div>
                <div class="selected-date">{selected.strftime("%A, %B %-d, %Y") if hasattr(selected, "strftime") else selected}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_left, nav_center, nav_right = st.columns([1, 5, 1])
    with nav_left:
        if st.button("‹", key="prev_month", help="Previous month"):
            st.session_state["calendar_month"] = month_delta(visible_month, -1)
            st.rerun()
    with nav_center:
        st.date_input(
            "Selected date",
            key="selected_date",
            label_visibility="collapsed",
        )
    with nav_right:
        if st.button("›", key="next_month", help="Next month"):
            st.session_state["calendar_month"] = month_delta(visible_month, 1)
            st.rerun()

    if selected.year != visible_month.year or selected.month != visible_month.month:
        if "calendar_sync_done" not in st.session_state:
            st.session_state["calendar_month"] = date(selected.year, selected.month, 1)
            st.session_state["calendar_sync_done"] = True
            st.rerun()
    else:
        st.session_state.pop("calendar_sync_done", None)

    st.markdown(
        '<div class="calendar-weekdays">'
        + "".join(f'<div class="weekday">{day}</div>' for day in WEEKDAY_LABELS)
        + "</div>",
        unsafe_allow_html=True,
    )

    for week_index, week in enumerate(calendar.monthcalendar(visible_month.year, visible_month.month)):
        columns = st.columns(7, gap="small")
        for day_index, day_number in enumerate(week):
            with columns[day_index]:
                if day_number == 0:
                    st.markdown('<div class="calendar-cell"></div>', unsafe_allow_html=True)
                    continue

                cell_date = date(visible_month.year, visible_month.month, day_number)
                is_selected = cell_date == selected
                if st.button(
                    str(day_number),
                    key=f"day_{visible_month.year}_{visible_month.month}_{week_index}_{day_number}",
                    help=cell_date.strftime("%A, %B %d, %Y"),
                    type="primary" if is_selected else "secondary",
                ):
                    st.session_state["selected_date"] = cell_date
                    st.rerun()


add_styles()
ensure_calendar_state()
render_photo_strip()
render_intro()
render_calendar()
