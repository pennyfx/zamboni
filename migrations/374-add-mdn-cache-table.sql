BEGIN;
CREATE TABLE `mdn_cache` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL UNIQUE,
    `title` varchar(255) NOT NULL,
    `toc` longtext NOT NULL,
    `content` longtext NOT NULL,
    `permalink` varchar(255) NOT NULL,
    `modifed` datetime NOT NULL
)
;
COMMIT;