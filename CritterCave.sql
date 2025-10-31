-- Nina Howley
-- create the person, address and phone tables in nh107_db
-- load data from the provided and edited csvs into the tables

-- fixed: added ENGINE = InnoDB; for referential integrity

use crittercave_db;

-- drop tables before creating
-- drop in reverse order because of pid deletion restrictions
drop table if exists liked_story;
drop table if exists liked_critter;
drop table if exists story;
drop table if exists critter;
drop table if exists user;

-- create user table with primary key uid
create table user (
    uid int not null,
    name varchar(50),
    username varchar(50),
    password varchar(50),
    created datetime,
    profilepic varchar(50),
    darkmode boolean,
    primary key (uid)
) ENGINE = InnoDB;

create table critter (
    cid int not null,
    uid int not null,
    imagepath varchar(50),
    name varchar(50),
    description varchar(250),
    created datetime,
    primary key (cid),
    foreign key (uid) references user(uid) 
        on update restrict
        on delete restrict
) ENGINE = InnoDB;

create table story (
    sid int not null,
    cid int not null,
    uid int not null,
    created datetime,
    story varchar(2000),
    primary key (sid),
    foreign key (cid) references critter(cid) 
        on update restrict
        on delete restrict,
    foreign key (uid) references user(uid) 
        on update restrict
        on delete restrict
) ENGINE = InnoDB;

create table liked_critter (
    cid int not null,
    uid int not null,
    foreign key (cid) references critter(cid) 
        on update restrict
        on delete restrict,
    foreign key (uid) references user(uid) 
        on update restrict
        on delete restrict
) ENGINE = InnoDB;

create table liked_story (
    sid int not null,
    uid int not null,
    foreign key (sid) references story(sid) 
        on update restrict
        on delete restrict,
    foreign key (uid) references user(uid) 
        on update restrict
        on delete restrict
) ENGINE = InnoDB;