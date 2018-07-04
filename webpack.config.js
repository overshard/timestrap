const path = require('path');

const VueLoaderPlugin = require('vue-loader/lib/plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');


module.exports = {
  mode: 'production',
  entry: './client/static_src/main.js',
  output: {
    path: path.resolve(__dirname, 'client/static/'),
    filename: 'bundle.js',
  },
  watch: false,
  watchOptions: {
    ignored: /node_modules/,
  },
  performance: {
    maxEntrypointSize: 5000000,
    maxAssetSize: 5000000,
  },
  stats: {
    entrypoints: false,
  },
  devtool: 'source-map',
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      'picker': 'pickadate/lib/picker.js',
      'picker-date': 'pickadate/lib/picker.date.js',
    },
  },
  plugins: [
    new VueLoaderPlugin(),
    new MiniCssExtractPlugin({
      filename: 'bundle.css',
    }),
  ],
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.(sc|c)ss$/,
        loaders: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },
      {
        test: /\.(png|jpg|gif|svg|ico)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
          outputPath: 'imgs/',
          publicPath: '/static/imgs/',
        },
      },
    ],
  },
};
