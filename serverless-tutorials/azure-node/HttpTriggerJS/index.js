var pd = require('pandas-js');

module.exports = function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    const df = new pd.DataFrame([{x: 1, y: 2}, {x: 2, y: 3}, {x: 3, y: 4}]);
    const dsString = df.toString();


    if (req.query.name || (req.body && req.body.name)) {
        context.res = {
            // status: 200, /* Defaults to 200 */
            body: "Hello " + dsString//(req.query.name || req.body.name)
        };
    }
    else {
        context.res = {
            status: 400,
            body: "Please pass a name on the query string or in the request body" 
        };
    }
    context.done();
};