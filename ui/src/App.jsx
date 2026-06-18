import { Auth0Provider } from '@auth0/auth0-react';
import CssBaseline from '@mui/material/CssBaseline';
import { StyledEngineProvider, ThemeProvider } from '@mui/material/styles';
import React from 'react';
import { GlobalStyles } from 'tss-react';
import Main from './Main';
import theme from './theme';

const App = () => {
  return (
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={theme}>
        <GlobalStyles
          styles={{
            'html, body': {
              height: '100%',
            },
            '#root': {
              height: '100%',
            },
            '.cm-editor': {
              fontSize: 13,
              height: '100%',
            },
            '.cm-theme': {
              flex: 1,
              overflow: 'auto',
            },
          }}
        />
        <CssBaseline />
        <Auth0Provider
          domain={process.env.AUTH0_DOMAIN}
          clientId={process.env.AUTH0_CLIENT_ID}
          authorizationParams={{
            redirect_uri: process.env.AUTH0_REDIRECT_URI,
            audience: process.env.AUTH0_AUDIENCE,
            scope: process.env.AUTH0_SCOPE,
          }}
          leeway={30}
          cacheLocation="localstorage"
          sessionCheckExpiryDays={7}
        >
          <Main />
        </Auth0Provider>
      </ThemeProvider>
    </StyledEngineProvider>
  );
};

export default App;
