# Current Plan: `--user`-Parameter + neuer Download-Pfad

## Ziel

- Neuer `--user`-Parameter der direkt den Usernamen akzeptiert (z.B. `--user scherenhaenden`)
- `--user-url` bleibt als Fallback erhalten (Rückwärtskompatibilität)
- Downloads werden in `./downloads/{user}/{yyyy-MM-dd}/` gespeichert
- Part 1 (Portfolio-Parsing mit `--base-dir`) bleibt unverändert

---

## Schritte

### `src/url_utils.py`

- [ ] **Schritt 1**: Neue Funktion `validate_username(username: str) -> str` ergänzen, die Regex-Validierung (`^[a-zA-Z0-9_-]+$`) durchführt und bei ungültigem Format einen `ValueError` wirft.

---

### `src/downloader.py`

- [ ] **Schritt 2**: Signatur von `download_person_data` von `(base_dir)` auf `(person, download_dir)` ändern.
- [ ] **Schritt 3**: Das Lesen von `person.txt` aus `base_dir/portfolio/` im Funktionskörper entfernen (person wird nun direkt übergeben).
- [ ] **Schritt 4**: `output_dir` auf `download_dir` umstellen (`os.makedirs(download_dir, exist_ok=True)`).

---

### `main.py`

- [ ] **Schritt 5**: `--user`-Argument zu argparse hinzufügen.
- [ ] **Schritt 6**: Username-Auflösungslogik erweitern: `args.user` → `args.user_url` (via `extract_username_from_url`) → `person.txt`-Fallback.
- [ ] **Schritt 7**: `download_dir` berechnen: `./downloads/{person}/{yyyy-MM-dd}/` (unabhängig von `base_dir`).
- [ ] **Schritt 8**: `download_person_data(base_dir)` durch `download_person_data(person, download_dir)` ersetzen.
- [ ] **Schritt 9**: `person_output_dir` (für Parsing von `profile.html`, `stats.html`) auf `download_dir` umstellen.
- [ ] **Schritt 10**: Manuelles Schreiben von `person.txt` nach `{base_dir}/portfolio/person.txt` entfernen (obsolet).
- [ ] **Schritt 11**: Fehlermeldung am Ende anpassen.

---

### `tests/test_downloader.py`

- [ ] **Schritt 12**: Test-Aufrufe `download_person_data(temp_base_dir)` auf neue Signatur `download_person_data('testuser', download_dir)` umstellen.
- [ ] **Schritt 13**: Im Test das Anlegen von `portfolio/person.txt` entfernen (nicht mehr nötig).
- [ ] **Schritt 14**: `test_download_no_person_file`-Test an neue Signatur anpassen.

---

### `tests/test_main.py`

- [ ] **Schritt 15**: Mock-Argumente um `args.user = None` erweitern.
- [ ] **Schritt 16**: Neuen Test `test_user_argument_parsing` ergänzen (`--user scherenhaenden`).
- [ ] **Schritt 17**: Neuen Test `test_user_overrides_user_url` ergänzen.

---

## Status

- [x] Planung abgeschlossen
- [x] Implementierung gestartet
- [x] Tests aktualisiert
- [x] Fertig

