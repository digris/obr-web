// const version = '0.0.1';

module.exports = {
  outputDir: './build/',
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
    public: 'next.openbroadcast.ch:3000',
    disableHostCheck: true,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {
      '^/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        logLevel: 'debug',
        // pathRewrite: { "^/api": "/" }
      },
    },
  },
};
