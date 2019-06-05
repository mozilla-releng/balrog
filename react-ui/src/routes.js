import lazy from './utils/lazy';
import releaseRoutes from './views/Releases/routes';
import ruleRoutes from './views/Rules/routes';
import requiredSignoffsRoutes from './views/RequiredSignoffs/routes';

const History = lazy(() =>
  import(/* webpackChunkName: 'History' */ './views/History')
);
const Home = lazy(() => import(/* webpackChunkName: 'Home' */ './views/Home'));
const Releases = lazy(() =>
  import(/* webpackChunkName: 'Releases' */ './views/Releases')
);
const Rules = lazy(() =>
  import(/* webpackChunkName: 'Rules' */ './views/Rules')
);
const Users = lazy(() =>
  import(/* webpackChunkName: 'Users' */ './views/Users')
);
const Roles = lazy(() =>
  import(/* webpackChunkName: 'Roles' */ './views/Roles')
);
const RequiredSignoffs = lazy(() =>
  import(/* webpackChunkName: 'RequiredSignoffs' */ './views/RequiredSignoffs')
);
const Login = lazy(() =>
  import(/* webpackChunkName: 'Login' */ './views/Login')
);

export default [
  {
    component: Releases,
    path: '/releases',
    routes: releaseRoutes('/releases'),
  },
  {
    component: Rules,
    path: '/rules',
    routes: ruleRoutes('/rules'),
  },
  {
    component: History,
    path: '/history',
  },
  {
    component: Users,
    path: '/users',
  },
  {
    component: Roles,
    path: '/roles',
  },
  {
    component: RequiredSignoffs,
    path: '/required-signoffs',
    routes: requiredSignoffsRoutes('/required-signoffs'),
  },
  {
    component: Login,
    path: '/login',
  },
  {
    component: Home,
    path: '/',
    exact: true,
  },
];
