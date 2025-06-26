import React, { Suspense } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { withUser } from '../../utils/AuthContext';

/**
 * Conditionally render a component based on location, with non-react-router
 * specific properties forwarded to the rendering component.
 */
function RouteWithProps(props) {
  const {
    user,
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
          {requiresAuth && !user ? (
            <Redirect to="/" />
          ) : (
            <Component {...renderProps} {...rest} />
          )}
        </Suspense>
      )}
    />
  );
}

export default withUser(RouteWithProps);
