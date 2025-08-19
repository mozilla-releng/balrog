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

export default () => [
  {
    component: ReleaseV2,
    path: 'create/v2',
    isNewRelease: true,
  },
  {
    component: ListReleaseRevisionsV2,
    path: ':releaseName/revisions/v2',
  },
  {
    component: ListReleaseRevisions,
    path: ':releaseName/revisions',
  },
  {
    component: ReleaseV2,
    path: ':releaseName/v2',
  },
  {
    component: Release,
    path: ':releaseName',
  },
  {
    component: ListReleases,
    path: '',
  },
];
