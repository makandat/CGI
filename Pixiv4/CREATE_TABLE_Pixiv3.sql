CREATE TABLE `pixiv3` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(128) NOT NULL,
  `Creator` varchar(40) NOT NULL,
  `Illust_id` bigint(20) NOT NULL,
  `Original` varchar(100) DEFAULT '',
  `Tags` varchar(128) DEFAULT '',
  `BINDATA` int(11) DEFAULT '0',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Illust_id` (`Illust_id`),
  KEY `idxTitle` (`Title`),
  KEY `idxIllusy_id` (`Illust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=235 DEFAULT CHARSET=utf8;
