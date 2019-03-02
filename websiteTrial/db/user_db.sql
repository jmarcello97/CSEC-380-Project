

DROP TABLE IF EXISTS User; 

CREATE TABLE User (
	UserID int(5) NOT NULL,
	Username varchar(15) NOT NULL,
	PasswordHash varchar(200) NOT NULL,
	DisplayName varchar(15) NOT NULL,
	PRIMARY KEY (UserID)
);

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