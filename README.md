# e-rektor.pl - System zarządzania studentami

## Opis
e-rektor.pl to aplikacja mobilna stworzona dla dziekanów uczelni do zarządzania informacjami o studentach. Aplikacja została zrefaktorowana z oryginalnej aplikacji Task3App do specjalistycznego narzędzia edukacyjnego.

## Funkcjonalności

### 🎯 Główne cechy:
- **Przeglądanie studentów**: Lista wszystkich studentów z avatarami i kolorowym kodowaniem
- **Filtrowanie**: Oddzielne widoki dla zdających (zielony) i niezdających (czerwony) studentów
- **Menu nawigacyjne**: Pełnofunkcjonalne menu boczne dostępne przez przycisk hamburgera
- **Próg zdania**: Konfigurowalny próg (domyślnie 3.0)
- **Kodowanie kolorami**: Zielone nazwy dla zdających, czerwone dla niezdających
- **Szczegółowe informacje**: Kompletne dane kontaktowe i akademickie w dialogach
- **Statystyki**: Kompleksowy przegląd wyników akademickich z rozkładem ocen

### 📱 Nawigacja:
**Dostęp przez menu hamburgera (☰) w lewym górnym rogu:**
1. **👥 Wszyscy studenci** - Pełna lista studentów z kolorowym kodowaniem
2. **✅ Zdający** - Studenci ze średnią ≥ 3.0 (wyświetlane na zielono)
3. **❌ Niezdający** - Studenci ze średnią < 3.0 (wyświetlane na czerwono)
4. **📊 Statystyki** - Szczegółowe statystyki i rozkład ocen
5. **➕ Dodaj studenta** - Pełnofunkcjonalny dialog do dodawania nowych studentów

**Dodatkowe funkcje:**
- Kliknięcie na studenta wyświetla szczegółowe informacje
- Przycisk odświeżania (🔄) w prawym górnym rogu
- Responsywny interfejs z automatycznym kolorowaniem

### 📊 System oceniania:
- **Bardzo dobry**: 4.5-5.0
- **Dobry**: 3.5-4.4
- **Dostateczny**: 3.0-3.4
- **Niedostateczny**: <3.0

## Struktura danych

### Plik `app_data.json`:
```json
{
  "students": [
    {
      "id": 1,
      "name": "Imię Nazwisko",
      "email": "email@student.edu.pl",
      "phone": "+48 123 456 789",
      "address": "Adres studenta",
      "photo": "ścieżka/do/zdjęcia",
      "grades": [4.0, 3.5, 4.5, 3.0, 4.0],
      "average": 3.8
    }
  ],
  "passing_threshold": 3.0
}
```

## Technologie
- **Framework**: KivyMD
- **Język**: Python 3.12
- **Architektura**: MVC z separacją logiki i UI
- **Dane**: JSON-based storage

## Instalacja i uruchomienie

### Wymagania systemowe
- Python 3.8+
- pip (menedżer pakietów Python)

### Kroki instalacji
1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/twój-username/e-rektor.git
   cd e-rektor
   ```

2. **Zainstaluj zależności:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Uruchom aplikację:**
   ```bash
   python task3_app.py
   ```

### Alternatywna instalacja (z virtual environment)
```bash
# Utwórz wirtualne środowisko
python -m venv venv

# Aktywuj środowisko
# Na macOS/Linux:
source venv/bin/activate
# Na Windows:
venv\Scripts\activate

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację
python task3_app.py
```

## Autor
Zrefaktorowane z Task3App do e-rektor.pl - system zarządzania studentami dla dziekanów.

## Licencja
MIT License - zobacz plik LICENSE dla szczegółów.

## Zgłaszanie problemów
Jeśli napotkasz problemy lub masz sugestie ulepszeń, proszę [utwórz issue](https://github.com/twój-username/e-rektor/issues) w repozytorium GitHub.

## Wkład w projekt
Pull requesty są mile widziane! Dla większych zmian, proszę najpierw otwórz issue aby omówić proponowane zmiany.

## Zrzuty ekranu
*Dodaj tutaj zrzuty ekranu aplikacji po uruchomieniu*

## Status
✅ **Działające funkcjonalności:**
- ✅ Przeglądanie studentów z kolorowym kodowaniem
- ✅ Filtrowanie po statusie zdania (zdający/niezdający)
- ✅ Wyświetlanie szczegółowych profili studentów
- ✅ Kompleksowe statystyki i analizy akademickie
- ✅ Dodawanie nowych studentów przez dialog
- ✅ Automatyczne obliczanie średnich i zapisywanie danych
- ✅ Responsywny interfejs z nawigacją hamburger menu
- ✅ Pełna funkcjonalność menu bocznego

🎯 **Wszystkie główne funkcje zostały zaimplementowane!**

🔄 **Możliwe przyszłe ulepszenia:**
- Edycja istniejących danych studentów
- Eksport raportów do PDF/Excel
- Zaawansowane filtry (po średniej, przedmiocie)
- Zarządzanie zdjęciami studentów
- Import danych z plików CSV
