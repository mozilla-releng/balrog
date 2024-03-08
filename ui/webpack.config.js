const webpack = require("webpack");

const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  mode: "development",
  devtool: "cheap-module-eval-source-map",
  target: "web",
  context: "/app",
  stats: {
    children: false,
    entrypoints: false,
    modules: false,
  },
  node: {
    Buffer: false,
    fs: "empty",
    tls: "empty",
  },
  output: {
    path: "/app/build",
    publicPath: "/",
    filename: "assets/[name].js",
    globalObject: "this",
  },
  resolve: {
    alias: {
      "react-native": "react-native-web",
      "react-dom": "@hot-loader/react-dom",
    },
    extensions: [
      ".web.jsx",
      ".web.js",
      ".wasm",
      ".mjs",
      ".jsx",
      ".js",
      ".json",
    ],
  },
  devServer: {
    port: "9000",
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
    host: "0.0.0.0",
    https: true,
    headers: {
      "Content-Security-Policy":
        "default-src 'none'; script-src 'self' 'unsafe-eval'; img-src 'self' https://*.gravatar.com https://*.githubusercontent.com https://i1.wp.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; connect-src https://localhost:8010 'self' https://balrog-localdev.auth0.com https://www.googleapis.com/; frame-src https://balrog-localdev.auth0.com; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
      "X-Frame-Options": "SAMEORIGIN",
      "X-Content-Type-Options": "nosniff",
      "X-XSS-Protection": "1; mode=block",
      "Referrer-Policy": "no-referrer",
      "Strict-Transport-Security":
        "max-age=31536000; includeSubDomains; always;",
    },
  },
  module: {
    rules: [
      {
        enforce: "pre",
        include: ["/app/src", "/app/test"],
        use: [
          {
            loader: "/app/node_modules/eslint-loader/dist/cjs.js",
            options: {
              cache: true,
              cwd: "/app",
              emitWarning: true,
              failOnError: false,
              formatter: "codeframe",
              useEslintrc: false,
              baseConfig: {
                parser: "/app/node_modules/babel-eslint/lib/index.js",
                root: true,
                extends: [
                  "/app/node_modules/eslint-config-airbnb/index.js",
                  "/app/node_modules/eslint-config-airbnb/hooks.js",
                  "prettier",
                  "plugin:react/recommended",
                  "prettier/react",
                  "plugin:jest/recommended",
                ],
                rules: {
                  "react/state-in-constructor": ["error", "never"],
                  "new-cap": "off",
                  "no-invalid-this": "off",
                  "object-curly-spacing": "off",
                  semi: "off",
                  "no-unused-expressions": "off",
                  "babel/new-cap": [
                    "error",
                    {
                      newIsCap: true,
                      newIsCapExceptions: [],
                      capIsNew: false,
                      capIsNewExceptions: [
                        "Immutable.Map",
                        "Immutable.Set",
                        "Immutable.List",
                      ],
                    },
                  ],
                  "babel/no-invalid-this": "off",
                  "babel/object-curly-spacing": ["error", "always"],
                  "babel/semi": ["error", "always"],
                  "babel/no-unused-expressions": [
                    "error",
                    {
                      allowShortCircuit: false,
                      allowTernary: false,
                      allowTaggedTemplates: false,
                    },
                  ],
                  "react-hooks/rules-of-hooks": "error",
                  "react-hooks/exhaustive-deps": "warn",
                },
                env: {
                  es6: true,
                  browser: true,
                  commonjs: true,
                },
                globals: {
                  process: true,
                },
                parserOptions: {
                  ecmaVersion: 2018,
                  sourceType: "module",
                },
                plugins: ["babel", "react", "react-hooks"],
                settings: {
                  react: {
                    version: "detect",
                  },
                },
              },
              plugins: ["prettier"],
              rules: {
                "import/no-extraneous-dependencies": "off",
                "max-len": [
                  "error",
                  80,
                  2,
                  {
                    ignoreUrls: true,
                    ignoreComments: false,
                    ignoreStrings: true,
                    ignoreTemplateLiterals: true,
                  },
                ],
                "class-methods-use-this": "off",
                "no-console": "off",
                "no-extra-parens": "off",
                "prefer-const": "error",
                "prettier/prettier": [
                  "error",
                  {
                    singleQuote: true,
                    trailingComma: "es5",
                    bracketSpacing: true,
                    jsxBracketSameLine: true,
                    tabWidth: 2,
                    semi: true,
                  },
                ],
                "padding-line-between-statements": [
                  "error",
                  {
                    blankLine: "always",
                    prev: ["const", "let", "var"],
                    next: "*",
                  },
                  {
                    blankLine: "never",
                    prev: ["const", "let", "var"],
                    next: ["const", "let", "var"],
                  },
                  {
                    blankLine: "always",
                    prev: ["cjs-import"],
                    next: "*",
                  },
                  {
                    blankLine: "always",
                    prev: ["import"],
                    next: "*",
                  },
                  {
                    blankLine: "always",
                    prev: "*",
                    next: ["cjs-export"],
                  },
                  {
                    blankLine: "always",
                    prev: "*",
                    next: ["export"],
                  },
                  {
                    blankLine: "never",
                    prev: ["import"],
                    next: ["import"],
                  },
                  {
                    blankLine: "never",
                    prev: ["cjs-import"],
                    next: ["cjs-import"],
                  },
                  {
                    blankLine: "any",
                    prev: ["export"],
                    next: ["export"],
                  },
                  {
                    blankLine: "any",
                    prev: ["cjs-export"],
                    next: ["cjs-export"],
                  },
                  {
                    blankLine: "always",
                    prev: "multiline-block-like",
                    next: "*",
                  },
                  {
                    blankLine: "always",
                    prev: "*",
                    next: ["if", "do", "for", "switch", "try", "while"],
                  },
                  {
                    blankLine: "always",
                    prev: "*",
                    next: "return",
                  },
                ],
                "consistent-return": "off",
                "no-unused-expressions": "off",
                "no-shadow": "off",
                "no-return-assign": "off",
                "babel/new-cap": "off",
                "no-mixed-operators": "off",
                "jsx-quotes": ["error", "prefer-double"],
                "jsx-a11y/anchor-is-valid": [
                  "error",
                  {
                    components: ["Link"],
                    specialLink: ["to"],
                  },
                ],
                "jsx-a11y/click-events-have-key-events": "off",
                "jsx-a11y/no-static-element-interactions": "off",
                "react/jsx-indent-props": ["error", 2],
                "react/jsx-pascal-case": "error",
                "react/jsx-tag-spacing": [
                  "error",
                  {
                    beforeSelfClosing: "always",
                  },
                ],
                "react/default-props-match-prop-types": "off",
                "react/jsx-closing-bracket-location": "off",
                "react/destructuring-assignment": "off",
                "react/jsx-handler-names": [
                  "error",
                  {
                    eventHandlerPrefix: "handle",
                    eventHandlerPropPrefix: "on",
                  },
                ],
                "react/jsx-indent": "off",
                "react/prefer-stateless-function": "off",
                "react/prop-types": "off",
                "react/sort-comp": "off",
                "react/forbid-prop-types": "off",
                "react/no-unused-prop-types": "off",
                "react/require-default-props": "off",
                "react/jsx-fragments": ["error", "element"],
                "react/jsx-props-no-spreading": "off",
                "react/jsx-no-bind": "off",
                "react-hooks/exhaustive-deps": "off",
                "import/no-cycle": "off",
              },
            },
          },
        ],
      },
      {
        use: [
          {
            loader: "/app/node_modules/html-loader/index.js",
            options: {
              attrs: ["img:src", "link:href"],
            },
          },
        ],
      },
      {
        include: ["/app/src", "/app/test"],
        use: [
          {
            loader: "/app/node_modules/babel-loader/lib/index.js",
            options: {
              cacheDirectory: true,
              babelrc: false,
              configFile: false,
              presets: [
                [
                  "/app/node_modules/@babel/preset-env/lib/index.js",
                  {
                    debug: false,
                    useBuiltIns: false,
                    shippedProposals: true,
                    targets: {
                      browsers: [
                        "last 2 Chrome versions",
                        "last 2 Firefox versions",
                        "last 2 Edge versions",
                        "last 2 Opera versions",
                        "last 2 Safari versions",
                        "last 2 iOS versions",
                      ],
                    },
                  },
                ],
                [
                  "/app/node_modules/@babel/preset-react/lib/index.js",
                  {
                    development: true,
                    useSpread: true,
                  },
                ],
              ],
              plugins: [
                "/app/node_modules/@babel/plugin-syntax-dynamic-import/lib/index.js",
                "/app/node_modules/react-hot-loader/babel.js",
              ],
            },
          },
        ],
      },
      {
        oneOf: [
          {
            use: [
              {
                loader: "/app/node_modules/style-loader/dist/cjs.js",
              },
              {
                loader: "/app/node_modules/css-loader/dist/cjs.js",
                options: {
                  importLoaders: 0,
                  modules: true,
                },
              },
            ],
          },
          {
            use: [
              {
                loader: "/app/node_modules/style-loader/dist/cjs.js",
              },
              {
                loader: "/app/node_modules/css-loader/dist/cjs.js",
                options: {
                  importLoaders: 0,
                },
              },
            ],
          },
        ],
      },
      {
        use: [
          {
            loader: "/app/node_modules/file-loader/dist/cjs.js",
            options: {
              name: "assets/[name].[ext]",
            },
          },
        ],
      },
      {
        use: [
          {
            loader: "/app/node_modules/url-loader/dist/cjs.js",
            options: {
              limit: 8192,
              name: "assets/[name].[ext]",
            },
          },
        ],
      },
      {
        use: [
          {
            loader: "/app/node_modules/worker-loader/dist/cjs.js",
          },
        ],
      },
    ],
  },
  optimization: {
    minimize: false,
    splitChunks: {
      chunks: "all",
      name: true,
    },
    runtimeChunk: "single",
  },
  plugins: [
    new webpack.EnvironmentPlugin({
      HOST: "localhost",
      PORT: 9000,
      BALROG_ROOT_URL: "https://localhost:8010",
      AUTH0_CLIENT_ID: "GlZhJQfx52b7MLQ19AjuTJHieiB4oh1j",
      AUTH0_DOMAIN: "balrog-localdev.auth0.com",
      AUTH0_AUDIENCE: "balrog-localdev",
      AUTH0_RESPONSE_TYPE: "token id_token",
      AUTH0_SCOPE: "full-user-credentials openid profile email",
      AUTH0_REDIRECT_URI: "https://localhost:9000/login",
      GCS_NIGHTLY_HISTORY_BUCKET:
        "https://www.googleapis.com/storage/v1/b/balrog-prod-nightly-history-v1/o",
      GCS_RELEASES_HISTORY_BUCKET:
        "https://www.googleapis.com/storage/v1/b/balrog-prod-release-history-v1/o",
    }),
    new HtmlWebpackPlugin({
      template: "src/index.html",
      templateContent: false,
      filename: "index.html",
      publicPath: "auto",
      hash: false,
      inject: "body",
      scriptLoading: "blocking",
      compile: true,
      favicon: "/app/src/images/favicon.png",
      minify: "auto",
      cache: true,
      showErrors: true,
      chunks: ["index"],
      excludeChunks: [],
      chunksSortMode: "auto",
      meta: {
        viewport: "width=device-width, initial-scale=1",
      },
      base: false,
      title: "Webpack App",
      xhtml: false,
      appMountId: "root",
      lang: "en",
    }),
    new webpack.HotModuleReplacementPlugin({}),
  ],
  entry: {
    index: ["/app/src/index"],
  },
};
