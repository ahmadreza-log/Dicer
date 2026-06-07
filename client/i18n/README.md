# Client translations

Add a new language by creating a module in this folder and registering it in `Catalog.py`.

## Steps for contributors

1. Copy `en.py` to `<code>.py` (for example `de.py`).
2. Set `CODE`, `LABEL`, and translate every value in `STRINGS`.
3. Import the module in `Catalog.py` and append it to `Packages`.

## Usage in UI code

```python
from i18n.Locale import Locale

label = Locale.t("menu.start")
message = Locale.t("network.saved.body", host="127.0.0.1", port=12055)
```

Keys use dot notation (`section.item`). Keep keys identical across all language files.

## Fonts

- English (`en`) uses **Inter** (or system fallback).
- Persian (`fa`) uses bundled **IRANSansDN** from `assets/fonts/Iransansdn-Regular.ttf`.

Register additional locale fonts in `Fonts.py`.

## Direction

Set `RTL = True` in a language module for right-to-left layout.
Use helpers from `Layout.py` (`Anchor`, `Sticky`, `Label`, `PlaceScreenHeader`).
