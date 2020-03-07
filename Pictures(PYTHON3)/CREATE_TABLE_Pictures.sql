CREATE TABLE `Pictures` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TITLE` varchar(100) NOT NULL,
  `CREATOR` varchar(100) NOT NULL,
  `PATH` varchar(500) NOT NULL,
  `MARK` varchar(10) DEFAULT NULL,
  `INFO` varchar(100) DEFAULT NULL,
  `fav` int(4) DEFAULT '0',
  `COUNT` int(8) DEFAULT '0',
  `BINDATA` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `idxTitle` (`TITLE`),
  KEY `idxCreator` (`CREATOR`),
  KEY `idxInfo` (`INFO`),
  KEY `idxPath` (`PATH`),
  KEY `idx_info` (`INFO`),
  KEY `idx_mark` (`MARK`)
) ENGINE=InnoDB AUTO_INCREMENT=17342 DEFAULT CHARSET=utf8;
