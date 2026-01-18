# UI Development Instructions

## Goal
Build a lightweight, premium-looking web interface for the IR Agent.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JS, CSS3, HTML5
- **Server**: Uvicorn

## File Structure
Add these files to the existing repository:

```text
brief_agent/
├── api.py           # FastAPI application
└── web/
    ├── __init__.py
    ├── templates/
    │   └── index.html
    └── static/
        ├── css/
        │   └── style.css
        └── js/
            └── app.js
```

## Requirements

### 1. API (`brief_agent/api.py`)
- `GET /api/briefs`: List all JSON/MD files in `output/`, sorted by date.
- `GET /api/briefs/{filename}`: Return file content.
- `POST /api/generate`: Accepts JSON `{ticker: str, date: str, mode: str}`. Runs `Agent.run()` in a background task or synchronously (for simplicity initially).

### 2. Frontend
- **Design**:
    - Dark mode by default or clear toggle.
    - Use a nice sans-serif font (Inter or system-ui).
    - "Glass" effect cards for briefs.
- **Functionality**:
    - Sidebar or top bar for inputs (Ticker, Date).
    - Main area displays grid of existing briefs.
    - Clicking a brief opens it in a view mode.
    - "Generate" button shows a loading spinner.

### 3. CLI Integration
- Update `brief_agent/cli.py` to add `ui` command:
  ```python
  def run_ui(args):
      import uvicorn
      uvicorn.run("brief_agent.api:app", reload=True)
  ```

## Styling Guidelines
- **Colors**: Deep blues/greys for background (`#0f172a`), clean white text. bright accent color (e.g., `#38bdf8`) for buttons/links.
- **Spacing**: Generous padding.
- **Feedback**: Immediate visual feedback for interactions (hover states, active states).
