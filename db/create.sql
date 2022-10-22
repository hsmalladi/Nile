-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    address VARCHAR(255), 
    balance DECIMAL(12,2) DEFAULT 0
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    image BYTEA,
    category VARCHAR(510) NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    description VARCHAR(2000)
);

CREATE TABLE Sellers (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY REFERENCES Users(id)
);

CREATE TABLE Inventory (
    sid INT NOT NULL REFERENCES Sellers(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    PRIMARY KEY(sid, pid)
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Cart (
    quantity INT NOT NULL,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    sid INT NOT NULL REFERENCES Sellers(id),
    PRIMARY KEY(uid, pid, sid)
);

CREATE TABLE RatesSeller (
    sid INT NOT NULL REFERENCES Sellers(id),
    uid INT NOT NULL REFERENCES Users(id),
    dates timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating INT NOT NULL,
    review VARCHAR(2000),
    PRIMARY KEY(sid, uid, dates)
);

CREATE TABLE RatesProduct (
    pid INT NOT NULL REFERENCES Products(id),
    uid INT NOT NULL REFERENCES Users(id),
    dates timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    rating INT NOT NULL,
    review VARCHAR(2000),
    PRIMARY KEY(pid, uid, dates)
);

CREATE TABLE Orders (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    sid INT NOT NULL REFERENCES Sellers(id),
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    quantity INT NOT NULL,
    date_ordered timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    fulfilled BOOL NOT NULL,
    unit_price_at_time_of_payment DECIMAL(12,2) NOT NULL
);
