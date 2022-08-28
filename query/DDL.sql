CREATE TABLE contents 
(
  contents_key int not null identity(1, 1) encode delta sortkey,
  path varchar(256) not null,
  primary key (contents_key),
  unique (path)
  )
  diststyle key distkey (contents_key);

CREATE TABLE time
(
    time_key timestamp not null encode delta sortkey,
    date date encode delta,
    day	int,
	weekday	int,
	month	int,
	year	int,
	hour	int,
	minute	int,
	second	int,
    primary key (time_key))
    diststyle key distkey (time_key);

CREATE TABLE client
(
    client_key int not null identity(1, 1) encode delta sortkey,
    host varchar(255) not null,
    primary key (client_key),
    unique (host)
    )
    diststyle key distkey (client_key);

CREATE TABLE os
(
    os_key int not null identity(1, 1) encode delta sortkey,
    name varchar(255) not null encode bytedict,
    primary key (os_key),
    unique(name))
    diststyle key distkey (os_key);

CREATE TABLE browser
(
    browser_key int not null identity(1, 1) encode delta sortkey,
    name varchar(255) not null encode bytedict,
    primary key (browser_key),
    unique(name))
    diststyle key distkey (browser_key);

CREATE TABLE visit
(
    time_key timestamp not null encode delta references time(time_key),
    contents_key int not null encode delta references contents(contents_key),
    client_key int not null encode delta references client(client_key),
    os_key int not null encode delta references os(os_key),
    browser_key int not null encode delta references browser(browser_key),
    method varchar(30) encode bytedict,
    status int encode bytedict,
    size int encode mostly8,
    primary key (time_key, contents_key, client_key, os_key, browser_key))
    diststyle key distkey (time_key)
    compound sortkey (time_key, contents_key, client_key, os_key, browser_key);
