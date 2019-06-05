import { hot } from 'react-hot-loader/root';
import React, { Fragment, useState } from 'react';
import { Authorize } from 'react-auth0-components';
import CssBaseline from '@material-ui/core/CssBaseline';
import { ThemeProvider } from '@material-ui/styles';
import { AuthContext } from './utils/AuthContext';
import { USER_SESSION } from './utils/constants';
import theme from './theme';
import Main from './Main';

const App = () => {
  const [authorize, setAuthorize] = useState(
    Boolean(localStorage.getItem(USER_SESSION))
  );
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
  const handleAuthorize = user => {
    setAuthContext({
      ...authContext,
      user,
    });
  };

  return (
    <Fragment>
      <CssBaseline />
      <AuthContext.Provider value={authContext}>
        <ThemeProvider theme={theme}>
          <Authorize
            authorize={authorize}
            onAuthorize={handleAuthorize}
            popup
            domain={process.env.AUTH0_DOMAIN}
            clientID={process.env.AUTH0_CLIENT_ID}
            audience={process.env.AUTH0_AUDIENCE}
            redirectUri={process.env.AUTH0_REDIRECT_URI}
            responseType={process.env.AUTH0_RESPONSE_TYPE}
            scope={process.env.AUTH0_SCOPE}
            render={() => {
              const session = localStorage.getItem(USER_SESSION);

              if (session) {
                const user = JSON.parse(session);
                const expires = new Date(user.expiration);
                const now = new Date();

                if (expires < now && user) {
                  authContext.unauthorize();
                }
              }

              return <Main />;
            }}
          />
        </ThemeProvider>
      </AuthContext.Provider>
    </Fragment>
  );
};

export default hot(App);
