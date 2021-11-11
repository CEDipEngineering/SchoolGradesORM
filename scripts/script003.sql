USE Notas;

-- User
INSERT INTO User VALUES (1,"Thomas"), (2,"Martha"), (3,"Bruce"), (4,"Alfred"), (5,"Gordon");

-- Class
INSERT INTO Class VALUES (1,"MatVar", "Orfali"), 
						 (2,"CDados", "Ayres"),
                         (3,"DesProg", "Hashi"),
                         (4,"Nuvem", "Raul");
                         
-- User_has_Class
INSERT INTO User_has_Class VALUES (1,1),(2,1),(3,2),(3,3),(3,4),(5,4);

-- Grade
INSERT INTO Note VALUES (1,1,1,"7.3"),(2,2,1,"5.7"),(3,2,1,"7.3"),(4,3,3,"9"),(5,3,4,"2.1"), (6,1,1,"Opa"),(7,2,1,"É, uma matéria"),(8,2,1,"Quando?"),(9,3,3,"Batarang"),(10,3,4,"2.1");
