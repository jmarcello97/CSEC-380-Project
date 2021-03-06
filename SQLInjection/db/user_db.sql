

CREATE DATABASE users;
USE users;

DROP TABLE IF EXISTS User;

CREATE TABLE User (
	UserID int(5) NOT NULL,
	Username varchar(15) NOT NULL,
	PasswordHash varchar(200) NOT NULL,
	DisplayName varchar(15) NOT NULL,
	PRIMARY KEY (UserID)
);

-- Insert user for testing purposes
INSERT INTO User VALUES(1, "admin", "$5$rounds=535000$Lz8amuEeaJdfDLJ7$VzAbQapAX6F8rItWDJIDlNFrj80rg/xx7ItGAUjqehA", "admin");

DROP TABLE IF EXISTS Video;

CREATE TABLE Video (
	UserID int(5) NOT NULL,
	VideoID int(5) NOT NULL,
	URL varchar(50) NOT NULL,
	Name varchar(30) NOT NULL,
	UploadDate date NOT NULL,
	PRIMARY KEY (UserID, VideoID),
	CONSTRAINT fk1 FOREIGN KEY (UserID) REFERENCES User (UserID)
);
