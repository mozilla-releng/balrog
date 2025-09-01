import { matchPath } from 'react-router';

// Returns an array of matched routes.
const matchRoutes = (path, routes, branch = []) => {
  const matchingRoute = routes.find((route) =>
    matchPath(
      {
        path: route.path,
        end: route.exact,
      },
      path,
    ),
  );

  if (matchingRoute) {
    branch.push(matchingRoute);

    if (matchingRoute.routes) {
      matchRoutes(path, matchingRoute.routes, branch);
    }
  }

  return branch;
};

export default matchRoutes;
