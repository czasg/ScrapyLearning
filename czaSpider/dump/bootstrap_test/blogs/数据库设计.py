__file__ = 'sql'

"""
create table users1 (
    `id` bigint not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(100) not null,
    `created_at` real not null,
    `unread_msg` bigint not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs1 (
    `id` bigint not null,
    `user_id` bigint not null,
    `blog_image` varchar(100) not null,
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
    `user_image` varchar(100) not null,
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
    `user_image` varchar(100) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;
"""
