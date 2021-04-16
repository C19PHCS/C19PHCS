drop user if exists 'admin'@'localhost';
create user 'admin'@'localhost' identified by 'admin';
grant all privileges on * . * to 'admin'@'localhost';
ALTER USER 'admin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'admin';
flush PRIVILEGES;

drop schema if exists comp353;

create schema comp353;

USE comp353;

CREATE TABLE `publicHealthCenter` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `address` varchar(255) NOT NULL,
    `webAddress` varchar(255) NOT NULL,
    `phoneNumber` varchar(15) NOT NULL,
    `type` enum('hospital','clinic','special_installment') NOT NULL,
    `city` varchar(45) NOT NULL,
    `province` char(2) NOT NULL,
    `country` varchar(45) NOT NULL,
    `postalCode` char(6) NOT NULL,
    PRIMARY KEY (`id`)
);