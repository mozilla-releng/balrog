import React, { useState } from 'react';
import { NavLink, Link as RouterLink } from 'react-router';
import routes from '../routes';
import matchRoutes from './matchRoutes';

/**
 * A react hook which augments `react-router`'s `Link` component
 * with pre-fetching capabilities.
 */
export default function Link({ viewName, nav, to, ...props }) {
  const isPathAbsolute = URL.canParse(to);
  const Component = nav ? NavLink : RouterLink;
  const [prefetchFlag, setPrefetchFlag] = useState(false);

  function prefetch() {
    if (prefetchFlag) {
      return;
    }

    if (!isPathAbsolute) {
      const matchingRoutes = matchRoutes(to, routes);

      matchingRoutes.forEach(({ component }) => {
        component.preload();
      });
    }

    setPrefetchFlag(true);
  }

  function handleFocus(e) {
    const { onFocus } = props;

    prefetch();

    if (onFocus) {
      onFocus(e);
    }
  }

  function handleMouseOver(e) {
    const { onMouseOver } = props;

    prefetch();

    if (onMouseOver) {
      onMouseOver(e);
    }
  }

  return isPathAbsolute ? (
    <a href={to} {...props} target="_blank" rel="noopener noreferrer" />
  ) : (
    <Component
      {...props}
      to={to}
      onFocus={handleFocus}
      onMouseOver={handleMouseOver}
    />
  );
}

Link.defaultProps = {
  nav: false,
};
