import axios from 'axios';
import React, { Fragment, useEffect, useState } from 'react';
import { Column } from 'react-virtualized';
import 'react-virtualized/styles.css';
import Drawer from '@material-ui/core/Drawer';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/styles';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { formatDistanceStrict } from 'date-fns';
import Button from '../../../components/Button';
import Dashboard from '../../../components/Dashboard';
import DiffRelease from '../../../components/DiffRelease';
import ErrorPanel from '../../../components/ErrorPanel';
import Radio from '../../../components/Radio';
import RevisionsTable from '../../../components/RevisionsTable';
import useAction from '../../../hooks/useAction';
import { getRevisions } from '../../../services/releases';
import { CONTENT_MAX_WIDTH } from '../../../utils/constants';

const useStyles = makeStyles((theme) => ({
  radioCell: {
    paddingLeft: 0,
  },
  drawerPaper: {
    maxWidth: CONTENT_MAX_WIDTH,
    margin: '0 auto',
    padding: theme.spacing(1),
    maxHeight: '80vh',
  },
  tableHeader: {
    textTransform: 'none',
    color: theme.palette.text.secondary,
    fontSize: theme.typography.pxToRem(12),
    lineHeight: theme.typography.pxToRem(21),
    fontWeight: theme.typography.fontWeightMedium,
    '& > [title="Compare"]': {
      marginLeft: theme.spacing(2),
    },
  },
  jsDiff: {
    margin: `${theme.spacing(5)}px 0`,
  },
}));

function ListReleaseRevisionsV2(props) {
  const classes = useStyles();
  const { releaseName } = props.match.params;
  const [fetchedRevisions, fetchRevisions] = useAction(getRevisions);
  const [fetchedRevisionData, fetchRevisionData] = useAction(axios.get);
  const [drawerState, setDrawerState] = useState({ open: false, item: {} });
  const [leftRadioCheckedIndex, setLeftRadioCheckedIndex] = useState(1);
  const [leftRevisionData, setLeftRevisionData] = useState(null);
  const [rightRevisionData, setRightRevisionData] = useState(null);
  const [rightRadioCheckedIndex, setRightRadioCheckedIndex] = useState(0);
  const error = fetchedRevisions.error || fetchedRevisionData.error;
  const isLoading = fetchedRevisions.loading;
  // The most recent revision for each part of the Release
  // and a list of all of the older revisions (of which
  // there may be many for each part of the Release).
  const [latestRevisions, olderRevisions] = fetchedRevisions.data
    ? fetchedRevisions.data
    : [[], []];
  // This is a bit of a hack to make sure the very first listed
  // revision will show the entire Release instead of just the
  // part of it that changed most recently.
  // This is the same data structure as the lists above use, but
  // with semi-faked data. Most notably, `data_url` points at the
  // Balrog URL that will retrieve the current version of the
  // entire Release rather than a GCS link that only contains
  // the most recently changed part.
  const currentRevision =
    latestRevisions.length > 0
      ? {
          path: null,
          timestamp: latestRevisions[0].timestamp,
          changed_by: latestRevisions[0].changed_by,
          data_url: `/v2/releases/${releaseName}`,
        }
      : {};
  const prettyPath =
    olderRevisions.length > 0
      ? olderRevisions[leftRadioCheckedIndex - 1].path
        ? olderRevisions[leftRadioCheckedIndex - 1].path
        : 'Base'
      : '';

  useEffect(() => {
    fetchRevisions(releaseName, 2);
  }, [releaseName]);

  const handleLeftRadioChange = ({ target: { value } }) => {
    setLeftRadioCheckedIndex(Number(value));
  };

  const handleRightRadioChange = ({ target: { value } }) => {
    setRightRadioCheckedIndex(Number(value));
  };

  const handleDrawerClose = () => {
    setDrawerState({
      ...drawerState,
      open: false,
    });
  };

  const handleViewClick = (item) => async () => {
    const section =
      item.path === null
        ? 'entire Release'
        : item.path === ''
          ? 'base'
          : item.path;
    const when = new Date(item.timestamp);
    const result = await fetchRevisionData(item.data_url);

    setDrawerState({
      ...drawerState,
      // Result could come from Balrog, where what we want to display is in
      // `blob` or from GCS, where its the entire `data`.
      item: result.data.data.blob ? result.data.data.blob : result.data.data,
      title: `Contents of ${section} at ${when}`,
      open: true,
    });
  };

  useEffect(() => {
    const olderRevision = olderRevisions[leftRadioCheckedIndex - 1];

    if (olderRevision) {
      // The left revision is always a part of the Release
      // that we can retrieve from GCS.
      axios.get(olderRevision.data_url).then((result) => {
        setLeftRevisionData(result.data || {});
      });

      // In order to display a useful diff, we need the right revision
      // to be the most recent version of the same part of the Release,
      // which we can find by looking for the older revisions path in
      // `latestRevisions`.
      const latestRevision = latestRevisions.find(
        (r) => r.path === olderRevision.path,
      );

      if (latestRevision) {
        axios.get(latestRevision.data_url).then((result) => {
          // FIXME: sometimes the page doesn't rerender the diff after this
          // for some reason...
          // I think there's some sort of race condition, or issue with the
          // depedencies on this useEffect.
          setRightRevisionData(result.data || {});
        });
      }
    }
  }, [
    leftRadioCheckedIndex,
    fetchedRevisions.data,
    olderRevisions,
    latestRevisions,
  ]);

  const revisionsCount = olderRevisions.length;
  const columnWidth = CONTENT_MAX_WIDTH / 4;

  return (
    <Dashboard title={`Release ${releaseName} Revisions`}>
      {error && <ErrorPanel fixed error={error} />}
      {isLoading && <Spinner loading />}
      {!isLoading && olderRevisions.length === 1 && (
        <Typography>{releaseName} has no revisions</Typography>
      )}
      {!isLoading && revisionsCount > 1 && (
        <Fragment>
          <RevisionsTable
            rowCount={revisionsCount + 1}
            rowGetter={({ index }) =>
              index === 0 ? currentRevision : olderRevisions[index - 1]
            }
          >
            <Column
              label="Revision Date"
              dataKey="timestamp"
              cellRenderer={({ cellData }) =>
                formatDistanceStrict(new Date(cellData), new Date(), {
                  addSuffix: true,
                })
              }
              width={columnWidth}
            />
            <Column
              width={columnWidth}
              label="Changed By"
              dataKey="changed_by"
            />
            <Column
              label="Compare"
              dataKey="compare"
              width={columnWidth}
              cellRenderer={({ rowIndex }) => (
                <Fragment>
                  <Radio
                    variant="red"
                    value={rowIndex}
                    disabled={rowIndex === 0}
                    checked={leftRadioCheckedIndex === rowIndex}
                    onChange={handleLeftRadioChange}
                  />
                  {/* Always disabled for V2 API because revisions only
                   contain partial objects. Allowing a diff against
                   two partial objects would potentially require
                   fetching hundreds of revisions and rebuilding
                   the object from scratch.
                   Instead, we only support diffing the current revision
                   against one older revision.
                  */}
                  <Radio
                    variant="green"
                    value={rowIndex}
                    disabled
                    checked={rightRadioCheckedIndex === rowIndex}
                    onChange={handleRightRadioChange}
                  />
                </Fragment>
              )}
            />
            <Column
              dataKey="actions"
              width={columnWidth}
              cellRenderer={({ rowData }) => (
                <Fragment>
                  <Button onClick={handleViewClick(rowData)}>View</Button>
                </Fragment>
              )}
            />
          </RevisionsTable>
          {leftRevisionData && rightRevisionData && (
            <DiffRelease
              className={classes.jsDiff}
              firstFilename={`Revision Version ${
                olderRevisions[leftRadioCheckedIndex - 1].data_version
              } for ${prettyPath}`}
              secondFilename="Current Version"
              firstRelease={leftRevisionData || {}}
              secondRelease={rightRevisionData || {}}
            />
          )}
          <Drawer
            classes={{ paper: classes.drawerPaper }}
            anchor="bottom"
            open={drawerState.open}
            onClose={handleDrawerClose}
          >
            <pre>
              <h3>{drawerState.title}</h3>
              <code>{JSON.stringify(drawerState.item, null, 2)}</code>
            </pre>
          </Drawer>
        </Fragment>
      )}
    </Dashboard>
  );
}

export default ListReleaseRevisionsV2;
