
CREATE TABLE `mdn_cache` (
    `id` int(11) AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL UNIQUE,
    `title` varchar(255) NOT NULL,
    `toc` longtext NOT NULL,
    `content` longtext NOT NULL,
    `permalink` varchar(255) NOT NULL,
    `modifed` datetime NOT NULL
) ENGINE=InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;
