#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
    @description: this is a python script to create a database with 3 tables
    for a mamy-to-many relationship
    @author: Manuel Parra
    @date: 06/01/19
"""

import sqlite3
import json
import sys

conn = sqlite3.connect('manytomany.sqlite')
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        card_id TEXT UNIQUE,
        name TEXT,
        email TEXT
    );

    CREATE TABLE IF NOT EXISTS Course (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Member (
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        role INTEGER,
        PRIMARY KEY (user_id, course_id)
    )
""")

fname = input('Enter file name (for file dafault press enter): ')
if len(fname) < 1: fname = 'data_sample.json'
if fname == 'quit': sys.exit()

try:
    fhand = open(fname)
except:
    print(f"Error opening the file {fname}")
    sys.exit()

try:
    js = json.loads(fhand.read())
except:
    print(f"This file {fname} doesn't containe a json structure!")
    sys.exit()

for entry in js:
    user_card_id = entry[0]
    user_name = entry[1]
    course_title = entry[2]
    user_email = entry[3]
    user_role = entry[4]

    cur.execute("""
        INSERT OR IGNORE INTO User (card_id, name, email)
        VALUES (?, ?, ?)
    """, (user_card_id, user_name, user_email))

    cur.execute("""
        SELECT id
        FROM User
        WHERE card_id = ?
    """, (user_card_id, ))
    user_id = cur.fetchone()[0]

    cur.execute("""
        INSERT OR IGNORE INTO Course (title)
        VALUES (?)
    """, (course_title, ))

    cur.execute("""
        SELECT id
        FROM Course
        WHERE title = ?
    """, (course_title, ))
    course_id = cur.fetchone()[0]

    cur.execute("""
        INSERT OR IGNORE INTO Member (user_id, course_id, role)
        VALUES (?, ?, ?)
    """, (user_id, course_id, user_role))

conn.commit()

cur.execute("""
    SELECT User.card_id, User.name, User.email, Course.Title, Member.role
    FROM User JOIN Member JOIN Course
         ON User.id = Member.user_id
         AND Member.course_id = Course.id
    ORDER BY User.name ASC, Course.title ASC
""")

for row in cur:
    print("-"*15)
    print(f"Card ID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Email: {row[2]}")
    print(f"Course: {row[3]}")
    print(f"Role: {row[4]}")

cur.close()
