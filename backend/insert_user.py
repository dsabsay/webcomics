import argparse
import sqlite3

from werkzeug.security import generate_password_hash

def main(args):
    conn = sqlite3.connect("instance/webcomics.sqlite")

    conn.execute(
        'INSERT INTO users (name, password) VALUES (?, ?)',
        (args.username, generate_password_hash(args.password))
    )
    conn.commit()

    print('Done.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a user into the database.')
    parser.add_argument('username', type=str, help='Username.')
    parser.add_argument('password', type=str, help='Password. Will be hashed before being stored.')

    args = parser.parse_args()
    main(args)
