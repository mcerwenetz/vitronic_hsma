CREATE TABLE paket(
	id SERIAL,
	lenght INT,
	height INT,
	lastGate INT,
	lastSeenAt TIMESTAMP,
	expectedNext TIMESTAMP,
	status INT,
	PRIMARY KEY (id)
);
