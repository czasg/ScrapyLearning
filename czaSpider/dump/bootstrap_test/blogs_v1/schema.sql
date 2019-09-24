-- schema.sql

drop database if exists awesome;

create database awesome;

use awesome;

grant select, insert, update, delete on awesome.* to 'www-data'@'localhost' identified by 'www-data';

create table users1 (
    `id` bigint not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(50) not null,
    `created_at` real not null,
    `unread_msg` bigint not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs1 (
    `id` bigint not null,
    `user_id` bigint not null,
    `user_name` varchar(50) not null,
    `blog_image` varchar(50) not null,
    `title` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    `count` bigint not null,
    `update_at` real not null,
    `blog_type` varchar(50) not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments1 (
    `id` bigint not null,
    `blog_id` bigint not null,
    `user_id` bigint not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(50) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table son_comments1 (
    `id` bigint not null,
    `comment_id` bigint not null,
    `blog_id` bigint not null,
    `user_id` bigint not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(50) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;




-- 添加统计模块字段
alter table blogs add count bigint not null default 0;
alter table blogs1 add user_name varchar(50) not null;
alter table blogs1 add blog_image varchar(50) not null;
-- blog 类型：0表示未分类
-- 1-前端 2-后端 3-爬虫 4-生活
alter table blogs add blog_type bigint not null default 0;