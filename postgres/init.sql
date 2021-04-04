CREATE DATABASE xythrion_postgres;

\c xythrion_postgres;

CREATE TABLE IF NOT EXISTS Dates(
    identification serial PRIMARY KEY,
    created_on TIMESTAMP WITH TIME ZONE,
    user_id BIGINT,
    name TEXT,
    time TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS Blocked_Guilds(
    identification serial PRIMARY KEY,
    created_on TIMESTAMP WITH TIME ZONE,
    guild_id BIGINT
);

CREATE TABLE IF NOT EXISTS Blocked_Users(
    identification serial PRIMARY KEY,
    created_on TIMESTAMP WITH TIME ZONE,
    user_id BIGINT
);
