CREATE TABLE parceldump( -- gate PIs dump their results here
	id SERIAL,
	lenght INT,
	height INT,
	lastGate INT,
	lastSeenAt TIMESTAMP,
	expectedNext TIMESTAMP,
	status INT,
	features integer[][],
	PRIMARY KEY (id)
);

CREATE TABLE parcel( -- DB Pi reads from dumptable and writes to this table
	id SERIAL,
	lenght INT,
	height INT,
	lastGate INT,
	lastSeenAt TIMESTAMP,
	expectedNext TIMESTAMP,
	status INT,
	features integer[][],
	PRIMARY KEY (id)
);
