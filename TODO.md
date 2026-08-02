# TODO — Expand currencies & make all dropdowns click-selectable

## Steps

- [x] 1. `calculators/financial.py` — expand `CURRENCIES` + `FX_RATES` to cover all major world countries (with ISO codes, names, symbols, and approximate exchange rates vs USD)
- [x] 2. `app.py` — make every select/combobox open its dropdown list on click (not only the arrow) across all services
- [x] 3. `app.py` — keep both currency dropdowns editable/searchable (state="normal", NOT read-only) and restore the full country list after each selection
- [x] 4. `app.py` — add a hint label under the currency dropdowns ("click to pick a country, or type to search")
- [x] 5. Verify: every currency option shows its ISO code + country + rate; dropdowns open on click; Swap button and live ratio still work
- [x] 6. Run import/UI check to confirm the app starts cleanly

