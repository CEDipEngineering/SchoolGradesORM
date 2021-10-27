USE Notas;

-- User
INSERT INTO User VALUES (1,"Thomas"), (2,"Martha"), (3,"Bruce"), (4,"Alfred"), (5,"Gordon");

-- Class
INSERT INTO Class VALUES (1,"MatVar","Calculo I", "Orfali"), 
						 (2,"CDados","Estatistica e ML", "Ayres"),
                         (3,"DesProg","Algoritmos e Complexidades", "Hashi"),
                         (4,"Nuvem","Arquitetura de Computação em Nuvem", "Raul");
                         
-- User_has_Class
INSERT INTO User_has_Class VALUES (1,1),(2,1),(3,2),(3,3),(3,4),(5,4);

-- Grade
INSERT INTO Grade VALUES (1,1,1,7.3),(2,2,1,5.7),(3,2,1,7.3),(4,3,3,9),(5,3,4,2.1);
