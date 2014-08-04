
help:
	@echo "Supported tasks:"
	@echo "\t tables     : list the tables in the database"
	@echo "\t schema     : show the columns in the RediBatch table"
	@echo "\t list       : list the redi batches that have been run"
	@echo "\t last       : show the row corresponding to the last redi batch run"
	@echo "\t add        : insert sample row in the RediBatch table"
	@echo "\t fresh      : create a fresh database file"
	@echo "\t clean      : remove all rows from the RediBatch table"


tables:
	sqlite3 redi.db .tables 

schema:
	sqlite3 redi.db 'PRAGMA table_info("RediBatch")'

# 0|	rbID			|INTEGER|0||1
# 1|	rbStartTime	|TEXT|1||0
# 2|	rbEndTime	|TEXT|0||0
# 3|	rbStatus		|TEXT|0||0
# 4|	rbMd5Sum		|TEXT|1||0
#
# sqlite3 redi.db ".echo OFF"
# sqlite3 redi.db ".mode column"
# sqlite3 redi.db ".echo OFF"
# sqlite3 redi.db ".mode line"

list:
	sqlite3 redi.db "SELECT * FROM RediBatch"

last:
	sqlite3 redi.db "SELECT * FROM RediBatch ORDER BY rbID DESC LIMIT 1"

add:
	sqlite3 redi.db "INSERT INTO RediBatch (rbStartTime, rbStatus, rbMd5Sum) VALUES ( datetime('now'), 'Started', 'xyz');"

fresh:
	rm -f redi.db
	touch redi.db
	sqlite3 redi.db 'CREATE TABLE RediBatch ( rbID INTEGER PRIMARY KEY AUTOINCREMENT, rbStartTime TEXT NOT NULL, rbEndTime TEXT, rbStatus TEXT, rbMd5Sum TEXT NOT NULL);'
	@test -s redi.db || echo 'File redi.db was not created'

clean:
	sqlite3 redi.db "DELETE FROM RediBatch"
