-- This file should contain all code required to create & seed database tables.
DROP TABLE IF EXISTS visitor_ratings;
DROP TABLE IF EXISTS assistance;
DROP TABLE IF EXISTS emergencies;
DROP TABLE IF EXISTS rating_classification;
DROP TABLE IF EXISTS exhibitions;
DROP TABLE IF EXISTS departments; 
DROP TABLE IF EXISTS floors;


CREATE TABLE assistance (
    assistance_id SERIAL PRIMARY KEY,
    at TIMESTAMPTZ NOT NULL UNIQUE DEFAULT CURRENT_TIMESTAMP,
    exhibition_id SMALLINT NOT NULL
);


CREATE TABLE emergencies (
    emergency_id SERIAL PRIMARY KEY,
    at TIMESTAMPTZ NOT NULL UNIQUE DEFAULT CURRENT_TIMESTAMP,
    exhibition_id SMALLINT NOT NULL
);


CREATE TABLE visitor_ratings (
    visitor_rating_id SERIAL PRIMARY KEY,
    rating_classification_id INT,
    at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exhibition_id SMALLINT NOT NULL
);


CREATE TABLE rating_classification (
    rating_classification_id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL, 
    number SMALLINT NOT NULL
);


CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE floors (
    floor_id SERIAL PRIMARY KEY,
    floor VARCHAR(50) NOT NULL
);


CREATE TABLE exhibitions (
    exhibition_id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255) UNIQUE NOT NULL, 
    department_id SMALLINT NOT NULL, 
    start_date date NOT NULL,
    floor_id SMALLINT NOT NULL
);


ALTER TABLE exhibitions
    ADD CONSTRAINT department_fk
    FOREIGN KEY (department_id)
        REFERENCES departments(department_id);

ALTER TABLE exhibitions
    ADD CONSTRAINT floor_fk
    FOREIGN KEY (floor_id)
        REFERENCES floors(floor_id);


ALTER TABLE assistance
    ADD CONSTRAINT exhibition_fk
    FOREIGN KEY (exhibition_id)
        REFERENCES exhibitions(exhibition_id);


ALTER TABLE emergencies
    ADD CONSTRAINT exhibition_fk
    FOREIGN KEY (exhibition_id)
        REFERENCES exhibitions(exhibition_id);


ALTER TABLE visitor_ratings
    ADD CONSTRAINT exhibition_fk
    FOREIGN KEY (exhibition_id)
        REFERENCES exhibitions(exhibition_id);


ALTER TABLE visitor_ratings
    ADD CONSTRAINT rating_classification_fk
    FOREIGN KEY (rating_classification_id)
        REFERENCES rating_classification(rating_classification_id);
        

INSERT INTO rating_classification (rating_classification_id, description, number) VALUES (0, 'Angry', 0);
INSERT INTO rating_classification (rating_classification_id, description, number) VALUES (1, 'Sad', 1);
INSERT INTO rating_classification (rating_classification_id, description, number) VALUES (2, 'Neutral', 2);
INSERT INTO rating_classification (rating_classification_id, description, number) VALUES (3, 'Good', 3);
INSERT INTO rating_classification (rating_classification_id, description, number) VALUES (4, 'Amazing!', 4);


INSERT INTO departments (department_name) VALUES ('Entomology');
INSERT INTO departments (department_name) VALUES ('Geology');
INSERT INTO departments (department_name) VALUES ('Paleontology');
INSERT INTO departments (department_name) VALUES ('Zoology');
INSERT INTO departments (department_name) VALUES ('Ecology');



INSERT INTO floors (floor) VALUES ('1');
INSERT INTO floors (floor) VALUES ('2');
INSERT INTO floors (floor) VALUES ('3');
INSERT INTO floors (floor) VALUES ('Vault');



INSERT INTO exhibitions (exhibition_id, name, description, department_id, start_date, floor_id) VALUES (
        0,
        'Measureless to Man',
        'An immersive 3D experience: delve deep into a previously-inaccessible cave system.', 
        2, 
        '2021-08-23',
        1
    ),
    (   1,
        'Adaptation',
         'How insect evolution has kept pace with an industrialised world',
         1,
         '2019-07-01',
         4
        ),
    (
        2,
        'Thunder Lizards',
        'How new research is making scientists rethink what dinosaurs really looked like.',
        3,
        '2023-02-01',
        1
    ),
    (
        3,
        'The Crenshaw Collection',
        'An exhibition of 18th Century watercolours, mostly focused on South American wildlife.',
        4,
        '2021-03-03',
        2
    ),
    (
        4,
        'Our Polluted World',
        'A hard-hitting exploration of humanity''s impact on the environment.',
        5,
        '2021-05-12',
        3
    ),
    (
        5,
        'Cetacean Sensations',
        'Whales: from ancient myth to critically endangered.',
        4,
        '2019-07-01',
        1
    );
