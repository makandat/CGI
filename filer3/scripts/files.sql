create table info (
  n integer not null primary key autoincrement,
  path text not null,
  info text not null,
  method text,
  icon text,
  dir integer not null default 0,
  bin integer not null default 0,
  `group` text,
  tstamp text
);
