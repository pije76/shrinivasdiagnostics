const path = require('path');

const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = (env, argv) => {
    const devMode = argv.mode === 'development' ? true : false;

    const plugins = [
        new HtmlWebpackPlugin({
            template: './website/index.html',
            filename: './index.html',
            minify: {
                collapseWhitespace: false,
                preserveLineBreaks: true
            }
        }),
        new MiniCssExtractPlugin({
            filename: devMode ? '[name].css' : '[name].[contenthash].css',
            chunkFilename: devMode ? '[id].css' : '[id].[contenthash].css',
        }),
    ];

    const config = [
        {
            mode: devMode ? 'development' : 'production',
            entry: './website/index.js',
            output: {
                filename: devMode ? 'bundle.js' : '[name].[contenthash].bundle.js',
                path: path.resolve(__dirname, './demo')
            },
            devServer: {
                liveReload: true,
                contentBase: [
                    path.resolve(__dirname, './../dist'),
                ],
                publicPath: '/',
                watchContentBase: true,
                compress: true,
                port: 9000,
            },
            module: {
                rules: [
                    {
                        test: /\.html$/,
                        loader: "html-loader",
                        options: {
                            minimize: false
                        }
                    },
                    {
                        test: /\.m?js$/,
                        exclude: /(node_modules|bower_components)/,
                        use: {
                            loader: 'babel-loader',
                            options: {
                                presets: ['@babel/preset-env']
                            }
                        }
                    },
                    {
                        test: /\.scss$/,
                        use: [
                            MiniCssExtractPlugin.loader,
                            "css-loader",
                            {
                                loader: 'postcss-loader',
                                options: {
                                    postcssOptions: {
                                        plugins: function () {
                                            return [
                                                require('autoprefixer')
                                            ];
                                        }
                                    }
                                }
                            },
                            "sass-loader",
                        ]
                    },
                    {
                        test: /\.css$/i,
                        use: [
                            MiniCssExtractPlugin.loader,
                            "extract-loader",
                            "css-loader",
                            'postcs-loader'
                        ]
                    }
                ],
            },
            plugins: plugins,
            optimization: {
                minimize: devMode ? false : true
            }
        }
    ];
    
    return config;
};
