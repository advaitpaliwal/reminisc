CREATE TABLE classifications (
  id UUID PRIMARY KEY,
  input TEXT NOT NULL,
  classification BOOLEAN NOT NULL,
  model TEXT NOT NULL,
  timestamp TIMESTAMP NOT NULL
);