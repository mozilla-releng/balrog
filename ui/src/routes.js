import lazy from './utils/lazy';
import releaseRoutes from './views/Releases/routes';
import requiredSignoffsRoutes from './views/RequiredSignoffs/routes';
import roleRoutes from './views/Roles/routes';
import ruleRoutes from './views/Rules/routes';
import userRoutes from './views/Users/routes';

const Home = lazy(() => import(/* webpackChunkName: 'Home' */ './views/Home'));
const Releases = lazy(
  () => import(/* webpackChunkName: 'Releases' */ './views/Releases'),
);
const Rules = lazy(
  () => import(/* webpackChunkName: 'Rules' */ './views/Rules'),
);
const Users = lazy(
  () => import(/* webpackChunkName: 'Users' */ './views/Users'),
);
const Roles = lazy(
  () => import(/* webpackChunkName: 'Roles' */ './views/Roles'),
);
const RequiredSignoffs = lazy(
  () =>
    import(
      /* webpackChunkName: 'RequiredSignoffs' */ './views/RequiredSignoffs'
    ),
);

export default [
  {
    component: Releases,
    path: '/releases/*',
    routes: releaseRoutes('/releases'),
  },
  {
    component: Rules,
    path: '/rules/*',
    routes: ruleRoutes('/rules'),
  },
  {
    component: Users,
    path: '/users/*',
    routes: userRoutes('/users'),
    requiresAuth: true,
  },
  {
    component: Roles,
    path: '/roles/*',
    routes: roleRoutes('/roles'),
    requiresAuth: true,
  },
  {
    component: RequiredSignoffs,
    path: '/required-signoffs/*',
    routes: requiredSignoffsRoutes('/required-signoffs'),
    requiresAuth: true,
  },
  {
    component: Home,
    path: '/',
  },
];
