const webpack = require('webpack');
const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const DEFAULT_HOST = 'localhost';
const DEFAULT_PORT = 9000;
const port = process.env.PORT || DEFAULT_PORT;

// DO NOT USE DEVTOOLS THAT RELY ON EVAL IN PRODUCTION
// These include tools such as 'cheap-module-eval-source-map'
module.exports = (_, { mode }) => {
  return {
    devtool: mode === 'production' ? false : 'eval-cheap-module-source-map',
    target: 'web',
    context: __dirname,
    stats: {
      children: false,
      entrypoints: false,
      modules: false,
    },
    output: {
      path: `${__dirname}/build`,
      clean: true,
      publicPath: '/',
      filename: 'assets/[name].[contenthash:8].js',
      globalObject: 'this',
    },
    resolve: {
      alias: {
        'react-native': 'react-native-web',
      },
      extensions: [
        '.web.jsx',
        '.web.js',
        '.wasm',
        '.mjs',
        '.jsx',
        '.js',
        '.json',
      ],
      fallback: {
        Buffer: false,
        fs: false,
        tls: false,
      },
    },
    devServer: {
      host: process.env.HOST || DEFAULT_HOST,
      port,
      server: 'https',
      historyApiFallback: {
        disableDotRule: true,
      },
      client: {
        overlay: false,
      },
      headers: {
        'Content-Security-Policy':
          "default-src 'none'; script-src 'self' 'unsafe-eval'; img-src 'self' https://*.gravatar.com https://*.githubusercontent.com https://i1.wp.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; connect-src https://localhost:8010 'self' https://balrog-localdev.auth0.com https://www.googleapis.com/; frame-src https://balrog-localdev.auth0.com; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
        'X-Frame-Options': 'SAMEORIGIN',
        'X-Content-Type-Options': 'nosniff',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'no-referrer',
        'Strict-Transport-Security':
          'max-age=31536000; includeSubDomains; always;',
      },
    },
    module: {
      rules: [
        {
          test: /\.m?js/,
          resolve: {
            fullySpecified: false,
          },
        },
        {
          test: /\.(js|jsx)$/,
          include: [`${__dirname}/src`, `${__dirname}/test`],
          use: [
            {
              loader: 'babel-loader',
              options: {
                cacheDirectory: true,
                babelrc: false,
                configFile: false,
                presets: [
                  [
                    '@babel/preset-env',
                    {
                      debug: false,
                      useBuiltIns: false,
                      shippedProposals: true,
                      targets: {
                        browsers: [
                          'last 2 Chrome versions',
                          'last 2 Firefox versions',
                          'last 2 Edge versions',
                          'last 2 Opera versions',
                          'last 2 Safari versions',
                          'last 2 iOS versions',
                        ],
                      },
                    },
                  ],
                  [
                    '@babel/preset-react',
                    {
                      development: mode === 'development',
                      useSpread: true,
                    },
                  ],
                ],
                plugins: [
                  ...(mode === 'development' ? ['react-refresh/babel'] : []),
                ],
              },
            },
          ],
        },
        {
          oneOf: [
            {
              test: /\.module\.css$/,
              use: [
                {
                  loader: MiniCssExtractPlugin.loader,
                  options: {
                    esModule: true,
                  },
                },
                {
                  loader: 'css-loader',
                  options: {
                    importLoaders: 0,
                    modules: true,
                  },
                },
              ],
            },
            {
              test: /\.css$/,
              use: [
                {
                  loader: MiniCssExtractPlugin.loader,
                  options: {
                    esModule: true,
                  },
                },
                {
                  loader: 'css-loader',
                  options: {
                    importLoaders: 0,
                  },
                },
              ],
            },
          ],
        },
        {
          test: /\.(eot|ttf|woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
          type: 'asset/resource',
        },
        {
          test: /\.(ico|png|jpg|jpeg|gif|svg|webp)(\?v=\d+\.\d+\.\d+)?$/,
          type: 'asset/resource',
        },
      ],
    },
    optimization: {
      minimize: true,
      splitChunks: {
        chunks: 'all',
        maxInitialRequests: 5,
        name: false,
      },
      runtimeChunk: 'single',
    },
    plugins: [
      new webpack.EnvironmentPlugin({
        HOST: DEFAULT_HOST,
        PORT: DEFAULT_PORT,
        BALROG_ROOT_URL: 'https://localhost:8010',
        AUTH0_CLIENT_ID: 'GlZhJQfx52b7MLQ19AjuTJHieiB4oh1j',
        AUTH0_DOMAIN: 'balrog-localdev.auth0.com',
        AUTH0_AUDIENCE: 'balrog-localdev',
        AUTH0_SCOPE: 'full-user-credentials openid profile email',
        AUTH0_REDIRECT_URI: 'https://localhost:9000/login',
        GCS_NIGHTLY_HISTORY_BUCKET:
          'https://www.googleapis.com/storage/v1/b/balrog-prod-nightly-history-v1/o',
        GCS_RELEASES_HISTORY_BUCKET:
          'https://www.googleapis.com/storage/v1/b/balrog-prod-release-history-v1/o',
      }),
      new HtmlWebpackPlugin({
        template: `${__dirname}/src/index.html`,
        templateContent: false,
        filename: 'index.html',
        publicPath: 'auto',
        hash: false,
        inject: 'body',
        scriptLoading: 'blocking',
        compile: true,
        favicon: `${__dirname}/src/images/favicon.png`,
        minify: 'auto',
        cache: true,
        showErrors: true,
        chunks: ['index'],
        excludeChunks: [],
        chunksSortMode: 'auto',
        meta: {
          viewport: 'width=device-width, initial-scale=1',
        },
        base: false,
        title: 'Balrog Admin',
        xhtml: false,
        appMountId: 'root',
        lang: 'en',
      }),
      new MiniCssExtractPlugin({
        filename: 'assets/[name].[contenthash:8].css',
        ignoreOrder: false,
        chunkFilename: 'assets/[name].[contenthash:8].css',
      }),
      ...(mode === 'development'
        ? [new ReactRefreshWebpackPlugin({ overlay: false })]
        : []),
    ],
    entry: {
      index: [`${__dirname}/src/index`],
    },
  };
};
