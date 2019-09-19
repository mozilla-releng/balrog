import { hot } from 'react-hot-loader/root';
import React, { Fragment, useEffect, useState } from 'react';
import { Authorize } from 'react-auth0-components';
import CssBaseline from '@material-ui/core/CssBaseline';
import { ThemeProvider } from '@material-ui/styles';
import axios from 'axios';
import { AuthContext } from './utils/AuthContext';
import { BASE_URL, USER_SESSION } from './utils/constants';
import theme from './theme';
import Main from './Main';

axios.interceptors.request.use(config => {
  const result = config;

  if (!config.url.startsWith('http')) {
    let accessToken = null;

    result.baseURL = BASE_URL;

    try {
      ({ accessToken } = JSON.parse(
        localStorage.getItem(USER_SESSION)
      ).authResult);
    } catch {
      accessToken = null;
    }

    if (accessToken) {
      result.headers.Authorization = `Bearer ${accessToken}`;
    }
  }

  return result;
});
axios.interceptors.response.use(
  response => response,
  error => {
    const errorMsg = error.response
      ? error.response.data.exception || error.response.data.detail || null
      : error.message;

    // If we found a more detailed error message
    // raise an Error with that instead.
    if (errorMsg !== null) {
      throw new Error(errorMsg);
    }

    throw error;
  }
);

const App = () => {
  const userSession = localStorage.getItem(USER_SESSION);
  const [authorize, setAuthorize] = useState(Boolean(userSession));
  const [authContext, setAuthContext] = useState({
    authorize: () => setAuthorize(true),
    unauthorize: () => {
      setAuthorize(false);
      setAuthContext({
        ...authContext,
        user: null,
      });
    },
    user: null,
  });
  // Wait until authorization is done before rendering
  // to make sure users who are logged in are able to access protected views
  const [ready, setReady] = useState(false);

  // When the user is not logged in, handleAuthorize and handleError will never
  // be triggered since the `authorize` prop is set to `false`.
  useEffect(() => {
    if (!userSession) {
      setReady(true);
    }
  }, [userSession]);

  const handleAuthorize = user => {
    setAuthContext({
      ...authContext,
      user,
    });
    setReady(true);
  };

  const handleError = () => {
    setAuthContext({
      ...authContext,
      user: null,
    });
    setReady(true);
  };

  const render = () => <Main />;

  return (
    <Fragment>
      <CssBaseline />
      <AuthContext.Provider value={authContext}>
        <ThemeProvider theme={theme}>
          <Authorize
            authorize={authorize}
            onAuthorize={handleAuthorize}
            onError={handleError}
            popup
            domain={process.env.AUTH0_DOMAIN}
            clientID={process.env.AUTH0_CLIENT_ID}
            audience={process.env.AUTH0_AUDIENCE}
            redirectUri={process.env.AUTH0_REDIRECT_URI}
            responseType={process.env.AUTH0_RESPONSE_TYPE}
            scope={process.env.AUTH0_SCOPE}
            render={ready ? render : null}
            leeway={30}
          />
        </ThemeProvider>
      </AuthContext.Provider>
    </Fragment>
  );
};

export default hot(App);
