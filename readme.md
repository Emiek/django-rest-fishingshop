# Webcam API

## Przeznaczenie
System przeznaczony na potrzeby realizacji przedmiotu Programowanie Serwisów Internetowych na UWM. 
Prezentowany kod źródłowy to przykładowy system napisany za pomocą frameworków Django oraz Django REST przy użyciu języka Python w wersji 3.11.6.
System jest zbiorem dobrych praktyk, których warto przestrzegać podczas pracy z frameworkiem Django.
Warto mieć jednak na uwadze fakt, że w niektórych przypadkach - 
z uwagi na czytelność kodu i początkujący poziom odbiorców - zostały wprowadzone rozwiązania czytelniejsze w porównaniu
z dobrymi praktykami, których nie należy stosować w rozwiązaniach produkcyjnych. Oto niektóre z nich wraz z propozycjami
lepszych rozwiązań:
- aplikacja **core** powinna zawierać wszystkie modele danych, alternatywnie - mogą być zawarte w osobnym pakiecie na poziomie głównym systemu,
- do testów została wykorzystana wbudowana biblioteka **unittest**, która nie przestrzega zasady poprawności zapisu kodu języka Python (**snake_case**), używaja zamiast tego **cammelCase**; lepszym rozwiązaniem jest np. biblioteka **pytest**,
- testy zostały przygotowane w sposób powtarzalny, co ma na celu ułatwienie ich analizy, szczególnie na początku drogi z Django; lepszym rozwiązaniem jest zastosowanie parametryzowanych testów, również z domieszkami,
- funkcjonalność wyszukiwania kamer w promieniu *n* km od użytkownika została zaimplementowana w najprostszy możliwy sposób, bez uwzględniania jednak krzywizny kuli ziemskiej (odległość euklidesowa);
lepszym rozwiązaniem byłoby wykorzystanie biblioteki **GeoDjango** wraz z rozszerzeniem bazy danych **PostGIS**; 
z uwagi na wykorzystanie kontenera z minimalną dystrybucją systemu Linux pod spodem (**Alpine**) proces instalacji bieżącej wersji rozszerzenia **PostGIS** jest skrajnie trudny, co w efekcie może wymagać zastosowania kontenera z cieższą dystrybucją Linuxa pod spodem (np. **Ubuntu** lub **Debian**), a nawet wprost - wykorzystania wirtualizacji. 

## Opis systemu

System umożliwiający operacje CRUD na referencjach do kamer internetowych dostępnych w sieci. 
Kamery podzielone są na kategorie oraz względem lokalizacji (kontynent/kraj). 
Zalogowani użytkownicy mogą dodawać komentarze do kamer. Odczytywać komentarze moga wszyscy użytkownicy.

Zalogowani użytkownicy mogą dodawać nowe kamery, a także komentarze pod nimi. 
Użytkownicy mogą dodawać także istniejące kamery do listy ulubionych.

Kategorie oraz lista krajów i kontynentów może być zarządzana jedynie przez administratora systemu.

## Aplikacje

### Core

Aplikacja przeznaczona na potrzeby wewnętrzne systemu.

### User

Modele

User
- ID
- Nick
- E-mail
- Password
- Favourites

### Locations

Modele

Continent
- ID
- Name

Country
- ID
- Name
- Continent

### Webcam

Modele

Webcam
- ID
- Name
- Description
- URL
- Image URL
- Coords
- Category
- Country
- Comments
- Added (date)
- Added (user)

Category
- ID
- Name

Comment
- ID
- User
- Content
- Date

## Stos technologiczny

System uruchamiany jest za pomocą narzędzia Docker compose, gdzie zawarte są następujące kontenery:
- app: REST API przygotowane w Django REST Framework
- db: relacyjna baza danych PostgreSQL

