CREATE TABLE Reviewable (
	id      	SERIAL,
	PRIMARY KEY (id)
);

CREATE TABLE Movies (
	id      	INTEGER,
	name    	VARCHAR(100) NOT NULL,
	year    	INTEGER NOT NULL CHECK (year > 1800),
	genre   	VARCHAR(50) NOT NULL,
	runtime 	INTEGER CHECK (runtime > 0),
	overview	TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES Reviewable
    	ON DELETE CASCADE
    	ON UPDATE CASCADE
);

CREATE TABLE Talent (
	tid     	SERIAL,
	name    	VARCHAR(100) NOT NULL,
	PRIMARY KEY (tid)
);

CREATE TABLE Stars_In (
	movieID 	INTEGER,
	tid     	INTEGER,
	role    	VARCHAR(100) NOT NULL,
	PRIMARY KEY (movieID, tid),
	FOREIGN KEY (movieID) REFERENCES Movies,
	FOREIGN KEY (tid) REFERENCES Talent
);

CREATE TABLE Theaters (
	id      	INTEGER,
	name    	VARCHAR(50) NOT NULL,
	address 	VARCHAR(141) NOT NULL,
	seat_info   	INTEGER NOT NULL CHECK (seat_info >= 0),
	contact 	VARCHAR(20),
	zip     	INTEGER CHECK (zip > 0),
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES Reviewable
    	ON DELETE CASCADE
    	ON UPDATE CASCADE
);

CREATE TABLE TimeSlots (
	datetime    TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (datetime)
);

CREATE TABLE Showing (
	movieID    INTEGER,
	theaterID  INTEGER,
	datetime   TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (movieID, theaterID, datetime),
	FOREIGN KEY (movieID) REFERENCES Movies,
	FOREIGN KEY (theaterID) REFERENCES Theaters,
	FOREIGN KEY (datetime) REFERENCES TimeSlots
);

CREATE TABLE Users (
        uid             SERIAL,
        username        VARCHAR(50) NOT NULL,
        password        VARCHAR(50) NOT NULL,
        email           VARCHAR(50) NOT NULL,
        PRIMARY KEY (uid),
        UNIQUE          username,
				UNIQUE					email
);

CREATE TABLE Book (
	movieID 	INTEGER,
	theaterID 	INTEGER,
	datetime  	TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	uid     	INTEGER,
	num_seats	INTEGER NOT NULL CHECK (num_seats > 0),
	price   	REAL NOT NULL CHECK (price >=  0),
	PRIMARY KEY (uid, movieID, theaterID, datetime),
	FOREIGN KEY (uid) REFERENCES Users
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (movieID, theaterID, datetime) REFERENCES Showing
);

CREATE TABLE Review (
    	rid	   	INTEGER,
    	uid 	   	INTEGER,
	rating 	   	INTEGER CHECK (rating >= 1 AND rating <= 10),
	text	   	TEXT,
	review_date	TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	PRIMARY KEY (rid, uid),
	FOREIGN KEY (uid) REFERENCES Users
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
	FOREIGN KEY (rid) REFERENCES Reviewable
    	ON DELETE CASCADE
    	ON UPDATE CASCADE
);

CREATE TABLE CreateCollections (
	name    	VARCHAR(100),
	uid     	INTEGER,
	PRIMARY KEY (uid, name),
	FOREIGN KEY (uid) REFERENCES Users
    	ON DELETE CASCADE
    	ON UPDATE CASCADE
);

CREATE TABLE Contain (
	movieID 	INTEGER,
	uid     	INTEGER,
	name    	VARCHAR(100),
	PRIMARY KEY (movieID, uid, name),
	FOREIGN KEY (movieID) REFERENCES Movies
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
	FOREIGN KEY (uid, name) REFERENCES CreateCollections
    	ON DELETE CASCADE
    	ON UPDATE CASCADE
);
