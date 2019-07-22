import React from 'react';
import { Switch } from 'react-router-dom';
import RouteWithProps from '../../components/RouteWithProps';
import routes from './routes';

export default function Roles(props) {
  const {
    match: { path },
  } = props;

  return (
    <Switch>
      {routes(path).map(({ routes, ...routeProps }) => (
        <RouteWithProps key={routeProps.path || 'not-found'} {...routeProps} />
      ))}
    </Switch>
  );
}
