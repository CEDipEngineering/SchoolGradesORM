USE Notas;
DROP TABLE IF EXISTS User_has_Class;
DROP TABLE IF EXISTS Note;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Class;

CREATE TABLE User (
    idUser INT NOT NULL AUTO_INCREMENT,
    nameUser VARCHAR(45),
    PRIMARY KEY (idUser)
);

CREATE TABLE User_has_Class (
    idUser INT,
    idClass INT,
    PRIMARY KEY (idUser, idClass)
);

CREATE TABLE Class (
	idClass INT NOT NULL AUTO_INCREMENT,
    nameClass VARCHAR(45) NOT NULL,
    Professor VARCHAR(45),
    PRIMARY KEY (idClass)
);

CREATE TABLE Note (
    idNote INT NOT NULL AUTO_INCREMENT,
    idUser INT NOT NULL,
    idClass INT NOT NULL,
    nota TEXT(200),
    PRIMARY KEY (idNote)
);


ALTER TABLE User_has_Class ADD FOREIGN KEY (idUser) REFERENCES User (idUser);
ALTER TABLE User_has_Class ADD FOREIGN KEY (idClass) REFERENCES Class (idClass);
ALTER TABLE Note ADD FOREIGN KEY (idUser) REFERENCES User (idUser);
ALTER TABLE Note ADD FOREIGN KEY (idClass) REFERENCES Class (idClass);
