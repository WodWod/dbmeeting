/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 80015
Source Host           : localhost:3306
Source Database       : dbmeeting

Target Server Type    : MYSQL
Target Server Version : 80015
File Encoding         : 65001

Date: 2019-12-18 14:57:09
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for movie_person
-- ----------------------------
DROP TABLE IF EXISTS `movie_person`;
CREATE TABLE `movie_person` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `subject_num` varchar(10) DEFAULT '' ,
  `name` varchar(500) DEFAULT '',
  `person_name` varchar(50) DEFAULT '',
  `rating` int(1) DEFAULT 3 ,
  `person_id` varchar(50) DEFAULT '',
  `img_src`   varchar(100) DEFAULT '',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `book_person`;
CREATE TABLE `book_person` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `subject_num` varchar(10) DEFAULT '' ,
  `name` varchar(500) DEFAULT '',
  `person_name` varchar(50) DEFAULT '',
  `rating` int(1) DEFAULT 3 ,
  `person_id` varchar(50) DEFAULT '',
  `img_src`   varchar(100) DEFAULT '',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `music_person`;
CREATE TABLE `music_person` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `subject_num` varchar(10) DEFAULT '' ,
  `name` varchar(500) DEFAULT '',
  `person_name` varchar(50) DEFAULT '',
  `rating` int(1) DEFAULT 3 ,
  `person_id` varchar(50) DEFAULT '',
  `img_src`   varchar(100) DEFAULT '',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `person`;
CREATE TABLE `person` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `person_id` varchar(50) DEFAULT '',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


-- subject插入数据
-- select count(*) as re,subject_num,name from movie_person group by subject_num,name having re=1;
-- select count(distinct subject_num) from movie_person;
DROP TABLE IF EXISTS `subject`;
CREATE TABLE `subject` (
  `subject_num` varchar(10) DEFAULT '' ,
  `name` varchar(500) DEFAULT '',
  `type` varchar(10) DEFAULT '',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`subject_num`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;

CREATE TEMPORARY TABLE temp (subject_num varchar(10),name varchar(500) ,type varchar(10));
insert IGNORE into temp(subject_num,name)  select subject_num,name  from movie_person group by subject_num,name;
update temp set type='movie';
insert IGNORE into subject(subject_num,name,type)  select subject_num,name,type from temp;
DROP TABLE temp;

CREATE TEMPORARY TABLE temp (subject_num varchar(10),name varchar(500) ,type varchar(10));
insert IGNORE into temp(subject_num,name)  select subject_num,name  from book_person group by subject_num,name;
update temp set type='book';
insert IGNORE into subject(subject_num,name,type)  select subject_num,name,type from temp;
DROP TABLE temp;

CREATE TEMPORARY TABLE temp (subject_num varchar(10),name varchar(500) ,type varchar(10));
insert IGNORE into temp(subject_num,name)  select subject_num,name  from music_person group by subject_num,name;
update temp set type='music';
insert IGNORE into subject(subject_num,name,type)  select subject_num,name,type from temp;
DROP TABLE temp;

-- 模糊匹配subject.name
select subject_num,name from subject where type='movie' and name like '%横道%' ;  subject_num 10484041
select person_id,person_name,rating from movie_person where subject_num='10484041';  rating 5-> +2

-- 代理池
DROP TABLE IF EXISTS `proxy`;
CREATE TABLE `proxy` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(10) DEFAULT '',
  `address` varchar(50) DEFAULT '',
  `status`  int(1),
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

delete from proxy where status=0;

insert into dbtest.movie_person(subject_num,name,person_name,rating,person_id,img_src,timestamp)  select subject_num,name,person_name,rating,person_id,img_src,timestamp from dbmeeting.movie_person;
insert into dbtest.book_person(subject_num,name,person_name,rating,person_id,img_src,timestamp)  select subject_num,name,person_name,rating,person_id,img_src,timestamp from dbmeeting.book_person;
insert into dbtest.music_person(subject_num,name,person_name,rating,person_id,img_src,timestamp)  select subject_num,name,person_name,rating,person_id,img_src,timestamp from dbmeeting.music_person;
insert into dbtest.person(person_id,timestamp)  select person_id,timestamp from dbmeeting.person;

select count(*) as count,person_id from person group by person_id having count>1;

create table temp as select max(id) as id,person_id from person group by person_id having count(person_id)>1;
delete from person where id in (select id from temp);
drop table temp;

select count(*) as count,subject_num,person_id from book_person group by subject_num,person_id having count>1;