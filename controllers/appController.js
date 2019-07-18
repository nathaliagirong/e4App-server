module.exports = {
    
    uploadFile: async (req, res) => {
        try {
            const { nameFile } = req.body;
            if (Object.keys(req.files).length == 0) {
                return res.status(400).send({
                    code: 400,
                    description: 'No files were uploaded.',
                    response: null
                });
            }
            let e4File = req.files.e4File;
            e4File.mv(`../e4App-server/e4-records/${nameFile}`, function (err) {
                const path = `../opnym-backend/image-records/${nameFile}`;
                if (err)
                    return res.status(500).send(err);

                res.status(200).send({
                    code: 200,
                    description: 'success',
                    response: path
                });
            });
        } catch (error) {
            console.log('uploat request error', error); // the uploaded file object
            res.status(500).send({
                code: 500,
                description: 'Server error',
                message: error
            });
        }
    },
    /* GET RESULT */
    getResults: async (req, res) => {
        try {
            console.log('getResults request');
            res.send({
                code: 200,
                description: 'success',
                response: true
            });
        } catch (error) {
            res.status(500).send({
                code: 500,
                description: 'serverError',
                message: error
            });
        }
    },

}