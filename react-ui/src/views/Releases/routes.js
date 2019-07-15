import lazy from '../../utils/lazy';

const ListReleases = lazy(() =>
  import(/* webpackChunkName: 'Releases.ListReleases' */ './ListReleases')
);
const Release = lazy(() =>
  import(/* webpackChunkName: 'Releases.ListReleases' */ './Release')
);

export default path => [
  {
    component: Release,
    path: `${path}/create`,
  },
  {
    component: ListReleases,
    path,
  },
];
