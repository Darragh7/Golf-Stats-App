DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
DROP TABLE IF EXISTS rounds;

CREATE TABLE rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    name TEXT NOT NULL,
    score INTEGER NOT NULL,
    handicap INTEGER NOT NULL
);
DROP TABLE IF EXISTS putting_stats;

CREATE TABLE putting_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    puts_per_round INTEGER NOT NULL,
    one_putt_percent INTEGER NOT NULL,
    three_putt_avoid INTEGER NOT NULL,
    avg_putt_dist INTEGER NOT NULL
);




