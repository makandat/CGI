/* app.js  by express-generator */
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var fs = require('fs');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var multer = require('multer');
var session = require('express-session');
var favicon = require('serve-favicon');
var logger = require('morgan');

/* ルータ定義 */
var indexRouter = require('./routes/index');
var modify_albumRouter = require('./routes/modify_album');
var modify_pictureRouter = require('./routes/modify_picture');
var modify_folderRouter = require('./routes/modify_folder');
var picturesRouter = require('./routes/pictures');
var showfolderRouter = require('./routes/showfolder');
var pictalbumRouter = require('./routes/pictalbum');
var bindataRouter = require('./routes/bindata');
var creatorsRouter = require('./routes/creators');
var toolsRouter = require('./routes/tools');
var usersRouter = require('./routes/users');
var videoRouter = require('./routes/video');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
//app.use(multer);
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({
  secret: 'makandat',
  resave: false,
  saveUninitialized: false,
  cookie:{
    httpOnly: true,
    secure: false,
    maxage: 1000 * 60 * 30
  }
}));

app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));

// ルート設定
app.use('/', indexRouter);
app.use('/modify_album', modify_albumRouter);
app.use('/modify_picture', modify_pictureRouter);
app.use('/modify_folder', modify_folderRouter);
app.use('/pictures', picturesRouter);
app.use('/showfolder', showfolderRouter);
app.use('/pictalbum', pictalbumRouter);
app.use('/bindata', bindataRouter);
app.use('/creators', creatorsRouter);
app.use('/tools', toolsRouter);
app.use('/users', usersRouter);
app.use('/video', videoRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});


// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

/* package.json からバージョン番号を得る。*/
function getVersion() {
  let pstr = fs.readFileSync("package.json", "utf-8");
  let p = JSON.parse(pstr);
  return p.version;
}

console.info('画像アルバム for Express4 version ' + getVersion());
console.info('URL: http://127.0.0.1:3000');

/* モジュールエクスポート */
module.exports = app;
