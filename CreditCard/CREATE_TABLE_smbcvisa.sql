CREATE TABLE `smbcvisa` (
  `date` char(10) NOT NULL,
  `payment` decimal(10,0) NOT NULL,
  `info` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
