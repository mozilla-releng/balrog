import lazy from '../../utils/lazy';

const ListRules = lazy(() =>
  import(/* webpackChunkName: 'Rules.ListRules' */ './ListRules')
);
const Rule = lazy(() => import(/* webpackChunkName: 'Rules.Rule' */ './Rule'));

export default path => [
  {
    component: Rule,
    path: `${path}/create`,
  },
  {
    component: ListRules,
    path,
  },
];
