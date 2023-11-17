import React, { Fragment, useState, useEffect } from 'react';
import { Column } from 'react-virtualized';
import { clone } from 'ramda';
import { stringify } from 'qs';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { makeStyles } from '@material-ui/styles';
import Typography from '@material-ui/core/Typography';
import Drawer from '@material-ui/core/Drawer';
import { formatDistanceStrict } from 'date-fns';
import Dashboard from '../../../components/Dashboard';
import DialogAction from '../../../components/DialogAction';
import ErrorPanel from '../../../components/ErrorPanel';
import RuleCard from '../../../components/RuleCard';
import Radio from '../../../components/Radio';
import Button from '../../../components/Button';
import DiffRule from '../../../components/DiffRule';
import RevisionsTable from '../../../components/RevisionsTable';
import useAction from '../../../hooks/useAction';
import {
  getRevisions,
  addScheduledChange,
  getScheduledChanges,
} from '../../../services/rules';
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
const changesProps = {
  ruleId: 0,
  priority: 0,
  scheduledBy: '',
  allSignOffs: {},
  dataVersion: 0
};

function ListRuleRevisions(props) {
  const classes = useStyles();
  const rulesFilter =
    props.location.state && props.location.state.rulesFilter
      ? props.location.state.rulesFilter
      : [];
  const [drawerState, setDrawerState] = useState({ open: false, item: {} });
  const [leftRadioCheckedIndex, setLeftRadioCheckedIndex] = useState(1);
  const [rightRadioCheckedIndex, setRightRadioCheckedIndex] = useState(0);
  const [rulesWithChangesProps, setRulesWithChangesProps] = useState([]);
  const [ruleHistory, setRuleHistory] = useState([]);
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [fetchedRevisions, fetchRevisions] = useAction(getRevisions);
  const [scheduledChanges, fetchScheduledChanges] = useAction(
    getScheduledChanges
  );
  const addSC = useAction(addScheduledChange)[1];
  const { ruleId } = props.match.params;
  // eslint-disable-next-line prefer-destructuring
  const error = fetchedRevisions.error;
  const isLoading = fetchedRevisions.loading;
  const revisions = fetchedRevisions.data
    ? fetchedRevisions.data.data.rules
    : [];
  const revisionsCount = revisions.length;
  const redirectWithRulesFilter = hashFilter => {
    const [product, channel] = rulesFilter;
    const query = stringify({ product, channel }, { addQueryPrefix: true });

    props.history.push(`/rules${query}#${hashFilter}`);
  };

  useEffect(() => {
    fetchRevisions(ruleId);
    fetchScheduledChanges(true);
  }, [ruleId]);

  useEffect(() => {
    if (scheduledChanges.data) {
      const tempRulesWithChangesProps = [];
      const sc = scheduledChanges.data.data.scheduled_changes;
      console.log(sc[0])
      for (let i = 0; i < sc.length; i += 1) {
        tempRulesWithChangesProps.push({
          ...changesProps,
          ruleId: sc[i].rule_id,
          priority: sc[i].priority,
          scheduledBy: sc[i].scheduled_by,
          allSignOffs: sc[i].signoffs,
          dataVersion: sc[i].data_version,
          when: sc[i].when
        });
      }

      setRulesWithChangesProps(tempRulesWithChangesProps);
    }
  }, [scheduledChanges.data]);

  useEffect(() => {
    if (ruleId && rulesWithChangesProps.length > 0) {
      const tempRuleHistory = [];

      for (let i = 0; i < rulesWithChangesProps.length; i += 1) {
        if (rulesWithChangesProps[i].ruleId === Number(ruleId)) {
          tempRuleHistory.push(rulesWithChangesProps[i]);
        }
      }

      setRuleHistory(tempRuleHistory);
    }
  }, [ruleId, rulesWithChangesProps]);

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

  const handleViewClick = item => () => {
    // // console.log(item)
    console.log(ruleHistory)
    setDrawerState({
      ...drawerState,
      item,
      open: true,
    });
  };

  const handleRestoreClick = revision => () =>
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
      when: new Date().getTime() + 30000,
      data_version: revisions[0].data_version,
      ...ruleData,
    });

    if (error) {
      throw error;
    }

    return data.data.sc_id;
  };

  const handleDialogClose = () => setDialogState(DIALOG_ACTION_INITIAL_STATE);
  const handleDialogActionComplete = scId =>
    redirectWithRulesFilter(`scId=${scId}`);
  const handleDialogError = error => setDialogState({ ...dialogState, error });
  const columnWidth = CONTENT_MAX_WIDTH / 4;

  return (
    <Dashboard title={`Rule ${ruleId} Revisions`}>
      {error && <ErrorPanel fixed error={error} />}
      {isLoading && <Spinner loading />}
      {!isLoading && revisions.length === 1 && (
        <Typography>Rule {ruleId} has no revisions</Typography>
      )}
      {!isLoading && revisionsCount > 1 && (
        <Fragment>
          <RevisionsTable
            rowCount={revisionsCount}
            rowGetter={({ index }) => revisions[index]}>
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
                  <Radio
                    variant="green"
                    value={rowIndex}
                    disabled={rowIndex === revisions.length - 1}
                    checked={rightRadioCheckedIndex === rowIndex}
                    onChange={handleRightRadioChange}
                  />
                </Fragment>
              )}
            />
            <Column
              dataKey="actions"
              width={columnWidth}
              cellRenderer={({ rowData, rowIndex }) => (
                <Fragment>
                  <Button onClick={handleViewClick(rowData)}>View</Button>
                  {rowIndex > 0 && (
                    <Button onClick={handleRestoreClick(rowData)}>
                      Restore
                    </Button>
                  )}
                </Fragment>
              )}
            />
          </RevisionsTable>
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
            onClose={handleDrawerClose}>
            <RuleCard
              className={classes.ruleCard}
              readOnly
              rule={drawerState.item}
            />
          </Drawer>
          <p>THIS IS A TEST PARAGRAPH</p>
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
