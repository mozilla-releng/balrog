import { withAuth0 } from '@auth0/auth0-react';
import React, { Suspense } from 'react';
import { Redirect, Route } from 'react-router-dom';

/**
 * Conditionally render a component based on location, with non-react-router
 * specific properties forwarded to the rendering component.
 */
function RouteWithProps(props) {
  const {
    auth0,
    requiresAuth,
    component: Component,
    path,
    exact,
    strict,
    location,
    sensitive,
    ...rest
  } = props;

  return (
    <Route
      path={path}
      exact={exact}
      strict={strict}
      location={location}
      sensitive={sensitive}
      render={({ staticContext, ...renderProps }) => (
        <Suspense fallback={null}>
          {requiresAuth && !auth0.user ? (
            <Redirect to="/" />
          ) : (
            <Component {...renderProps} {...rest} />
          )}
        </Suspense>
      )}
    />
  );
}

export default withAuth0(RouteWithProps);
