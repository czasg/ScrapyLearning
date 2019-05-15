CREATE table housePrice (
    `id` varchar(50) not null,
    `house_price` real not null,
    `house_place` varchar(100) not null,
    `house_name` varchar(50) not null,
    `house_area` varchar(50) not null,
    `house_floor` varchar(50) not null,
    `house_scale` varchar(50) not null,
    `distance_from_subway` varchar(50),
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;