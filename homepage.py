from __future__ import annotations

import calendar
from datetime import date, timedelta
from urllib.parse import urlencode

import streamlit as st


st.set_page_config(
    page_title="White Witch Apartment",
    page_icon="ðŸŒ…",
    layout="wide",
    initial_sidebar_state="collapsed",
)


PHOTOS = [
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=85",
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=85",
    "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=1200&q=85",
]

MONTH_NAMES = list(calendar.month_name)
WEEKDAY_LABELS = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]


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

            .calendar-heading,
            .calendar-layout {
                align-items: center;
                display: flex;
                justify-content: space-between;
                gap: 1rem;
            }

            .calendar-layout {
                align-items: flex-start;
                gap: 2rem;
                margin-bottom: 1rem;
            }

            .calendar-title {
                color: var(--ink);
                font-size: 2rem;
                font-weight: 650;
                letter-spacing: 0;
                margin: 0;
            }

            .calendar-picker {
                background: #10151d;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                box-shadow: 0 20px 50px rgba(16, 21, 29, 0.18);
                max-width: 540px;
                padding: 1.2rem;
                width: 100%;
            }

            .calendar-nav {
                align-items: center;
                color: #ffffff;
                display: flex;
                justify-content: space-between;
                margin-bottom: 1rem;
            }

            .calendar-month {
                color: #ffffff;
                font-size: 1.15rem;
                font-weight: 700;
                letter-spacing: 0;
                margin: 0;
                text-align: center;
            }

            .selected-date {
                background: #ffffff;
                border: 1px solid var(--line);
                border-radius: 8px;
                color: var(--ink);
                font-weight: 600;
                padding: 0.75rem 1rem;
                text-align: left;
            }

            .calendar-weekdays {
                display: grid;
                gap: 0.55rem;
                grid-template-columns: repeat(7, minmax(0, 1fr));
                margin-bottom: 0.55rem;
            }

            .weekday {
                color: rgba(255, 255, 255, 0.46);
                font-size: 0.78rem;
                font-weight: 700;
                padding: 0.35rem 0;
                text-align: center;
                text-transform: uppercase;
            }

            .calendar-grid {
                display: grid;
                gap: 0.55rem;
                grid-template-columns: repeat(7, minmax(0, 1fr));
            }

            .calendar-day,
            .calendar-empty,
            .calendar-arrow-button {
                align-items: center;
                border-radius: 8px;
                display: flex;
                justify-content: center;
                min-height: 3.8rem;
            }

            .calendar-day,
            .calendar-arrow-button {
                color: #ffffff;
                font-weight: 700;
                text-decoration: none;
                transition: 140ms ease;
            }

            .calendar-day:hover,
            .calendar-arrow-button:hover {
                background: rgba(255, 255, 255, 0.08);
                color: #ffffff;
                transform: translateY(-1px);
            }

            .calendar-day.is-selected {
                background: var(--accent);
            }

            .calendar-arrow-button {
                min-height: 2.8rem;
                width: 2.8rem;
            }

            .availability-summary {
                min-width: 270px;
                width: 32%;
            }

            .summary-label {
                color: var(--muted);
                font-size: 0.8rem;
                font-weight: 700;
                letter-spacing: 0.08rem;
                margin-bottom: 0.5rem;
                text-transform: uppercase;
            }

            .availability-message {
                align-items: center;
                color: var(--accent);
                display: flex;
                font-size: 1.15rem;
                font-weight: 800;
                gap: 0.85rem;
                margin-top: 1rem;
                text-transform: lowercase;
            }

            .green-arrow {
                background: var(--accent);
                display: inline-block;
                height: 3px;
                position: relative;
                width: 42px;
            }

            .green-arrow::after {
                border-bottom: 7px solid transparent;
                border-left: 10px solid var(--accent);
                border-top: 7px solid transparent;
                content: "";
                position: absolute;
                right: -1px;
                top: 50%;
                transform: translateY(-50%);
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
                .calendar-heading,
                .calendar-layout {
                    align-items: flex-start;
                    flex-direction: column;
                }

                .calendar-picker,
                .availability-summary {
                    max-width: none;
                    width: 100%;
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

                .calendar-day,
                .calendar-empty {
                    min-height: 3rem;
                    padding-left: 0.25rem;
                    padding-right: 0.25rem;
                }

                .calendar-arrow-button {
                    min-height: 2.6rem;
                    width: 2.6rem;
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


def first_query_value(value: str | list[str] | None) -> str | None:
    if isinstance(value, list):
        return value[0] if value else None
    return value


def parse_date_param(value: str | list[str] | None) -> date | None:
    raw_value = first_query_value(value)
    if not raw_value:
        return None

    try:
        return date.fromisoformat(raw_value)
    except ValueError:
        return None


def parse_month_param(value: str | list[str] | None) -> date | None:
    raw_value = first_query_value(value)
    if not raw_value:
        return None

    try:
        year, month = raw_value.split("-", maxsplit=1)
        return date(int(year), int(month), 1)
    except ValueError:
        return None


def calendar_url(selected: date, visible_month: date) -> str:
    return "?" + urlencode(
        {
            "selected_date": selected.isoformat(),
            "calendar_month": f"{visible_month.year:04d}-{visible_month.month:02d}",
        }
    )


def ensure_calendar_state() -> None:
    today = date.today()
    selected = (
        parse_date_param(st.query_params.get("selected_date"))
        or st.session_state.get("selected_date")
        or today
    )
    visible_month = (
        parse_month_param(st.query_params.get("calendar_month"))
        or st.session_state.get("calendar_month")
        or date(selected.year, selected.month, 1)
    )

    st.session_state["selected_date"] = selected
    st.session_state["calendar_month"] = visible_month


def format_selected_date(selected: date) -> str:
    return f"{selected.strftime('%A, %B')} {selected.day}, {selected.year}"


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
                <h1 class="page-title">White Witch Apartment</h1>
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
                <div class="info-value">5</div>
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
    month_calendar = calendar.Calendar(firstweekday=6)
    previous_month = month_delta(visible_month, -1)
    next_month = month_delta(visible_month, 1)
    calendar_days = []

    for week in month_calendar.monthdayscalendar(visible_month.year, visible_month.month):
        for day_number in week:
            if day_number == 0:
                calendar_days.append('<div class="calendar-empty"></div>')
                continue

            cell_date = date(visible_month.year, visible_month.month, day_number)
            selected_class = " is-selected" if cell_date == selected else ""
            calendar_days.append(
                f'<a class="calendar-day{selected_class}" '
                f'href="{calendar_url(cell_date, date(cell_date.year, cell_date.month, 1))}">'
                f"{day_number}</a>"
            )

    st.markdown(
        f"""
        <div class="calendar-shell">
            <div class="calendar-heading">
                <div>
                    <div class="section-kicker">Availability</div>
                    <h2 class="calendar-title">Choose your date</h2>
                </div>
            </div>
            <div class="calendar-layout">
                <div class="calendar-picker">
                    <div class="calendar-nav">
                        <a class="calendar-arrow-button" href="{calendar_url(selected, previous_month)}">&lt;</a>
                        <h3 class="calendar-month">{MONTH_NAMES[visible_month.month]} {visible_month.year}</h3>
                        <a class="calendar-arrow-button" href="{calendar_url(selected, next_month)}">&gt;</a>
                    </div>
                    <div class="calendar-weekdays">
                        {"".join(f'<div class="weekday">{day}</div>' for day in WEEKDAY_LABELS)}
                    </div>
                    <div class="calendar-grid">
                        {"".join(calendar_days)}
                    </div>
                </div>
                <div class="availability-summary">
                <div class="summary-label">Date picked</div>
                <div class="selected-date">{format_selected_date(selected)}</div>
                <div class="availability-message">
                    <span class="green-arrow"></span>
                    <span>available!</span>
                </div>
            </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


add_styles()
ensure_calendar_state()
render_photo_strip()
render_intro()
render_calendar()

