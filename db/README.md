
# Intro

This folder stores the SQLite file used for inserting batch information
into the `RediBatch` table

# Table structure

CREATE TABLE RediBatch (
   rbID INTEGER PRIMARY KEY AUTOINCREMENT,
   rbStartTime TEXT NOT NULL,
   rbEndTime TEXT,
   rbStatus TEXT,
   rbMd5Sum TEXT NOT NULL
);

# Tools for debugging

You can run the following commands from the ./db folder to check the contents of the `RediBatch` table

   $ make list
   $ make last

