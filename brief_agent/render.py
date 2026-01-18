"""Markdown rendering for brief output."""

from .schemas import BriefOutput


def render_markdown(brief: BriefOutput) -> str:
    """
    Render a BriefOutput to formatted markdown.

    Args:
        brief: Validated brief data

    Returns:
        Formatted markdown string
    """
    lines = []

    # Otsikko
    lines.append(f"# Yritystiivistelmä: {brief.ticker}")
    lines.append(f"**Päivämäärä:** {brief.date}")
    lines.append("")

    # Yhteenveto
    lines.append("## Yhteenveto")
    for bullet in brief.summary_bullets:
        lines.append(f"- {bullet}")
    lines.append("")

    # Yritysprofiili
    lines.append("## Yritysprofiili")
    lines.append(f"- **Ticker:** {brief.ticker}")
    lines.append(f"- **Päivämäärä:** {brief.date}")
    lines.append("")

    # IR-tiedotteet
    lines.append("## IR-tiedotteet")
    if brief.ir_releases:
        for ir in brief.ir_releases[:3]:  # Top 3
            lines.append(f"### {ir.title}")
            lines.append(f"- **Päivämäärä:** {ir.date}")
            lines.append(f"- **Lähde:** {ir.source}")
            if ir.summary:
                lines.append(f"- {ir.summary}")
            lines.append(f"- [Linkki]({ir.url})")
            lines.append("")
    else:
        lines.append("*Ei IR-tiedotteita saatavilla.*")
        lines.append("")

    # Uutiset
    lines.append("## Uutiset")
    if brief.news:
        for news in brief.news[:5]:  # Top 5
            lines.append(f"### {news.title}")
            lines.append(f"- **Lähde:** {news.source}")
            if news.summary:
                lines.append(f"- {news.summary}")
            lines.append(f"- [Linkki]({news.url})")
            lines.append("")
    else:
        lines.append("*Ei uutisia saatavilla.*")
        lines.append("")

    # Kasvuajurit
    lines.append("## Kasvuajurit")
    for driver in brief.drivers:
        lines.append(f"- {driver}")
    lines.append("")

    # Riskit
    lines.append("## Riskit")
    for risk in brief.risks:
        lines.append(f"- {risk}")
    lines.append("")

    # Huomiot ja rajoitukset
    lines.append("## Huomiot ja rajoitukset")
    for limitation in brief.limitations:
        lines.append(f"- {limitation}")
    lines.append("")

    # Lopputeksti
    lines.append("---")
    lines.append("*Luotu IR & Uutis Tiivistelmä Agentilla*")

    return "\n".join(lines)
