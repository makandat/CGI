CREATE TABLE `BINDATA` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `original` varchar(400) DEFAULT NULL,
  `datatype` char(10) DEFAULT NULL,
  `data` blob,
  `info` varchar(100) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `original` (`original`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

