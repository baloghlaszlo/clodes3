var path = require('path');
var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8889',
                secure: false
            }
        },
        historyApiFallback: true
    },
    //devtool: "#source-map",
    devtool: "eval",
    entry: [
        'webpack-dev-server/client?http://localhost:8888',
        'webpack/hot/only-dev-server',
        './js/app.js'
    ],
    output: {
        path: path.resolve(__dirname, "build"),
        filename: "bundle.js",
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new HtmlWebpackPlugin({
            template: 'templates/webpack-index.html'
        })
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
