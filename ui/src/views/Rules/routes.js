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

export default (path) => [
  {
    component: Rule,
    path: `${path}/create/:scId`,
    isNewRule: true,
  },
  {
    component: Rule,
    path: `${path}/create`,
    isNewRule: true,
  },
  {
    component: Rule,
    path: `${path}/duplicate/scId/:scId`,
    isNewRule: true,
  },
  {
    component: Rule,
    path: `${path}/duplicate/ruleId/:ruleId`,
    isNewRule: true,
  },
  {
    component: ListRuleRevisions,
    path: `${path}/:ruleId/revisions`,
  },
  {
    component: Rule,
    path: `${path}/:ruleId`,
  },
  {
    component: ListRules,
    path,
  },
];
