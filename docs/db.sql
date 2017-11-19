CREATE DATABASE IF NOT EXISTS `qianmu`;
USE `qianmu`;


CREATE TABLE IF NOT EXISTS `universities` (
	`id` BIGINT UNSIGNED AUTO_INCREMENT COMMENT '主键',
	`name` VARCHAR(256) NOT NULL COMMENT '学校名称',
	`rank` INT(8) NOT NULL DEFAULT 0 COMMENT '学校排名',
	`country` VARCHAR(128) COMMENT '国家',
	`state` VARCHAR(128) COMMENT '州省',
	`city` VARCHAR(128) COMMENT '城市',
	`undergraduate_num` VARCHAR(128) COMMENT '本科生人数',
	`postgraduate_num` VARCHAR(128) COMMENT '研究生人数',
	`website` text COMMENT '网站地址',
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '大学信息表';