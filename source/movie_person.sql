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
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `book_person`;
CREATE TABLE `book_person` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `subject_num` varchar(10) DEFAULT '' ,
  `name` varchar(500) DEFAULT '',
  `person_name` varchar(50) DEFAULT '',
  `rating` int(1) DEFAULT 3 ,
  `person_id` varchar(50) DEFAULT '',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `music_person`;
CREATE TABLE `music_person` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `subject_num` varchar(10) DEFAULT '' ,
  `name` varchar(500) DEFAULT '',
  `person_name` varchar(50) DEFAULT '',
  `rating` int(1) DEFAULT 3 ,
  `person_id` varchar(50) DEFAULT '',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `person`;
CREATE TABLE `person` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `person_id` varchar(50) DEFAULT '',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;