import { useAuth0 } from '@auth0/auth0-react';
import { makeStyles } from '@material-ui/styles';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { BrowserRouter, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ErrorPanel from './components/ErrorPanel';
import RouteWithProps from './components/RouteWithProps';
import routes from './routes';
import { BASE_URL } from './utils/constants';

const useStyles = makeStyles({
  '@global': {
    'html, body': {
      height: '100%',
    },
    '#root': {
      height: '100%',
    },
    '.CodeMirror': {
      fontSize: 13,
      height: '100% !important',
      position: 'absolute !important',
      top: 0,
      bottom: 0,
      left: 0,
      right: 0,
    },
    '.react-codemirror2': {
      height: '100%',
      position: 'relative',
    },
  },
});

function setupAxiosInterceptors(getAccessTokenSilently, getIdTokenClaims) {
  axios.interceptors.request.use(async (config) => {
    const result = config;

    if (!config.url.startsWith('http')) {
      result.baseURL = BASE_URL;

      const claims = await getIdTokenClaims();

      if (claims) {
        const accessToken = await getAccessTokenSilently();

        result.headers.Authorization = `Bearer ${accessToken}`;
      }
    }

    return result;
  });

  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      const errorMsg = error.response
        ? error.response.data.exception || error.response.data.detail || null
        : error.message;

      // If we found a more detailed error message
      // raise an Error with that instead.
      if (errorMsg !== null) {
        throw new Error(errorMsg);
      }

      throw error;
    },
  );
}

function Main() {
  const { isLoading, getAccessTokenSilently, getIdTokenClaims } = useAuth0();
  const [isReady, setReady] = useState(false);

  useEffect(() => {
    setupAxiosInterceptors(getAccessTokenSilently, getIdTokenClaims);
  }, [getAccessTokenSilently, isLoading]);

  useEffect(() => {
    if (!isReady && !isLoading) {
      setReady(true);
    }
  }, [isLoading]);

  useStyles();
  const [backendError, setBackendError] = useState('');

  useEffect(() => {
    axios.get('/__heartbeat__').then(
      () => setBackendError(''),
      (error) => {
        setBackendError(
          `Error contacting Balrog backend: ${error}. Are you connected to the VPN?`,
        );
      },
    );
  }, []);

  if (!isReady) {
    return <div>Loading...</div>;
  }

  return backendError ? (
    <BrowserRouter>
      <Dashboard title="Error" disabled>
        <ErrorPanel fixed error={backendError} />
      </Dashboard>
    </BrowserRouter>
  ) : (
    <BrowserRouter>
      <Switch>
        {routes.map(({ path, ...rest }) => (
          <RouteWithProps key={path || 'not-found'} path={path} {...rest} />
        ))}
      </Switch>
    </BrowserRouter>
  );
}

export default Main;
