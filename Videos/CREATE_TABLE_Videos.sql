CREATE TABLE `Videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(400) NOT NULL,
  `path` varchar(400) NOT NULL,
  `media` varchar(200) DEFAULT NULL,
  `series` varchar(50) DEFAULT NULL,
  `mark` varchar(16) DEFAULT NULL,
  `info` varchar(400) DEFAULT NULL,
  `fav` char(1) DEFAULT '0',
  `count` int(8) DEFAULT '0',
  `thumb` blob,
  PRIMARY KEY (`id`),
  UNIQUE KEY `path` (`path`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

