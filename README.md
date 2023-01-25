# SK2-IRC

Projekt stworzony w ramach przedmiot Sieci Komputerowe 2. Aplikacja działa na wzór czatu IRC - pozwala użytkownikom wysyłać wiadomości publiczne w ramach jednego pokoju i prywatne.
Autorzy Marcin Janicki 148240 i Wojciech Strykowski 148136
Adres repozytorium
https://gitlab.cs.put.poznan.pl/inf148240/IRC


# Opis protokołu komunikacyjnego

Aplikacja działa w architekturze Client-Server za pomocą Socketów. Serwer nasłuchuje, w celu nawiązania połączenia z nowym użytkownikiem. Kiedy pojawi się połączenie na serverze dodawany jest nowy użytkownik do serwera, przechowywany jest jego Socket. Po otrzymaniu połączenia server tworzy nowy wątek dla klienta, który będzie zajmował się jego obsługą.

Klient z drugiej strony operuje na dwóch wątkach - jeden do ogólnej obsługi akcji użytkownika, drugi odpowiadający za nasłuchiwanie i obsługę wiadomości przychodzących.  

## Struktura projektu
Client został napisany w Pythonie za pomocą biblioteki Socket do obsługi połączeń oraz biblioteki TKinter do stworzenia GUI. Server został napisany w języku C++.

Pierwszy znak każdej wiadomości jest liczbą całkowitą odpowiadającą za komendę którą dana wiadomość wywołuje.

Server w zależności od komendy wiadomości działa w następujący sposób:
 1. Stworzenie nowego pokoju
 2. Dołączenie do istniejącego już pokoju
 3. Wyjście z pokoju
 4. Wysłanie wiadomości do pokoju w którym aktualnie dany użytkownik się znajduje
 5. Wysłanie użytkownikowi informacji o wszystkich istniejących już pokojach oraz użytkownikach w nich
 6. Odłączenie clienta od servera
 7. Wysłanie wiadomości prywatnej



## Sposób kompilacji, uruchomienia i obsługi programów projektu.

Server kompilujemy poprzez wywołanie komendy "g++ -pthread server.cpp", a następnie uruchamiamy aplikacje poprzez komendę ./a.out (server domyślnie działa na porcie 1234)

Clienta odpalamy poprzez komendę python client.py, następnie musimy wpisać adres oraz port servera. Pojawia nam się okno, w którym musimy podać naszą nazwę użytkownika. Następnie musimy stworzyć pokój przykładowo nr 0, potem możemy kliknąć przycisk "Open chat window". Odpalamy drugiego klienta, ponownie podajemy nazwe użytkownika, możemy od razu wybrać opcję Join a Room i wybrać pokój 0 i możemy już chatować z drugim clientem. Gdybyśmy byli w innym pokoju, możemy napisać wiadomość prywatną do innego clienta poprzez wpisanie "/w [nick clienta] wiadomość".

