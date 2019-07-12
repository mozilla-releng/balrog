import React from 'react';
import { BrowserRouter, Switch } from 'react-router-dom';
import { makeStyles } from '@material-ui/styles';
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
  },
});

function Main() {
  useStyles();

  return (
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
