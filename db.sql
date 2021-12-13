CREATE DATABASE IF NOT EXISTS `proj` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `proj`;

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(100) NOT NULL,
    PRIMARY KEY(`id`)
);

select * from accounts ;

CREATE TABLE IF NOT EXISTS `user_movie` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `movie` varchar(255) NOT NULL,
    `rating` varchar(50) NOT NULL,
    PRIMARY KEY(`id`),
    unique KEY `key1` (`username`, `movie`)
);