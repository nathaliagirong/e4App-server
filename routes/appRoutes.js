const appController = require('../controllers/appController');

module.exports = app => {
    /* ROUTES */
    /* Get Result */
    app.get('/getResult', appController.getResults);
};