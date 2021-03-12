/* 日付 */
exports.getDateString = (time = null) => {
  if (time == null || time == undefined) {
    time = new Date();
  }
  let tstr = `${time.getFullYear()}-${(time.getMonth()+1).toString().padStart(2, '0')}-${time.getDate().toString().padStart(2, '0')}`;
  return tstr;
}

/* 時間 */
exports.getTimeString = (time = null) => {
  if (time == null || time == undefined) {
    time = new Date();
  }
  let tstr = `${time.getHours().toString().padStart(2, '0')}-${time.getMinutes().toString().padStart(2, '0')}-${time.getSeconds().toString().padStart(2, '0')}`;
  return tstr;
}
