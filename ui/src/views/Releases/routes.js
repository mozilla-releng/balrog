import lazy from '../../utils/lazy';

const ListReleases = lazy(() =>
  import(/* webpackChunkName: 'Releases.ListReleases' */ './ListReleases')
);
const ListReleaseRevisions = lazy(() =>
  import(
    /* webpackChunkName: 'Releases.ListReleaseRevisions' */ './ListReleaseRevisions'
  )
);
const Release = lazy(() =>
  import(/* webpackChunkName: 'Releases.Release' */ './Release')
);

export default path => [
  {
    component: Release,
    path: `${path}/create`,
    isNewRelease: true,
  },
  {
    component: ListReleaseRevisions,
    path: `${path}/:releaseName/revisions`,
  },
  {
    component: Release,
    path: `${path}/:releaseName`,
  },
  {
    component: ListReleases,
    path,
  },
];
