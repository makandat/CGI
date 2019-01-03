CREATE TABLE `Music` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(180) NOT NULL,
  `path` varchar(400) NOT NULL UNIQUE,
  `artist` varchar(50) DEFAULT NULL,
  `album` varchar(50) DEFAULT NULL,
  `mark` varchar(16) DEFAULT NULL,
  `info` varchar(100) DEFAULT NULL,
  `fav` char(1) DEFAULT '0',
  `count` int(8) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

