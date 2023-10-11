# CREATE DATABASE items;

CREATE TABLE IF NOT EXISTS items_rating (
   id      INT    NOT NULL AUTO_INCREMENT,
   item_id INT    NOT NULL,
   rating  FLOAT,
   PRIMARY KEY (ID),
   FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE
);

INSERT INTO items_rating ( item_id, rating ) VALUES
  ( 1, 4.9 ), ( 1, 5.0 ), ( 1, 3.8 ), ( 1, 4.9 ),
  ( 2, 2.2 ), ( 2, 4.2 ),
  ( 4, 4.4 ),
  ( 5, 5.0 ), ( 5, 1.0);
