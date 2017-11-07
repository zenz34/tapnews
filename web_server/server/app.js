var bodyParser = require('body-parser');
var config = require('./config/config.json')
var cors = require('cors');
var express = require('express');
var passport = require('passport');
var path = require('path');
var index = require('./routes/index');
var news = require('./routes/news');
var auth = require('./routes/auth');

var app = express();

require('./models/main.js').connect(config.mongoDbUri);
// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));

// TODO: remove thsi after development is done.
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

app.use(cors());
app.use(bodyParser.json());

app.use('/', index);
app.use('/auth', auth);
const authCheckMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleware);
app.use('/news', news)

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  res.send('404 not found');
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

module.exports = app;
