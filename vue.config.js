// const version = '0.0.1';

// must be the same as WEBPACK_DEVSERVER_HEADER
const DEVSERVER_HEADER = 'X-WEBPACK-DEVSERVER';

module.exports = {
  outputDir: './build/',
  publicPath: 'http://local.next.openbroadcast.ch:3000/static/',
  chainWebpack: (config) => {
    config.module
      .rule('images')
      .use('url-loader')
      .tap((options) => ({ ...options, name: '[name].[ext]' }));
  },
  css: {
    extract: {
      filename: '[name].css',
      chunkFilename: '[name].css',
    },
  },
  configureWebpack: {
    output: {
      filename: '[name].js',
      chunkFilename: '[name].js',
      // publicPath: 'http://local.next.openbroadcast.ch:3000/static/',
    },
    performance: {
      maxEntrypointSize: 512000,
      maxAssetSize: 512000,
    },
  },
  devServer: {
    hot: true,
    inline: true,
    host: '0.0.0.0',
    port: 3000,
    // public: 'MBP15.local:3000',
    // public: 'local.next.openbroadcast.ch:3000',
    disableHostCheck: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {
      '/': {
        target: 'http://local.next.openbroadcast.ch:8080',
        onProxyReq: (proxyReq) => {
          // add header to let django know about getting a devserver request
          proxyReq.setHeader(DEVSERVER_HEADER, 'on');
        },
      },
    },
    // proxy: {
    //   '^/api': {
    //     target: 'http://local.next.openbroadcast.ch:8080',
    //     changeOrigin: true,
    //     logLevel: 'debug',
    //     // pathRewrite: { "^/api": "/" }
    //   },
    // },
  },
};
