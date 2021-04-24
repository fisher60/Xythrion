CREATE DATABASE xythrion_postgres;

\c xythrion_postgres;

CREATE TABLE IF NOT EXISTS user_commands
(
    identification SERIAL PRIMARY KEY,
    executions     INT,
    completions    INT
);

CREATE TABLE IF NOT EXISTS dates
(
    identification SERIAL PRIMARY KEY,
    created_on     TIMESTAMP WITH TIME ZONE,
    user_id        BIGINT,
    name           TEXT,
    time           TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS blocked_guilds
(
    identification SERIAL PRIMARY KEY,
    created_on     TIMESTAMP WITH TIME ZONE,
    guild_id       BIGINT
);

CREATE TABLE IF NOT EXISTS blocked_users
(
    identification SERIAL PRIMARY KEY,
    created_on     TIMESTAMP WITH TIME ZONE,
    user_id        BIGINT
);
