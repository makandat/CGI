/* Common.js */
'use strict';
const os = require('os');

/* コマンドライン引数を得る。*/
exports.getArg = (n) => {
  let count = process.argv.length;
  if (count < 2) {
    return '';
  }

  let args = [];
  for (let i = count - 1; i > 0; i--) {
    if (process.argv[i].endsWith('.js')) {
      break;
    }
    else {
      args.push(process.argv[i]);
    }
  }

  let a = args.reverse();
  if (n < 0 && n >= a.length) {
    return null;
  }
  return a[n];
}


/* コマンドライン引数の数を得る。*/
exports.getArgsCount = () => {
  let count = process.argv.length;
  for (let i = count - 1; i > 0; i--) {
    if (process.argv[i].endsWith('.js')) {
      count = count - i - 1;
    }
  }

  return count;
}

/* OS が Windows なら true */
exports.isWindows = () => {
  return (os.platform() == 'win32');
}

/* プログラムの終了 */
exports.quit = (code = 0) => {
  process.exit(code);
}

