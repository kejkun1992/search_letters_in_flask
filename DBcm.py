"""Menedżer kontekstu UseDatabase umożliwiający korzystanie z bazy MySQL/MariaDB.

Więcej informacji na jego temat można znaleźć w rozdziałach 7, 8, 9 oraz 11 
książki "Python. Rusz głową! Wydanie II".

Prosty przykład jego użycia:

    from DBcm import UseDatabase, SQLError

    config = { 'host': '127.0.0.1',
               'user': 'mojUzytkownik',
               'password': 'mojeHaslo',
               'database': 'mojaBazaDanych' }

    with UseDatabase(config) as cursor:
        _SQL = "select * from log"
        cursor.execute(_SQL)
        data = cursor.fetchall()

Powodzenia i dobrej zabawy! (Niestety kod przeznaczony jest do użytku wyłącznie 
w Pythonie 3, z powodu zastosowania podpowiedzi typów i nowej składni).
"""

##############################################################################
# Menedżer kontekstu umożliwiający łączenie się z bazą danych i rozłączanie.
##############################################################################

import mysql.connector


class UseDatabase:

   def __init__(self, config: dict) -> None:
      """Dodaje parametry konfiguracji bazy danych do obiektu.

      Ta funkcja oczekuje argumentu będącego słownikiem, w którym odpowiednie
      wartości muszą być przypisane do (przynajmniej) tych kluczy:

         host - adres IP hosta, na którym działa baza MySQL/MariaDB.
         user - użytkownik bazy MySQL/MariaDB, z którego należy skorzystać.
         password - hasło tego użytkownika.
         database - nazwa bazy danych, której należy użyć.

      Więcej informacji na ten temat można znaleźć w dokumentacji narzędzia
      mysql-connector-python."""
      self.configuration = config

   def __enter__(self) -> 'cursor':
      """Łączy się z bazą danych i tworzy kursor.
      Zwraca kursor do menedżera kontekstu."""
      self.conn = mysql.connector.connect(**self.configuration)
      self.cursor = self.conn.cursor()
      return self.cursor

   def __exit__(self, exc_type, exc_value, exc_trace) -> None:
      """Niszczy kursor oraz połączenie (po skomitowaniu)."""
      self.conn.commit()
      self.cursor.close()
      self.conn.close()
