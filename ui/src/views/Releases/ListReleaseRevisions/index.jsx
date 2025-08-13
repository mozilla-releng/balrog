import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';
import Drawer from '@material-ui/core/Drawer';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/styles';
import axios from 'axios';
import { formatDistanceStrict } from 'date-fns';
import React, { Fragment, useEffect, useState } from 'react';
import Button from '../../../components/Button';
import Dashboard from '../../../components/Dashboard';
import DiffRelease from '../../../components/DiffRelease';
import ErrorPanel from '../../../components/ErrorPanel';
import Radio from '../../../components/Radio';
import RevisionsTable from '../../../components/RevisionsTable';
import useAction from '../../../hooks/useAction';
import { getRelease, getRevisions } from '../../../services/releases';
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

function ListReleaseRevisions(props) {
  const classes = useStyles();
  const [fetchedRevisions, fetchRevisions] = useAction(getRevisions);
  const [fetchedRelease, fetchRelease] = useAction(getRelease);
  const [fetchedRevisionData, fetchRevisionData] = useAction(axios.get);
  const [drawerState, setDrawerState] = useState({ open: false, item: {} });
  const [leftRadioCheckedIndex, setLeftRadioCheckedIndex] = useState(1);
  const [leftRevisionData, setLeftRevisionData] = useState(null);
  const [rightRadioCheckedIndex, setRightRadioCheckedIndex] = useState(0);
  const [rightRevisionData, setRightRevisionData] = useState(null);
  const error =
    fetchedRelease.error || fetchedRevisions.error || fetchedRevisionData.error;
  const isLoading = fetchedRelease.loading || fetchedRevisions.loading;
  const revisions = fetchedRevisions.data ? fetchedRevisions.data : [];
  const { releaseName } = props.match.params;

  useEffect(() => {
    fetchRelease(releaseName);
  }, [releaseName]);

  useEffect(() => {
    if (fetchedRelease.data) {
      fetchRevisions(releaseName, 1);
    }
  }, [releaseName, fetchedRelease.data]);

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
    const result = await fetchRevisionData(item.data_url);

    setDrawerState({
      ...drawerState,
      item: result.data.data,
      open: true,
    });
  };

  useEffect(() => {
    const r = revisions[leftRadioCheckedIndex];

    if (r) {
      axios.get(r.data_url).then((result) => {
        setLeftRevisionData(result.data || {});
      });
    }
  }, [revisions, leftRadioCheckedIndex]);

  useEffect(() => {
    const r = revisions[rightRadioCheckedIndex];

    if (r) {
      axios.get(r.data_url).then((result) => {
        setRightRevisionData(result.data || {});
      });
    }
  }, [revisions, rightRadioCheckedIndex]);

  // TODO: Add logic to restore a revision
  const handleRestoreClick = () => {};
  const revisionsCount = revisions.length;
  const columnWidth = CONTENT_MAX_WIDTH / 4;

  const columns = React.useMemo(() => [
    {
      accessorKey: 'timestamp',
      cell: ({ cell }) =>
        formatDistanceStrict(new Date(cell.getValue()), new Date(), {
          addSuffix: true,
        }),
      header: 'Revision Date',
      width: columnWidth,
    },
    {
      header: 'Changed By',
      accessorKey: 'changed_by',
      width: columnWidth,
    },
    {
      header: 'Compare',
      accessorKey: 'compare',
      width: columnWidth,
      cell: ({ row }) => (
        <Fragment>
          <Radio
            variant="red"
            value={row.index}
            disabled={row.index === 0}
            checked={leftRadioCheckedIndex === row.index}
            onChange={handleLeftRadioChange}
          />
          <Radio
            variant="green"
            value={row.index}
            disabled={row.index === revisions.length - 1}
            checked={rightRadioCheckedIndex === row.index}
            onChange={handleRightRadioChange}
          />
        </Fragment>
      ),
    },
    {
      id: 'actions',
      width: columnWidth,
      cell: ({ row }) => (
        <Fragment>
          <Button onClick={handleViewClick(row.original)}>View</Button>
          {row.index > 0 && (
            <Button onClick={handleRestoreClick}>Restore</Button>
          )}
        </Fragment>
      ),
    },
  ]);

  return (
    <Dashboard title={`Release ${releaseName} Revisions`}>
      {error && <ErrorPanel error={error} />}
      {isLoading && (
        <Box style={{ textAlign: 'center' }}>
          <CircularProgress loading />
        </Box>
      )}
      {!isLoading && revisions.length === 1 && (
        <Typography>Role {releaseName} has no revisions</Typography>
      )}
      {!isLoading && revisionsCount > 1 && (
        <Fragment>
          <RevisionsTable data={revisions} columns={columns} />
          {leftRevisionData && rightRevisionData && (
            <DiffRelease
              className={classes.jsDiff}
              firstFilename={`Revision Version ${revisions[leftRadioCheckedIndex].data_version}`}
              secondFilename={`Revision Version ${revisions[rightRadioCheckedIndex].data_version}`}
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
              <code>{JSON.stringify(drawerState.item, null, 2)}</code>
            </pre>
          </Drawer>
        </Fragment>
      )}
    </Dashboard>
  );
}

export default ListReleaseRevisions;
