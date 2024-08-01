-- Drop dependent tables first
DROP TABLE IF EXISTS NexusMuscleLink;
DROP TABLE IF EXISTS TracksMetrics;
DROP TABLE IF EXISTS Muscles;
DROP TABLE IF EXISTS FunctionalFascialLines;

-- Now drop the referenced tables
DROP TABLE IF EXISTS NexusNetwork;
DROP TABLE IF EXISTS Methods;
DROP TABLE IF EXISTS Stations;

/* Creating Tables */
CREATE TABLE NexusNetwork (
    NexusID SERIAL PRIMARY KEY,
    NexusName VARCHAR NOT NULL,
    Description VARCHAR
);

CREATE TABLE FunctionalFascialLines (
    LineID SERIAL PRIMARY KEY,
    NexusID INT,
    LineName VARCHAR NOT NULL,
    FunctionDescription VARCHAR,
    FOREIGN KEY (NexusID) REFERENCES NexusNetwork(NexusID)
);

CREATE TABLE Stations (
    StationID SERIAL PRIMARY KEY,
    StationName VARCHAR NOT NULL
);

CREATE TABLE Muscles (
    MuscleID SERIAL PRIMARY KEY,
    MuscleName VARCHAR NOT NULL,
    Description VARCHAR,
    UpperStationID INT,
    LowerStationID INT
);

CREATE TABLE NexusMuscleLink (
    NexusID INT,
    MuscleID INT,
    Type VARCHAR(12) NOT NULL CHECK (Type IN ('Compression', 'Activation')),
    OppositeSide BOOLEAN NOT NULL CHECK (OppositeSide IN (FALSE, TRUE))
);

CREATE TABLE TracksMetrics (
    MetricID SERIAL PRIMARY KEY,
    LineID INT,
    Alpha FLOAT,
    Lambda FLOAT,
    Side VARCHAR(255),
    FOREIGN KEY (LineID) REFERENCES FunctionalFascialLines(LineID)
);

CREATE TABLE Methods (
    MethodID SERIAL PRIMARY KEY,
    MethodName VARCHAR(255) NOT NULL,
    Description VARCHAR,
    MethodType VARCHAR(50) NOT NULL CHECK (MethodType IN ('Training & Activating', 'Relaxing & Releasing')),
    TargetMuscleType VARCHAR(255) NOT NULL,
    SuitableForHome BOOLEAN NOT NULL DEFAULT TRUE -- TRUE means suitable for home, FALSE otherwise
);
