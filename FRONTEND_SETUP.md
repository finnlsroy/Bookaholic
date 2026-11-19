# Bookaholic frontend

Three JavaScript-rendered screens: Home, Library, Book Details. The Add Book and Review actions open dialogs rather than separate pages. All persistent information uses the existing Python library through Eel. No JavaScript frameworks or npm installation needed.

## Run on Windows

Extract the ZIP, open a terminal in `Bookaholic-main`, then run:

```powershell
py -m pip install -e ./backend
py -m bookaholic
```

Use Python 3.11 or newer with Chrome/Chromium installed (Eel's default browser). If your Python command is `python`, substitute it for `py`. Don't open index.html directly: Eel serves the page and exposes the backend. Existing saved books are loaded automatically.

## Frontend files

- `backend/bookaholic/frontend/index.html`: base markup, Eel script, dialog.
- `backend/bookaholic/frontend/app.js`: all rendering, navigation, search/filtering, statistics, book actions.
- `backend/bookaholic/frontend/style.css`: responsive styling.

The Home Back button is disabled when there is no navigation history. Book IDs remain within the current Eel session. Favourite books are books with at least 4 stars, not a separate favourite flag. Period statistics count the completed book's full page count in its finish period, as the existing backend does. Reading duration and speed in details are calculated in JS using the same inclusive-day formula as Python.

## Backend changes

- Add Eel startup block in `__main__.py`.
- Postpone self-referencing annotations in `_book.py` and `subject.py` so imports work in Python 3.11–3.13.
- Include frontend assets in package data and copy README into backend for packaging.
- Existing API names, schema and storage logic are unchanged.

## Verification

`node --check backend/bookaholic/frontend/app.js` checks JS syntax. `python tests/check_backend.py` tests the real Python book, library, statistics and rating functions with offline dependency stubs and temporary storage. Live Eel browser integration and Open Library search have not been tested in the build environment because dependencies/browser setup were unavailable. Manual lookup fallback is provided. The existing rating-summary division-by-zero issue is avoided by using get_top_rated instead.
