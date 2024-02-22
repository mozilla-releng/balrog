const reactLint = require('@mozilla-frontend-infra/react-lint')
const react = require('@neutrinojs/react');
const jest = require('@neutrinojs/jest');

const DEFAULT_HOST = 'localhost';
const DEFAULT_PORT = 9000;
const port = process.env.PORT || DEFAULT_PORT;

module.exports = {
  options: {
    root: __dirname,
  },
  use: [
    reactLint({
      rules: {
        'react/jsx-props-no-spreading': 'off',
        'react/jsx-no-bind': 'off',
        'react-hooks/exhaustive-deps': 'off',
        'import/no-cycle': 'off',
      }
    }),
    react({
      devServer: {
        host: process.env.HOST || DEFAULT_HOST,
        port,
        https: true,
        historyApiFallback: {
          disableDotRule: true,
        },
        headers: {
          /*
            Whenever this changes we will also need to update the headers
            for our deployed environments in the cloudops repo (TODO: add link).

            script-src: unsafe-eval is only for local dev, because of webpack/hotreload
            img-src: gravatar & githubusercontent & i1.wp.com for user avatars
                     (which can't be locked down to a specific path due to CSP format)
            style-src: https://fonts.googleapis.com for dynamically loaded fonts
                       'unsafe-inline' because CSS-in-JS needs them
                       TODO: we should look into using a nonce or hash to avoid this
            font-src: https://fonts.gstatic.com for fonts!
            connect-src: https://localhost:8010 for the backend api
                         https://www.googleapis.com/ for releases history
                         'self' for webpack connections (local dev only)
                         https://balrog-localdev.auth0.com for authentication.
                         note: this is different in stage/prod
            frame-src: https://balrog-localdev.auth0.com for background token refreshes
            frame-ancestors: 'none' because nobody should be embedding this UI.
            base-uri: 'none' because we don't have a <base> tag
            form-action: 'none' because we don't submit forms
          */
          'Content-Security-Policy': "default-src 'none'; script-src 'self' 'unsafe-eval'; img-src 'self' https://*.gravatar.com https://*.githubusercontent.com https://i1.wp.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; connect-src https://localhost:8010 'self' https://balrog-localdev.auth0.com https://www.googleapis.com/; frame-src https://balrog-localdev.auth0.com; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
          'X-Frame-Options': 'SAMEORIGIN',
          'X-Content-Type-Options': 'nosniff',
          'X-XSS-Protection': '1; mode=block',
          'Referrer-Policy': 'no-referrer',
          'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; always;',
        },
      },
      html: {
        favicon: `${__dirname}/src/images/favicon.png`,
        template: 'src/index.html',
      },
      env: {
        HOST: DEFAULT_HOST,
        PORT: DEFAULT_PORT,
        BALROG_ROOT_URL: 'https://localhost:8010',
        AUTH0_CLIENT_ID: 'GlZhJQfx52b7MLQ19AjuTJHieiB4oh1j',
        AUTH0_DOMAIN: 'balrog-localdev.auth0.com',
        AUTH0_AUDIENCE: 'balrog-localdev',
        NODE_ENV: process.env.NODE_ENV,
        AUTH0_RESPONSE_TYPE: 'token id_token',
        AUTH0_SCOPE: 'full-user-credentials openid profile email',
        AUTH0_REDIRECT_URI: `https://localhost:${port}/login`,
        GCS_NIGHTLY_HISTORY_BUCKET: 'https://www.googleapis.com/storage/v1/b/balrog-prod-nightly-history-v1/o',
        GCS_RELEASES_HISTORY_BUCKET: 'https://www.googleapis.com/storage/v1/b/balrog-prod-release-history-v1/o',
      },
    }),
    (neutrino) => {  
      neutrino.config.resolve.alias
        .set('react-dom', '@hot-loader/react-dom');
    
      neutrino.config.output.set('globalObject', 'this');
      neutrino.config.module
        .rule('worker')
          .test(/\.worker\.js$/)
          .use('worker')
            .loader(require.resolve('worker-loader'));
    },
    jest()
  ]
};
