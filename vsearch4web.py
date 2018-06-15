
from flask import Flask, render_template, request, escape
from vsearch import search4letters

from DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB', }


def log_request(req: 'flask_request', res: str) -> None:
   """Logs the details of the network request and results."""
   with UseDatabase(app.config['dbconfig']) as cursor:
      _SQL = """insert into log
                (phrase, letters, ip, browser_string, results)
                values
                (%s, %s, %s, %s, %s)"""
      cursor.execute(_SQL, (req.form['phrase'],
                            req.form['letters'],
                            req.remote_addr,
                            req.user_agent.browser,
                            res, ))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
   """It extracts the transferred data; performs a search; returns results."""
   phrase = request.form['phrase']
   letters = request.form['letters']
   title = 'Oto Twoje wyniki:'
   results = str(search4letters(phrase, letters))
   log_request(request, results)
   return render_template('results.html',
                          the_title=title,
                          the_phrase=phrase,
                          the_letters=letters,
                          the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
   """Displays the HMTL form of this web application."""
   return render_template('entry.html',
                          the_title='Witamy na stronie internetowej search4letters!')


@app.route('/viewlog')
def view_the_log() -> 'html':
   """Displays the contents of the log file in the HTML table."""
   with UseDatabase(app.config['dbconfig']) as cursor:
      _SQL = """select phrase, letters, ip, browser_string, results
                from log"""
      cursor.execute(_SQL)
      contents = cursor.fetchall()
   titles = ('Fraza', 'Adres klienta', 'Agent użytkownika', 'Wyniki')
   return render_template('viewlog.html',
                          the_title='Widok logu',
                          the_row_titles=titles,
                          the_data=contents,)


if __name__ == '__main__':
   app.run(debug=True)
