CREATE TABLE users
(
  id   INTEGER NOT NULL PRIMARY KEY,
  uuid TEXT
);

CREATE UNIQUE INDEX user_id_uindex
  ON users (id);

CREATE TABLE facts
(
  id      INTEGER NOT NULL PRIMARY KEY,
  name    TEXT    NOT NULL,
  value   TEXT    NOT NULL,
  state   BOOLEAN NOT NULL,
  type    TEXT    NOT NULL,
  user_id INTEGER NOT NULL,
  CONSTRAINT facts_users__fk FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE UNIQUE INDEX facts_id_uindex
  ON facts (id);

CREATE TABLE rules
(
  id INTEGER NOT NULL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  CONSTRAINT rules_users__fk FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE UNIQUE INDEX rule_id_uindex
  ON rules (id);

CREATE TABLE majors
(
  fact_id INTEGER NOT NULL,
  rule_id INTEGER NOT NULL,
  CONSTRAINT majors_facts__fk FOREIGN KEY (fact_id) REFERENCES facts (id),
  CONSTRAINT majors_facts__fk FOREIGN KEY (rule_id) REFERENCES rules (id)
);

CREATE TABLE conclusions
(
  fact_id INTEGER NOT NULL,
  rule_id INTEGER NOT NULL,
  CONSTRAINT majors_facts__fk FOREIGN KEY (fact_id) REFERENCES facts (id),
  CONSTRAINT majors_facts__fk FOREIGN KEY (rule_id) REFERENCES rules (id)
);