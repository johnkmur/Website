CREATE TABLE User (
    username VARCHAR(20), 
    firstname VARCHAR(20) NOT NULL, 
    lastname VARCHAR(20) NOT NULL, 
    password VARCHAR(20) NOT NULL, 
    email VARCHAR(40) NOT NULL,
    PRIMARY KEY (username)
);
CREATE TABLE Album (
    albumid INT AUTO_INCREMENT NOT NULL, 
    title VARCHAR(50) NOT NULL, 
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL, 
    lastupdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL, 
    username VARCHAR(20) NOT NULL, 
    PRIMARY KEY (albumid),
    FOREIGN KEY (username) REFERENCES User(username) ON DELETE CASCADE
);
CREATE TABLE Photo (
    picid VARCHAR(40) NOT NULL,
    format CHAR(3) NOT NULL,
    caption VARCHAR (255) NOT NULL, 
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (picid)
);
CREATE TABLE Contain (
    sequencenum INT NOT NULL,
    albumid INT NOT NULL,
    picid VARCHAR(40) NOT NULL,
    FOREIGN KEY (albumid) REFERENCES Album(albumid) ON DELETE CASCADE,
    FOREIGN KEY (picid) REFERENCES Photo(picid) ON DELETE CASCADE
);