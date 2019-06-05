import React, { Suspense } from 'react';
import { Route } from 'react-router-dom';

/**
 * Conditionally render a component based on location, with non-react-router
 * specific properties forwarded to the rendering component.
 */
function RouteWithProps(props) {
  const {
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
          <Component {...renderProps} {...rest} />
        </Suspense>
      )}
    />
  );
}

export default RouteWithProps;
