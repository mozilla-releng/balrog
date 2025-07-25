import lazy from '../../utils/lazy';

const ListReleases = lazy(
  () =>
    import(/* webpackChunkName: 'Releases.ListReleases' */ './ListReleases'),
);
const ListReleaseRevisionsV2 = lazy(
  () =>
    import(
      /* webpackChunkName: 'Releases.ListReleaseRevisionsV2' */ './ListReleaseRevisionsV2'
    ),
);
const ListReleaseRevisions = lazy(
  () =>
    import(
      /* webpackChunkName: 'Releases.ListReleaseRevisions' */ './ListReleaseRevisions'
    ),
);
const Release = lazy(
  () => import(/* webpackChunkName: 'Releases.Release' */ './Release'),
);
const ReleaseV2 = lazy(
  () => import(/* webpackChunkName: 'Releases.ReleaseV2' */ './ReleaseV2'),
);

export default (path) => [
  {
    component: ReleaseV2,
    path: `${path}/create/v2`,
    isNewRelease: true,
  },
  {
    component: ListReleaseRevisionsV2,
    path: `${path}/:releaseName/revisions/v2`,
  },
  {
    component: ListReleaseRevisions,
    path: `${path}/:releaseName/revisions`,
  },
  {
    component: ReleaseV2,
    path: `${path}/:releaseName/v2`,
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
