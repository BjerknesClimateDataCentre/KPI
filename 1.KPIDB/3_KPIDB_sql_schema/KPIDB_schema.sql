BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Calibration" (
	"id"	INTEGER,
	"CP URL Calibration"	TEXT,
	"date"	TEXT,
	"sensor_id"	INTEGER,
	"offset"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("sensor_id") REFERENCES "Sensor"
);
CREATE TABLE IF NOT EXISTS "Sensor" (
	"id"	INTEGER,
	"CP URL Sensor"	TEXT,
	"CP URL Sensor Dep."	TEXT,
	"CP URL Instrument Dep."	TEXT,
	"CP URL Platform Dep."	TEXT,
	"sensorType_id"	INTEGER,
	"station_id"	INTEGER,
	"manufacturer"	TEXT,
	"start"	TEXT,
	"end"	TEXT DEFAULT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("station_id") REFERENCES "Station",
	FOREIGN KEY("sensorType_id") REFERENCES "Sensor type"
);
CREATE TABLE IF NOT EXISTS "Sensor type" (
	"id"	INTEGER,
	"CP URL Variable Type"	TEXT,
	"name"	TEXT,
	"param_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("param_id") REFERENCES "Parameters"
);
CREATE TABLE IF NOT EXISTS "Parameters" (
	"id"	INTEGER,
	"CP URL Value Type"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Station staff" (
	"id"	INTEGER,
	"CP URL Assumed Role"	TEXT,
	"people_id"	INTEGER,
	"station_id"	INTEGER,
	"start"	TEXT,
	"end"	TEXT DEFAULT NULL,
	"role"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("people_id") REFERENCES "People",
	FOREIGN KEY("station_id") REFERENCES "Station"
);
CREATE TABLE IF NOT EXISTS "Station" (
	"id"	INTEGER,
	"CP URL Station"	TEXT,
	"CP URL Platform Dep."	TEXT,
	"name"	TEXT,
	"country"	TEXT,
	"start"	TEXT,
	"end"	TEXT DEFAULT NULL,
	"platform type"	TEXT,
	"previous station id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("previous station id") REFERENCES "Station"
);
CREATE TABLE IF NOT EXISTS "People" (
	"id"	INTEGER,
	"CP URL Person"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id")
);
COMMIT;
