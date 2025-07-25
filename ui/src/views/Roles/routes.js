import lazy from '../../utils/lazy';

const ListRoles = lazy(
  () => import(/* webpackChunkName: 'Roles.ListRoles' */ './ListRoles'),
);

export default (path) => [
  {
    component: ListRoles,
    path,
  },
];
