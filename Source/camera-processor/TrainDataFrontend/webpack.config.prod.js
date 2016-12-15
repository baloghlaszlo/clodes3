var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: [
        './js/app.js'
    ],
    output: {
        path: path.resolve(__dirname, "../TrainDataBackend/static"),
        filename: "bundle.js",
    },
    plugins: [
        new webpack.optimize.UglifyJsPlugin({minimize: true})
    ],
    module: {
        loaders: [{
            test: /\.jsx?$/,
            exclude: /node_modules/,
            loaders: ['babel-loader']
        }]
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    }
};
