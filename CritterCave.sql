-- (CritterCave)
-- Creates all necessary tables for the database

use crittercave_db;

-- drop tables before creating
-- drop in reverse order because of uid, cid and sid deletion restrictions
drop table if exists liked_story;
drop table if exists liked_critter;
drop table if exists story;
drop table if exists critter;
drop table if exists user;

-- create user table with primary key uid
create table user (
    uid int not null auto_increment,
    name varchar(50) not null,
    username varchar(50) not null,
    password char(60) not null,         -- password is a hashed 60 character string
    created datetime not null,
    profilepic varchar(50) not null,
    darkmode boolean not null,
    unique(username),                   -- usernames must be unique
    index(username),                    -- index of user is username (unique)
    primary key (uid)       
) ENGINE = InnoDB;

-- create critter table with primary key cid and foreign key uid
create table critter (
    cid int not null auto_increment,
    uid int not null,
    imagepath varchar(50) not null,
    name varchar(50) not null,
    description varchar(250) not null,
    created datetime not null,
    primary key (cid),
    foreign key (uid) references user(uid) 
        on update restrict
        on delete restrict
) ENGINE = InnoDB;

-- create story table with primary key sid and foreign keys cid and uid
create table story (
    sid int not null auto_increment,
    cid int not null,
    uid int not null,
    created datetime not null,
    story varchar(2000) not null,
    primary key (sid),
    foreign key (cid) references critter(cid) 
        on update restrict
        on delete restrict,
    foreign key (uid) references user(uid) 
        on update restrict
        on delete restrict
) ENGINE = InnoDB;

-- create liked_critter table with foreign keys cid and uid
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

-- create liked_story table with foreign keys sid and uid
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