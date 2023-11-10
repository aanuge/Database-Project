DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS arrakis_members;
DROP TABLE IF EXISTS comedy_members;
DROP TABLE IF EXISTS arrakis_channels;
DROP TABLE IF EXISTS comedy_channels;
DROP TABLE IF EXISTS arrakis_messages;
DROP TABLE IF EXISTS comedy_messages;


CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(1000) NOT NULL DEFAULT '123',
    session_key TEXT,
    unread_count INTEGER NOT NULL DEFAULT 0,
    email VARCHAR(40) NOT NULL DEFAULT 'user@email.com',
    phone VARCHAR(12) NOT NULL DEFAULT '012-345-6789',
    usernamechange TIMESTAMP NOT NULL DEFAULT '0001-01-01'
);

CREATE TABLE messages(
    id SERIAL PRIMARY KEY,
    sender VARCHAR(30) NOT NULL,
    recipient VARCHAR(30) NOT NULL,
    content VARCHAR(300) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT '2000-01-01',
    status VARCHAR(6) NOT NULL DEFAULT 'unread'
);

CREATE TABLE arrakis_members(
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    user_id INTEGER NOT NULL,
    suspension TIMESTAMP NOT NULL DEFAULT '001-01-01'
);

CREATE TABLE comedy_members(
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    user_id INTEGER NOT NULL,
    suspension TIMESTAMP NOT NULL DEFAULT '001-01-01'
);

CREATE TABLE arrakis_channels(
    id SERIAL PRIMARY KEY,
    channel_name VARCHAR(30) NOT NULL
);

CREATE TABLE comedy_channels(
    id SERIAL PRIMARY KEY,
    channel_name VARCHAR(30) NOT NULL
);

CREATE TABLE arrakis_messages(
    id SERIAL PRIMARY KEY,
    channel_id INTEGER NOT NULL,
    sender VARCHAR(30) NOT NULL,
    content VARCHAR(300),
    timestamp TIMESTAMP NOT NULL
);

CREATE TABLE comedy_messages(
    id SERIAL PRIMARY KEY,
    channel_id INTEGER NOT NULL,
    sender VARCHAR(30) NOT NULL,
    content VARCHAR(300),
    timestamp TIMESTAMP NOT NULL
);

INSERT INTO users(username, unread_count) VALUES
    ('Abbott', DEFAULT),
    ('Costello', 1),
    ('Moe', 1),
    ('Larry', DEFAULT),
    ('Curly', 1),
    ('Bob', DEFAULT),
    ('DrMarvin', 1),
    ('spicelover', DEFAULT),
    ('Paul', DEFAULT);

INSERT INTO messages(sender, recipient, content, timestamp, status) VALUES
    ('Larry', 'Costello', 'Larry to Costello 1956', '1956-05-06 00:00:00', DEFAULT),
    ('Abbott', 'Costello', 'Abbott to Costello 1923', '1923-02-03 00:00:00', 'read'),
    ('Costello', 'Abbott', 'Costello to Abbott 1940', '1940-04-04 00:00:00', 'read'),
    ('Curly', 'Abbott', 'Curly to Abbott 1960', '1960-06-06 00:00:00', 'unread'),
    ('Moe', 'Larry', 'Moe to Larry 1970', '1970-07-07 00:00:00', 'read'),
    ('Larry', 'Moe', 'Larry to Moe 1955', '1955-05-05 00:00:00', 'read'),
    ('Paul', 'Moe', 'Paul to Moe 1955', '2055-05-05 00:00:00', 'read'),
    ('Moe', 'Paul', 'Moe to Paul 1955', '2055-05-05 00:00:00', 'read'),
    ('Moe', 'Paul', 'dingus', '2055-05-06 00:00:00', 'read'),
    ('Curly', 'Moe', 'Curly to Moe 2000', '2000-01-01 00:00:00', 'read'),
    ('Bob', 'DrMarvin', 'Im doing the work, Im baby-stepping', '1991-05-18', 'read');

INSERT INTO comedy_members(username, user_id, suspension) VALUES
    ('Abbott', 1, DEFAULT),
    ('Costello', 2, DEFAULT),
    ('Moe', 3, DEFAULT),
    ('Larry', 4, DEFAULT),
    ('Curly', 5, DEFAULT),
    ('Bob', 6, DEFAULT),
    ('DrMarvin', 7, DEFAULT),
    ('spicelover', 8, DEFAULT),
    ('Paul', 9, DEFAULT);

INSERT INTO arrakis_members(username, user_id, suspension) VALUES
    ('spicelover', 8, DEFAULT);

INSERT INTO comedy_channels(channel_name) VALUES
    ('#ArgumentClinic'),
    ('#Dialog');

INSERT INTO arrakis_channels(channel_name) VALUES
    ('#Worms'),
    ('#Random');

INSERT INTO arrakis_messages(channel_id, sender, content, timestamp) VALUES
    (1, 'Paul', '@spicelover', '2001-01-01'),
    (2, 'Paul', 'ooooohhhhh', '2010-01-01'),
    (2, 'Paul', 'hi', '2020-01-01');

INSERT INTO comedy_messages(channel_id, sender, content, timestamp) VALUES
    (1, 'Moe', '@spicelover', '2001-01-01'),
    (2, 'Paul', 'AAAHHH', '2010-01-01'),
    (2, 'Larry', 'please reply', '2001-01-01'),
    (2, 'Larry', 'i replyed already!', '2001-01-01');
