card_table_migration = '''
DROP TABLE IF EXISTS cards;
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pan TEXT,
    expiry_date TEXT,
    cvv TEXT,
    issue_date TEXT,
    owner_id TEXT,
    status TEXT
);
'''
