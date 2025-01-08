# Rozwój Forest Mod Manager / Forest Mod Manager Development

## 🇵🇱 Polski

Cześć! Super, że chcesz pomóc w rozwoju Forest Mod Manager! Ten dokument zawiera wszystkie informacje potrzebne do
rozpoczęcia pracy nad projektem.

### 🛠️ Wymagania

- Python 3.8 lub nowszy
- Git
- Edytor kodu (polecamy VS Code lub PyCharm)

### 📦 Zależności

```bash
pip install -r requirements.txt
```

Główne biblioteki:

- `customtkinter` - nowoczesne widgety UI
- `tkinterdnd2` - obsługa drag & drop
- `Pillow` - obsługa obrazów
- `babel` - internacjonalizacja

### 🏗️ Struktura projektu

```
src/
├── ui/               # Interfejs użytkownika
│   ├── components/   # Reużywalne komponenty
│   ├── styles.py     # Style i kolory
│   └── main_window.py
├── utils/            # Narzędzia pomocnicze
├── installer.py      # Logika instalacji modów
├── config.py         # Zarządzanie konfiguracją
├── i18n.py          # System tłumaczeń
└── app.py           # Punkt wejścia aplikacji

assets/              # Zasoby
├── fonts/           # Czcionki
└── icons/           # Ikony

locales/             # Tłumaczenia
```

### 🚀 Rozpoczęcie pracy

1. Zrób fork repozytorium
2. Sklonuj swojego forka:
   ```bash
   git clone https://github.com/twoj-username/forest-mod-manager.git
   ```
3. Utwórz branch dla swojej funkcji:
   ```bash
   git checkout -b nazwa-funkcji
   ```
4. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
5. Uruchom aplikację:
   ```bash
   python -m src.app
   ```

### 💡 Zasady współpracy

1. **Kod**
    - Używamy PEP 8 (ale nie fanatycznie)
    - Komentarze i nazwy zmiennych po angielsku
    - Docstringi dla klas i ważniejszych funkcji
    - Type hints gdzie to możliwe

2. **Commity**
    - Krótkie, konkretne commity
    - Opis po angielsku, zaczynamy wielką literą
    - Format: `Add/Fix/Update/Remove: krótki opis`

3. **Pull Requests**
    - Jeden PR = jedna funkcjonalność
    - Opisz dokładnie zmiany
    - Dołącz screenshoty jeśli zmieniasz UI
    - Upewnij się, że wszystko się buduje

4. **Testowanie**
    - Przetestuj na Windows (główna platforma)
    - Sprawdź czy działa drag & drop
    - Przetestuj instalację modów
    - Sprawdź czy UI się nie psuje przy zmianie rozmiaru

### 🎯 Co można zrobić?

1. **UI/UX**
    - Dodać ciemny motyw
    - Poprawić responsywność
    - Dodać animacje

2. **Funkcjonalności**
    - Wsparcie dla paczek modów
    - Automatyczne aktualizacje
    - Backup modów

3. **Inne**
    - Więcej tłumaczeń
    - Lepsza dokumentacja
    - Testy jednostkowe

---

## 🇬🇧 English

Hey! Great that you want to help develop Forest Mod Manager! This document contains all the information needed to start
working on the project.

### 🛠️ Requirements

- Python 3.8 or newer
- Git
- Code editor (we recommend VS Code or PyCharm)

### 📦 Dependencies

```bash
pip install -r requirements.txt
```

Main libraries:

- `customtkinter` - modern UI widgets
- `tkinterdnd2` - drag & drop support
- `Pillow` - image handling
- `babel` - internationalization

### 🏗️ Project Structure

```
src/
├── ui/               # User interface
│   ├── components/   # Reusable components
│   ├── styles.py     # Styles and colors
│   └── main_window.py
├── utils/            # Helper utilities
├── installer.py      # Mod installation logic
├── config.py         # Configuration management
├── i18n.py          # Translation system
└── app.py           # Application entry point

assets/              # Resources
├── fonts/           # Fonts
└── icons/           # Icons

locales/             # Translations
```

### 🚀 Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/forest-mod-manager.git
   ```
3. Create a branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python -m src.app
   ```

### 💡 Collaboration Rules

1. **Code**
    - Follow PEP 8 (but don't be fanatic)
    - Comments and variable names in English
    - Docstrings for classes and important functions
    - Type hints where possible

2. **Commits**
    - Short, specific commits
    - Description in English, start with capital letter
    - Format: `Add/Fix/Update/Remove: short description`

3. **Pull Requests**
    - One PR = one feature
    - Describe changes in detail
    - Include screenshots if UI changes
    - Make sure everything builds

4. **Testing**
    - Test on Windows (main platform)
    - Check if drag & drop works
    - Test mod installation
    - Verify UI doesn't break on resize

### 🎯 What Can Be Done?

1. **UI/UX**
    - Add dark theme
    - Improve responsiveness
    - Add animations

2. **Features**
    - Mod pack support
    - Automatic updates
    - Mod backup

3. **Other**
    - More translations
    - Better documentation
    - Unit tests