# 🌍 Forest Mod Manager - Translation Guide

## 🇬🇧 English: How to Translate the App (For Complete Beginners!)

### 🤔 What is This?
This guide will help you translate the Forest Mod Manager app into your language, even if you've never done translation work before!

### 📋 What You'll Need
- A text editor (like Notepad, VSCode, or Sublime Text)
- Basic computer skills
- Knowledge of your target language
- (Optional but recommended) Poedit translation software

### 🗂️ Project Translation Structure
```
locales/
├── base.pot                             # Template with ALL text strings
├── en/                                  # English language folder
│   └── LC_MESSAGES/
│       ├── forest_mod_manager.mo        # Compiled English file
│       └── forest_mod_manager.po        # English translation source
└── pl/                                  # Polish language folder
    └── LC_MESSAGES/
        ├── forest_mod_manager.mo        # Compiled Polish file
        └── forest_mod_manager.po        # Polish translation source
```

### 🚀 Step-by-Step Translation Guide

#### 1. Prepare Your Translation Environment
1. Download the project files
2. Find the `locales` folder
3. Find the `base.pot` file

#### 2. Create a New Language Folder
1. In the `locales` folder, create a new folder with your language code
   - Example: For Spanish, create `es/LC_MESSAGES/`
   - Language codes: 
     - English: `en`
     - Spanish: `es`
     - French: `fr`
     - German: `de`
     - (Check ISO 639-1 codes for your language)

#### 3. Copy and Prepare Translation File
1. Copy `base.pot` to your new language folder
2. Rename the copied file to `forest_mod_manager.po`
3. Open `forest_mod_manager.po` in a text editor

#### 4. Edit the File Header
Replace the header information with your details:
```
msgid ""
msgstr ""
"POT-Creation-Date: 2025-01-06 21:45+0100\n"
"PO-Revision-Date: 2025-01-06 21:45+0100\n"
"Last-Translator: Your Name\n"
"Language: your_language_code\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.16.0\n"
```
- Change `your_language_code` to the correct two-letter code
- Adjust `Plural-Forms` for your language's grammar rules

#### 5. Start Translating
- Find `msgid` lines (original text)
- Translate in the corresponding `msgstr` line
- Keep placeholders like `{folder_name}` exactly the same!
- Preserve `\n` for line breaks

#### 6. Compile Your Translation
Option 1: Using Command Line
```bash
msgfmt forest_mod_manager.po -o forest_mod_manager.mo
```

Option 2: Using Poedit (Recommended for Beginners)
1. Download Poedit (free software)
2. Open your `forest_mod_manager.po`
3. Click "Save" - it automatically creates the `.mo` file

### 🛠️ Important Translation Tips
- Translate ONLY the text between `msgstr ""`
- Keep technical terms consistent
- Use natural language of the target translation
- Maintain the same tone and style as the original
- Test your translation in the app
- Ask for review if unsure

### 🆘 Need Help?
- Open an Issue in the project's GitHub repository
- Ask for translation review
- Share your progress!
- Join our translation community

### 💡 Translation Etiquette
- Be respectful of other translators
- Coordinate with existing translators
- Maintain consistency with previous translations

---

## 🇵🇱 Polski: Jak Przetłumaczyć Aplikację (Dla Zupełnie Początkujących!)

### 🤔 Co to jest?
Ten przewodnik pomoże Ci przetłumaczyć aplikację Forest Mod Manager na Twój język, nawet jeśli nigdy wcześniej nie zajmowałeś się tłumaczeniami!

### 📋 Czego będziesz potrzebować
- Edytor tekstu (np. Notatnik, VSCode lub Sublime Text)
- Podstawowe umiejętności komputerowe
- Znajomość języka docelowego
- (Opcjonalnie, ale polecane) Oprogramowanie Poedit

### 🗂️ Struktura Projektu Tłumaczeń
```
locales/
├── base.pot                             # Szablon ze WSZYSTKIMI tekstami
├── en/                                  # Folder języka angielskiego
│   └── LC_MESSAGES/
│       ├── forest_mod_manager.mo        # Skompilowany plik angielski
│       └── forest_mod_manager.po        # Źródło tłumaczenia angielskiego
└── pl/                                  # Folder języka polskiego
    └── LC_MESSAGES/
        ├── forest_mod_manager.mo        # Skompilowany plik polski
        └── forest_mod_manager.po        # Źródło tłumaczenia polskiego
```

### 🚀 Przewodnik Krok po Kroku

#### 1. Przygotuj Środowisko Tłumaczenia
1. Pobierz pliki projektu
2. Znajdź folder `locales`
3. Znajdź plik `base.pot`

#### 2. Utwórz Folder Nowego Języka
1. W folderze `locales` stwórz nowy folder z kodem Twojego języka
   - Przykład: Dla języka hiszpańskiego stwórz `es/LC_MESSAGES/`
   - Kody języków: 
     - Angielski: `en`
     - Hiszpański: `es`
     - Francuski: `fr`
     - Niemiecki: `de`
     - (Sprawdź kody ISO 639-1 dla Twojego języka)

#### 3. Skopiuj i Przygotuj Plik Tłumaczenia
1. Skopiuj `base.pot` do folderu Twojego języka
2. Zmień nazwę skopiowanego pliku na `forest_mod_manager.po`
3. Otwórz `forest_mod_manager.po` w edytorze tekstu

#### 4. Edytuj Nagłówek Pliku
Zastąp informacje w nagłówku swoimi danymi:
```
msgid ""
msgstr ""
"POT-Creation-Date: 2025-01-06 21:45+0100\n"
"PO-Revision-Date: 2025-01-06 21:45+0100\n"
"Last-Translator: Twoje Imię\n"
"Language: kod_twojego_języka\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.16.0\n"
```
- Zmień `kod_twojego_języka` na odpowiedni dwuliterowy kod
- Dostosuj `Plural-Forms` do zasad gramatycznych Twojego języka

#### 5. Zacznij Tłumaczenie
- Znajdź linie `msgid` (oryginalny tekst)
- Przetłumacz w odpowiedniej linii `msgstr`
- Zachowaj symbole zastępcze jak `{folder_name}` dokładnie takie same!
- Zachowaj `\n` dla podziałów linii

#### 6. Skompiluj Swoje Tłumaczenie
Opcja 1: Używając Wiersza Poleceń
```bash
msgfmt forest_mod_manager.po -o forest_mod_manager.mo
```

Opcja 2: Używając Poedit (Polecane dla Początkujących)
1. Pobierz Poedit (darmowe oprogramowanie)
2. Otwórz swój plik `forest_mod_manager.po`
3. Kliknij "Zapisz" - automatycznie utworzy plik `.mo`

### 🛠️ Ważne Wskazówki Dotyczące Tłumaczenia
- Tłumacz TYLKO tekst między `msgstr ""`
- Zachowaj spójność terminów technicznych
- Używaj naturalnego języka tłumaczenia
- Zachowaj ten sam ton i styl co oryginał
- Przetestuj tłumaczenie w aplikacji
- Poproś o weryfikację, jeśli masz wątpliwości

### 🆘 Potrzebujesz Pomocy?
- Otwórz zgłoszenie w repozytorium GitHub
- Poproś o przegląd tłumaczenia
- Podziel się postępami
- Dołącz do naszej społeczności tłumaczy

### 💡 Zasady Etykiety Tłumaczeniowej
- Szanuj innych tłumaczy
- Koordynuj działania z istniejącymi tłumaczami
- Zachowaj spójność z poprzednimi tłumaczeniami