drop user if exists 'admin'@'localhost';
create user 'admin'@'localhost' identified by 'admin';
grant all privileges on * . * to 'admin'@'localhost';
ALTER USER 'admin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin';
flush PRIVILEGES;

drop schema if exists comp353;

create schema comp353;

USE comp353;

CREATE TABLE test (
    name VARCHAR(45),
    PRIMARY KEY (name)
);

INSERT test (name)
VALUES
("bob")
;