const webpack = require('webpack');

const DEFAULT_HOST = 'localhost';
const DEFAULT_PORT = 9000;
const port = process.env.PORT || DEFAULT_PORT;
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ESLintPlugin = require('eslint-webpack-plugin');
const baseConfig = require('./.eslintrc');

const eslintConfig = {
  cache: true,
  cwd: __dirname,
  emitWarning: true,
  failOnError: false,
  formatter: 'codeframe',
  useEslintrc: false,
  baseConfig,
};

// DO NOT USE DEVTOOLS THAT RELY ON EVAL IN PRODUCTION
// These include tools such as 'cheap-module-eval-source-map' and 'react-hot-loader/babel'
module.exports = env => {
  return {
    mode: env,
    devtool: env === 'production' ? false : 'cheap-module-eval-source-map',
    target: 'web',
    context: __dirname,
    stats: {
      children: false,
      entrypoints: false,
      modules: false,
    },
    node: {
      Buffer: false,
      fs: 'empty',
      tls: 'empty',
    },
    output: {
      path: `${__dirname}/build`,
      publicPath: '/',
      filename: 'assets/[name].js',
      globalObject: 'this',
    },
    resolve: {
      alias: {
        'react-native': 'react-native-web',
        'react-dom': '@hot-loader/react-dom',
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
    },
    devServer: {
      port,
      hot: true,
      historyApiFallback: {
        disableDotRule: true,
      },
      overlay: true,
      stats: {
        all: false,
        errors: true,
        timings: true,
        warnings: true,
      },
      host: process.env.HOST || DEFAULT_HOST,
      https: true,
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
          test: /\.html$/,
          use: [
            {
              loader: 'html-loader',
              options: {
                attrs: ['img:src', 'link:href'],
              },
            },
          ],
        },
        {
          include: [`${__dirname}/src`, `${__dirname}/test`],
          test: /\.(js|jsx)$/,
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
                      development: env === 'development',
                      useSpread: true,
                    },
                  ],
                ],
                plugins: [
                  '@babel/plugin-syntax-dynamic-import',
                  ...(env === 'development' ? ['react-hot-loader/babel'] : []),
                ],
              },
            },
          ],
        },
        {
          oneOf: [
            {
              test: /\.css$/i,
              use: [
                {
                  loader: 'style-loader',
                },
                {
                  loader: 'css-loader',
                  options: {
                    importLoaders: 0,
                    modules: true,
                  },
                },
              ],
              include: /\.module\.css$/,
            },
            {
              test: /\.css$/i,
              use: [
                {
                  loader: 'style-loader',
                },
                {
                  loader: 'css-loader',
                  options: {
                    importLoaders: 0,
                  },
                },
              ],
              exclude: /\.module\.css$/,
            },
          ],
        },
        {
          test: /\.(png|jpe?g|gif|svg)$/i,
          use: [
            {
              loader: 'url-loader',
              options: {
                limit: 8192,
                name: 'assets/[name].[ext]',
                fallback: require.resolve('file-loader'),
              },
            },
          ],
        },
        {
          test: /\.worker\.js$/,
          use: [
            {
              loader: 'worker-loader',
            },
          ],
        },
      ],
    },
    optimization: {
      minimize: false,
      splitChunks: {
        chunks: 'all',
        name: true,
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
        AUTH0_RESPONSE_TYPE: 'token id_token',
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
      new ESLintPlugin({
        extensions: ['js', 'jsx'],
        files: [`${__dirname}/src`, `${__dirname}/test`],
        ...eslintConfig,
      }),
      new webpack.HotModuleReplacementPlugin(),
    ],
    entry: {
      index: [`${__dirname}/src/index`],
    },
  };
};
