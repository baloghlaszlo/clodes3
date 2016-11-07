var webpack = require('webpack');
var path = require('path');

module.exports = {
    entry: [
        './js/app.js'
    ],
    output: {
        path: path.resolve('./static/webpack'),
        filename: 'bundle.js'
    },
    resolve: {
        root:  path.resolve('./js'),
        extensions: ['', '.js']
    },
    module: {
        loaders: [
            {
                test: /\.js$/i,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    "presets": ["es2015", "react", "stage-1"]
                }
            }
        ]
    },
    plugins: [
    ]
};