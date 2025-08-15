import lazy from '../../utils/lazy';

const ListRules = lazy(
  () => import(/* webpackChunkName: 'Rules.ListRules' */ './ListRules'),
);
const ListRuleRevisions = lazy(
  () =>
    import(
      /* webpackChunkName: 'Rules.ListRuleRevisions' */ './ListRuleRevisions'
    ),
);
const Rule = lazy(() => import(/* webpackChunkName: 'Rules.Rule' */ './Rule'));

export default () => [
  {
    component: Rule,
    path: 'create/:scId',
    isNewRule: true,
  },
  {
    component: Rule,
    path: 'create',
    isNewRule: true,
  },
  {
    component: Rule,
    path: 'duplicate/scId/:scId',
    isNewRule: true,
  },
  {
    component: Rule,
    path: 'duplicate/ruleId/:ruleId',
    isNewRule: true,
  },
  {
    component: ListRuleRevisions,
    path: ':ruleId/revisions',
  },
  {
    component: Rule,
    path: ':ruleId',
  },
  {
    component: ListRules,
    path: '',
  },
];
