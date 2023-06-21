card_table_migration = '''
DROP TABLE IF EXISTS cards;
CREATE TABLE IF NOT EXISTS cards (
    id SERIAL PRIMARY KEY,
    pan VARCHAR(50) NOT NULL,
    expiry_date VARCHAR(50) NOT NULL,
    cvv VARCHAR(100) NOT NULL,
    issue_date VARCHAR(50) NOT NULL,
    owner_id VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL
);
'''