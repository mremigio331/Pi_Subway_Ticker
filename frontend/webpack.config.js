const path = require('path');
const HtmlWebPackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: './src/index.js', // Corrected entry point path
    output: {
        path: path.resolve(__dirname, 'dist'),
        publicPath: '/', // Added publicPath
        filename: 'bundle.js', // Added output filename
    },
    devServer: {
        historyApiFallback: true, // Added historyApiFallback
        static: {
            directory: path.join(__dirname, 'public'),
        },
        allowedHosts: 'all', // Updated allowedHosts value
        compress: true,
        port: 8080,
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/, // Updated file extension pattern
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react'],
                    },
                },
            },
            {
                test: /\.css$/,
                include: [path.resolve(__dirname, 'src'), /@cloudscape-design/], // Updated include pattern
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {},
                    },
                ],
            },
            {
                test: /\.kml$/, // Added loader configuration for KML files
                use: 'raw-loader',
            },
        ],
    },
    plugins: [
        new HtmlWebPackPlugin({
            template: './src/index.html',
        }),
    ],
};
