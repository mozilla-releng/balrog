import lazy from '../../utils/lazy';

const ListUsers = lazy(
  () => import(/* webpackChunkName: 'Users.ListUsers' */ './ListUsers'),
);
const ViewUser = lazy(
  () => import(/* webpackChunkName: 'Users.ViewUser' */ './ViewUser'),
);

export default () => [
  {
    component: ViewUser,
    path: 'create',
    isNewUser: true,
  },
  {
    component: ViewUser,
    path: ':username',
  },
  {
    component: ListUsers,
    path: '',
  },
];
