-- THUC HANH INDEX

CREATE TABLE books (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    name   VARCHAR(50),
    author VARCHAR(10),
    year   INT,
    type   VARCHAR(5),
    price  INT
);
INSERT INTO books (name, author, year, type, price) VALUES
('Doraemon', 'BC',  1001, 'A', 50000),
('Meo',      'abc', 2006, 'B', 30000),
('GAU',      'CA',  1995, 'A', 40000),
('Conan',    'XY',  1994, 'A', 45000),
('Naruto',   'MK',  1999, 'B', 35000),
('Bleach',   'TK',  2001, 'B', 32000),
('OnePiece', 'EO',  1997, 'A', 55000),
('Dragon',   'AT',  1984, 'A', 48000),
('Slam',     'TI',  1990, 'B', 38000),
('Pokemon',  'SA',  1996, 'A', 42000);
EXPLAIN SELECT * FROM books WHERE name = 'Conan';
CREATE INDEX idx ON books(name);
SHOW INDEX FROM books;
EXPLAIN SELECT * FROM books WHERE name = 'Conan';
INSERT INTO books (name, author, year, type, price)
SELECT CONCAT(name, '_', id), author, year, type, price FROM books;
DROP INDEX idx ON books;
SELECT * FROM books WHERE name = 'Conan';  
CREATE INDEX idx ON books(name);
SELECT * FROM books WHERE name = 'Conan';   	  --duration nhanh hơn hẳn



-- TRANSACTION - COMMIT
drop table if exists bank;
CREATE table bank (
	id int primary key,
    name varchar(50),
    money int
);
insert into bank(id, name, money) values 
(1, 'ly', 1000),
(2, 'huy', 2000);
select * from bank;
start transaction;
update bank set money = money - 500 where id=1;
update bank set money = money + 500 where id=2;	
commit;
select * from bank;

-- TRANSACTION - ROLLBACK
drop table if exists bank;
CREATE table bank (
	id int primary key,
    name varchar(50),
    money int
);
insert into bank(id, name, money) values 
(1, 'ly', 1000),
(2, 'huy', 2000);
select * from bank;
start transaction;
update bank set money = money - 500 where id=1;
update bank set money = money + 500 where id=2;	
rollback;
select * from bank;
