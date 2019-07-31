import React, { Fragment, useState, useEffect } from 'react';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { makeStyles, withStyles } from '@material-ui/styles';
import { red, green } from '@material-ui/core/colors';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Typography from '@material-ui/core/Typography';
import Radio from '@material-ui/core/Radio';
import Drawer from '@material-ui/core/Drawer';
import { formatDistanceStrict } from 'date-fns';
import Dashboard from '../../../components/Dashboard';
import DataTable from '../../../components/DataTable';
import ErrorPanel from '../../../components/ErrorPanel';
import RuleCard from '../../../components/RuleCard';
import Button from '../../../components/Button';
import DiffRule from '../../../components/DiffRule';
import useAction from '../../../hooks/useAction';
import { getRevisions } from '../../../services/rules';
import { CONTENT_MAX_WIDTH } from '../../../utils/constants';

const useStyles = makeStyles(theme => ({
  radioCell: {
    paddingLeft: 0,
  },
  ruleCard: {
    boxShadow: 'unset',
  },
  tableWrapper: {
    maxHeight: '50%',
    overflowY: 'auto',
  },
  tableHeadCell: {
    position: 'sticky',
    top: 0,
    backgroundColor: theme.palette.common.white,
    zIndex: theme.zIndex.appBar,
  },
  drawerPaper: {
    maxWidth: CONTENT_MAX_WIDTH,
    margin: '0 auto',
  },
}));
const GreenRadio = withStyles({
  root: {
    '&$checked': {
      color: green[600],
    },
  },
  checked: {},
})(props => <Radio color="default" {...props} />);
const RedRadio = withStyles({
  root: {
    '&$checked': {
      color: red[600],
    },
  },
  checked: {},
})(props => <Radio color="default" {...props} />);

function ListRuleRevisions(props) {
  const classes = useStyles();
  const [drawerState, setDrawerState] = useState({ open: false, item: {} });
  const [leftRadioCheckedIndex, setLeftRadioCheckedIndex] = useState(1);
  const [rightRadioCheckedIndex, setRightRadioCheckedIndex] = useState(0);
  const [fetchedRevisions, fetchRevisions] = useAction(getRevisions);
  const { ruleId } = props.match.params;
  // eslint-disable-next-line prefer-destructuring
  const error = fetchedRevisions.error;
  const isLoading = fetchedRevisions.loading;
  const revisions = fetchedRevisions.data
    ? fetchedRevisions.data.data.rules
    : [];
  const headers = ['Revision Date', 'Changed By', 'Compare', ''];

  useEffect(() => {
    fetchRevisions(ruleId);
  }, []);

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
    setDrawerState({
      ...drawerState,
      item,
      open: true,
    });
  };

  // TODO: Add logic to restore a revision
  const handleRestoreClick = () => {};
  const renderRow = (row, index) => (
    <TableRow key={row.timestamp}>
      <TableCell title={new Date(row.timestamp)}>
        {formatDistanceStrict(new Date(row.timestamp), new Date(), {
          addSuffix: true,
        })}
      </TableCell>
      <TableCell>{row.changed_by}</TableCell>
      <TableCell className={classes.radioCell}>
        <RedRadio
          value={index}
          disabled={index === 0}
          checked={leftRadioCheckedIndex === index}
          onChange={handleLeftRadioChange}
        />
        <GreenRadio
          value={index}
          disabled={index === revisions.length - 1}
          checked={rightRadioCheckedIndex === index}
          onChange={handleRightRadioChange}
        />
      </TableCell>
      <TableCell>
        <Button onClick={handleViewClick(row)}>View</Button>
        {index > 0 && <Button onClick={handleRestoreClick}>Restore</Button>}
      </TableCell>
    </TableRow>
  );

  return (
    <Dashboard title={`Rule ${ruleId} Revisions`}>
      {error && <ErrorPanel fixed error={error} />}
      {isLoading && <Spinner loading />}
      {!isLoading && revisions.length === 1 && (
        <Typography>Rule {ruleId} has no revisions</Typography>
      )}
      {!isLoading && revisions.length > 1 && (
        <Fragment>
          <div className={classes.tableWrapper}>
            <DataTable
              size="small"
              headers={headers}
              renderRow={renderRow}
              items={revisions}
              tableHeadCellProps={{ className: classes.tableHeadCell }}
            />
          </div>
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
        </Fragment>
      )}
    </Dashboard>
  );
}

export default ListRuleRevisions;
