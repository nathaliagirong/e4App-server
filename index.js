const express = require('express');
const bodyParser = require("body-parser");
const fileUpload = require('express-fileupload');
const app = express();


/* MIDDLE | bodyParser for parse to JSON format */
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(fileUpload());

app.listen(5000, () => {
    console.log("MongoDB and server connected");
});


/* IMPORT ROUTER MODULES */
app.get("/getResult", (req, res) => {
    res.send({
        respuesta: true,
        description: 'Usted está fibrilando'
    });
})