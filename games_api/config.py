import sqlite3

def seed_db(db, cursor):

  cursor.execute("""CREATE TABLE IF NOT EXISTS played_statuses (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    played_status TEXT
  
  )""")

  cursor.execute("SELECT COUNT(*) FROM played_statuses")
  played_status_count = cursor.fetchone()[0]

  if played_status_count == 0:

    cursor.execute("""INSERT INTO played_statuses (played_status) VALUES 
    
      ('Never played'),
      ('Playing'),
      ('Played')

    """)

    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS genres (

      id INTEGER PRIMARY KEY AUTOINCREMENT,
      genre TEXT

    )""")

    cursor.execute("""INSERT INTO genres (genre) VALUES 
    
      ('Shooter'),
      ('Action'),
      ('Adventure'),
      ('Role Playing Game'),
      ('Strategy'),
      ('Fighting'),
      ('Puzzle'),
      ('Racing'),
      ('Sports'),
      ('Platformer'),
      ('Simulation'),
      ('Survival'),
      ('Sandbox'),
      ('Educational'),
      ('Horror')
    
    """)

    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS companies (
    
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      company TEXT
    
    )""")

    db.commit()

    cursor.execute("""INSERT INTO companies (company) VALUES 
    
      ('Sony'),
      ('Microsoft'),
      ('Nintendo'),
      ('Sega'),
      ('Atari'),
      ('Magnavox'),
      ('Multiple / Various')
    
    """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS consoles (

      id INTEGER PRIMARY KEY AUTOINCREMENT,
      console TEXT,
      slug TEXT,
      company_id INTEGER,

      FOREIGN KEY (company_id) REFERENCES companies(id)
    
    )""")

    cursor.execute("""INSERT INTO consoles (console, slug, company_id) VALUES

      ('Playstation 1','ps1', 1),
      ('Playstation 2','ps2', 1),
      ('Playstation 3','ps3', 1),
      ('Playstation 4','ps4', 1),
      ('Playstation 5','ps5', 1),
      ('Xbox', 'xbox', 2),
      ('Xbox 360', 'xbox-360', 2),
      ('Xbox One', 'xbox-1', 2),
      ('Xbox Series X', 'xbox-sx', 2),
      ('Nintendo Ds', 'nds', 3),
      ('Nintendo Switch', 'ns', 3),
      ('Nintendo Switch 2', 'ns2', 3),
      ('Wii', 'wii', 3),
      ('Computer', 'pc', 7),
      ('Nintendo Entertainment System', 'nes', 3),
      ('Super Nintendo', 'sn', 3),
      ('Sega Genesis', 'sg', 4),
      ('Atari 2600', 'a-2600', 5),
      ('Magnavox, Odyssey', 'mo', 6),
      ('Nintendo 64', 'n-64', 3),
      ('Sega Saturn', 'ss', 4),
      ('Nintendo Gamecube', 'ng', 3),
      ('Dreamcast', 'd', 4),
      ('Game Boy Advance', 'gba', 3),
      ('Playstation Portable', 'psp', 1),
      ('Wii U', 'wu', 3),
      ('Nintendo 3DS', 'n-3ds', 3),
      ('Playstation Vita', 'pv', 1)

    """)

    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS own_statuses (
    
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      own_status TEXT
    
    )""")

    cursor.execute("""INSERT INTO own_statuses (own_status) VALUES 
        
      ('Want'),
      ('Borrowed'),
      ('Have')
    
    """)

    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS games (
    
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      played_status_id INTEGER,
      own_status_id INTEGER,

      FOREIGN KEY (played_status_id) REFERENCES played_statuses(id),
      FOREIGN KEY (own_status_id) REFERENCES own_statuses(id)

    )""")

    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS game_console (

      game_id INTEGER,
      console_id INTEGER,

      PRIMARY KEY (game_id, console_id),

      FOREIGN KEY (game_id) REFERENCES games(id),
      FOREIGN KEY (console_id) REFERENCES consoles(id)

    )""")

    db.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS game_genre (

      game_id INTEGER,
      genre_id INTEGER,

      PRIMARY KEY (game_id, genre_id),

      FOREIGN KEY (game_id) REFERENCES games(id),
      FOREIGN KEY (genre_id) REFERENCES genres(id)
    
    )""")

    db.commit()
    db.close()