-- ユーザ管理テーブル
CREATE TABLE `user`.`Users` (
  `id` int not null primary key auto_increment,
  `userid` varchar(16) unique not null,
  `password` varchar(100) not null,
  `priv` char(1) not null default 1,
  `info` varchar(100),
  `registered` char(10),
  `expired` char(1) default 0
) CHARACTER SET UTF8;

INSERT INTO `user`.`Users`(`userid`, `password`, `priv`, `info`, `registered`, `expired`) VALUES('root', 'root', 2, '管理者', '2018-10-08', 0);
INSERT INTO `user`.`Users`(`userid`, `password`, `priv`, `info`, `registered`, `expired`) VALUES('guest', 'guest', 0, 'ゲスト', '2018-10-08', 1);
INSERT INTO `user`.`Users`(`userid`, `password`, `priv`, `info`, `registered`, `expired`) VALUES('user1', 'user1', 1, '一般ユーザ', '2018-10-08', 0);
INSERT INTO `user`.`Users`(`userid`, `password`, `priv`, `info`, `registered`, `expired`) VALUES('user2', 'user2', 1, '一般ユーザ', '2018-10-08', 0);
