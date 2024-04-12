import argparse
from sys import exit
from sqlite3 import connect
from prettytable import from_db_cursor


BANNER = '''
 __      __      ___. ___________           .__          
/  \    /  \ ____\_ |_\__    ___/___   ____ |  |   ______
\   \/\/   // __ \| __ \|    | /  _ \ /  _ \|  |  /  ___/
 \        /\  ___/| \_\ \    |(  <_> |  <_> )  |__\___ \ 
  \__/\  /  \___  >___  /____| \____/ \____/|____/____  >
       \/       \/    \/                              \/ 

Interactive list of useful online tools
'''

def outAll() -> int:
     print('Use the numbers to select a category:\n')
     types = cur.execute('SELECT * FROM types').fetchall()
     for i in types:
          print(f'[{i[0]}] {i[1]}')
     return len(types)


def outOne(x: str) -> None:
     print(cur.execute('SELECT type FROM types WHERE id=?', (x,)).fetchone()[0], '\n')
     print(from_db_cursor(cur.execute('SELECT rating, name, url, desc FROM sites WHERE typ=? ORDER BY rating ASC', (x,))))


def main(maxx: int) -> None:
     while True:
          try:
               inp = input('\n\r> ')
          except KeyboardInterrupt:
               con.close()
               print('Bye!')
               exit()
          print('\x1b[H\x1b[2J', end='')
         
          if inp == '0':
               outAll()
          
          elif inp.isdigit() and int(inp) <= maxx - 1:
               outOne(inp)
          
          elif '+' in inp:
               try:
                    select = cur.execute('SELECT rating, name, url, desc FROM sites WHERE name=?', (inp.split()[1],)).fetchone()
                    cur.execute('INSERT INTO sites (rating, name, url, desc, typ) VALUES(?, ?, ?, ?, 1)', (select[0], select[1], select[2], select[3]))
                    con.commit()
                    print('Tool added!')
               except Exception:
                    print('Usage: + <ToolName>')
          
          elif '-' in inp:
               try:
                    cur.execute('DELETE FROM sites WHERE typ=1 AND name=?', (inp.split()[1],))
                    con.commit()
                    print('Tool removed!')
               except Exception as e:
                    print('Usage: - <ToolName>')

          elif inp == 'h' or inp == 'help':
               print(f'[0] Menu\n[1] Favorites\n[2-{maxx - 1}] To select a category\n[+ <ToolName>] To add tool to favorites\n[- <ToolName>] To remove tool from favorites')


if __name__ == '__main__':
     con = connect('main.db')
     cur = con.cursor()
     parser = argparse.ArgumentParser()
     parser.add_argument('-f', '--favorites', help='show favorite tools', action='store_true')
     args = parser.parse_args()
     
     if args.favorites:
          print('WebTools v1.0')
          outOne('1')
          exit()
     
     print(BANNER)
     main(outAll())
