import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';
import Drawer from '@material-ui/core/Drawer';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/styles';
import { formatDistanceStrict } from 'date-fns';
import { stringify } from 'qs';
import { clone } from 'ramda';
import React, { Fragment, useEffect, useState } from 'react';
import Button from '../../../components/Button';
import Dashboard from '../../../components/Dashboard';
import DialogAction from '../../../components/DialogAction';
import DiffRule from '../../../components/DiffRule';
import ErrorPanel from '../../../components/ErrorPanel';
import Radio from '../../../components/Radio';
import RevisionsTable from '../../../components/RevisionsTable';
import RuleCard from '../../../components/RuleCard';
import useAction from '../../../hooks/useAction';
import { addScheduledChange, getRevisions } from '../../../services/rules';
import {
  CONTENT_MAX_WIDTH,
  DIALOG_ACTION_INITIAL_STATE,
} from '../../../utils/constants';

const useStyles = makeStyles({
  radioCell: {
    paddingLeft: 0,
  },
  ruleCard: {
    boxShadow: 'unset',
  },
  drawerPaper: {
    maxWidth: CONTENT_MAX_WIDTH,
    margin: '0 auto',
  },
});

function ListRuleRevisions(props) {
  const classes = useStyles();
  const rulesFilter = props.location.state?.rulesFilter
    ? props.location.state.rulesFilter
    : [];
  const [drawerState, setDrawerState] = useState({ open: false, item: {} });
  const [leftRadioCheckedIndex, setLeftRadioCheckedIndex] = useState(1);
  const [rightRadioCheckedIndex, setRightRadioCheckedIndex] = useState(0);
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [fetchedRevisions, fetchRevisions] = useAction(getRevisions);
  const addSC = useAction(addScheduledChange)[1];
  const { ruleId } = props.match.params;
  const error = fetchedRevisions.error;
  const isLoading = fetchedRevisions.loading;
  const revisions = fetchedRevisions.data
    ? fetchedRevisions.data.data.rules
    : [];
  const revisionsCount = revisions.length;
  const redirectWithRulesFilter = (hashFilter) => {
    const [product, channel] = rulesFilter;
    const query = stringify({ product, channel }, { addQueryPrefix: true });

    props.history.push(`/rules${query}#${hashFilter}`);
  };

  useEffect(() => {
    fetchRevisions(ruleId);
  }, [ruleId]);

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

  const handleViewClick = (item) => () => {
    setDrawerState({
      ...drawerState,
      item,
      open: true,
    });
  };

  const handleRestoreClick = (revision) => () =>
    setDialogState({
      ...dialogState,
      open: true,
      body: `Rule ${
        revision.alias ? revision.alias : revision.rule_id
      } will be restored to data version ${revision.data_version}.`,
      title: 'Restore Rule?',
      confirmText: 'Restore',
      item: revision,
    });
  const handleDialogSubmit = async () => {
    const ruleData = clone(dialogState.item);

    // We only want the actual rule data from the old revision,
    // not the metadata.
    delete ruleData.change_id;
    delete ruleData.changed_by;
    delete ruleData.timestamp;
    delete ruleData.data_version;
    const { error, data } = await addSC({
      change_type: 'update',
      when: Date.now() + 30000,
      data_version: revisions[0].data_version,
      ...ruleData,
    });

    if (error) {
      throw error;
    }

    return data.data.sc_id;
  };

  const handleDialogClose = () => setDialogState(DIALOG_ACTION_INITIAL_STATE);
  const handleDialogActionComplete = (scId) =>
    redirectWithRulesFilter(`scId=${scId}`);
  const handleDialogError = (error) =>
    setDialogState({ ...dialogState, error });
  const columnWidth = CONTENT_MAX_WIDTH / 4;
  const columns = [
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
            <Button onClick={handleRestoreClick(row.original)}>Restore</Button>
          )}
        </Fragment>
      ),
    },
  ];

  return (
    <Dashboard title={`Rule ${ruleId} Revisions`}>
      {error && <ErrorPanel error={error} />}
      {isLoading && (
        <Box style={{ textAlign: 'center' }}>
          <CircularProgress loading />
        </Box>
      )}
      {!isLoading && revisions.length === 1 && (
        <Typography>Rule {ruleId} has no revisions</Typography>
      )}
      {!isLoading && revisionsCount > 1 && (
        <Fragment>
          <RevisionsTable data={revisions} columns={columns} />
          <br />
          <br />
          {revisions[leftRadioCheckedIndex] &&
            revisions[rightRadioCheckedIndex] && (
              <DiffRule
                firstRule={revisions[leftRadioCheckedIndex]}
                secondRule={revisions[rightRadioCheckedIndex]}
              />
            )}
          <Drawer
            classes={{ paper: classes.drawerPaper }}
            anchor="bottom"
            open={drawerState.open}
            onClose={handleDrawerClose}
          >
            <RuleCard
              className={classes.ruleCard}
              readOnly
              rule={drawerState.item}
            />
          </Drawer>
        </Fragment>
      )}
      <DialogAction
        open={dialogState.open}
        title={dialogState.title}
        body={dialogState.body}
        confirmText={dialogState.confirmText}
        onSubmit={handleDialogSubmit}
        onError={handleDialogError}
        error={dialogState.error}
        onComplete={handleDialogActionComplete}
        onClose={handleDialogClose}
      />
    </Dashboard>
  );
}

export default ListRuleRevisions;
