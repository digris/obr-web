// const version = '0.0.1';

// must be the same as WEBPACK_DEVSERVER_HEADER
const DEVSERVER_HEADER = 'X-WEBPACK-DEVSERVER';

module.exports = {
  outputDir: './build/',
  publicPath: process.env.NODE_ENV === 'production'
    ? '/'
    : 'http://local.obr-next:3000/static/',
  chainWebpack: (config) => {
    config.module
      .rule('images')
      .use('url-loader')
      .tap((options) => ({ ...options, name: '[name].[ext]' }));
  },
  css: {
    // loaderOptions: {
    //   postcss: {
    //     plugins: {
    //       autoprefixer: {},
    //     },
    //   },
    // },
    extract: {
      filename: '[name].css',
      chunkFilename: '[name].css',
    },
  },
  configureWebpack: {
    output: {
      filename: '[name].js',
      chunkFilename: '[name].js',
    },
    performance: {
      maxEntrypointSize: 1500000,
      maxAssetSize: 1500000,
    },
  },
  devServer: {
    hot: true,
    inline: true,
    host: '0.0.0.0',
    port: 3000,
    public: 'local.obr-next:3000',
    disableHostCheck: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {
      '/': {
        target: 'http://local.obr-next:8080',
        onProxyReq: (proxyReq) => {
          // add header to let django know about getting a devserver request
          proxyReq.setHeader(DEVSERVER_HEADER, 'on');
        },
      },
    },
  },
};
