CREATE TABLE `YJFX_Settle` (
  `id` decimal(16,0) NOT NULL,
  `CurrencyPair` char(7) NOT NULL,
  `Sell` char(1) NOT NULL DEFAULT '0',
  `price1` decimal(11,2) NOT NULL,
  `Date1` datetime NOT NULL,
  `price2` decimal(11,2) NOT NULL,
  `Date2` datetime NOT NULL,
  `Benefit` decimal(10,0) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

