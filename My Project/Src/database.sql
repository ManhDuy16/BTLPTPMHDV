CREATE TABLE users (
	id int(11) PRIMARY KEY AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);

CREATE TABLE books (
	id int(11) PRIMARY KEY AUTO_INCREMENT,
    title varchar(255) NOT NULL,
    author varchar(255) NOT NULL,
    tags text,
    year_xb varchar(255) NOT NULL
);

CREATE TABLE rent_books (
	id int(11) PRIMARY KEY AUTO_INCREMENT,
    id_book int(11),
    FOREIGN KEY (id_book) REFERENCES books(id),
    name varchar(255) NOT NULL,
    studentId varchar(255) NOT NULL,
    date timestamp
);
