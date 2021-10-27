USE Notas;
DROP TABLE IF EXISTS User_has_Class;
DROP TABLE IF EXISTS Grade;
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
    Notes TEXT(200),
    Professor VARCHAR(45),
    PRIMARY KEY (idClass)
);

CREATE TABLE Grade (
    idGrade INT NOT NULL AUTO_INCREMENT,
    idUser INT NOT NULL,
    idClass INT NOT NULL,
    nota DOUBLE,
    PRIMARY KEY (idGrade)
);


ALTER TABLE User_has_Class ADD FOREIGN KEY (idUser) REFERENCES User (idUser);
ALTER TABLE User_has_Class ADD FOREIGN KEY (idClass) REFERENCES Class (idClass);
ALTER TABLE Grade ADD FOREIGN KEY (idUser) REFERENCES User (idUser);
ALTER TABLE Grade ADD FOREIGN KEY (idClass) REFERENCES Class (idClass);
