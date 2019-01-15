-- 銀行預金集計ビュー
CREATE ALGORITHM=UNDEFINED DEFINER=`user`@`%` SQL SECURITY DEFINER 
VIEW `vw_balance` AS
  select `BANKS`.`DAY` AS `day`,
         sum(`BANKS`.`BALANCE`) AS `balance` 
  from `BANKS` 
  group by `BANKS`.`DAY`;

