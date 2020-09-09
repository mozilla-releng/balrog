import React, { useEffect, useState } from 'react';
import { BrowserRouter, Switch } from 'react-router-dom';
import { makeStyles } from '@material-ui/styles';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import ErrorPanel from './components/ErrorPanel';
import RouteWithProps from './components/RouteWithProps';
import routes from './routes';

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

function Main() {
  useStyles();
  const [backendError, setBackendError] = useState('');

  useEffect(() => {
    axios.get('/__heartbeat__').then(
      () => setBackendError(''),
      error => {
        setBackendError(
          `Error contacting Balrog backend: ${error}. Are you connected to the VPN?`
        );
      }
    );
  }, []);

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
