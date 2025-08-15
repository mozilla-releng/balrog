import React from 'react';
import { Route, Routes } from 'react-router-dom';
import routes from './routes';

export default function Users(props) {
  const { path } = props;

  return (
    <Routes>
      {routes(path).map(({ component: Component, ...routeProps }) => (
        <Route
          key={routeProps.path || 'not-found'}
          {...routeProps}
          element={<Component {...routeProps} />}
        />
      ))}
    </Routes>
  );
}
