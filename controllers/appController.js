module.exports = {
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