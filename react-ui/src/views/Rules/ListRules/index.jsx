import React, { Fragment, useEffect, useState, useMemo } from 'react';
import { stringify, parse } from 'qs';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import ErrorPanel from '@mozilla-frontend-infra/components/ErrorPanel';
import { makeStyles } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import TablePagination from '@material-ui/core/TablePagination';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import MenuItem from '@material-ui/core/MenuItem';
import PlusIcon from 'mdi-react/PlusIcon';
import Dashboard from '../../../components/Dashboard';
import RuleCard from '../../../components/RuleCard';
import Link from '../../../utils/Link';
import useAction from '../../../hooks/useAction';
import {
  getProducts,
  getChannels,
  getRules,
  getScheduledChanges,
} from '../../../utils/Rules';
import { RULES_ROWS_PER_PAGE } from '../../../utils/constants';

const ALL = 'all';
const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  options: {
    display: 'flex',
    justifyContent: 'space-between',
  },
  dropdown: {
    minWidth: 200,
    marginBottom: theme.spacing(2),
  },
  tablePaginationToolbar: {
    paddingLeft: 'unset',
  },
  tablePaginationSpacer: {
    flex: 'unset',
  },
}));

function ListRules(props) {
  const classes = useStyles();
  const query = parse(props.location.search.slice(1));
  const productChannelSeparator = ' : ';
  const [rulesWithScheduledChanges, setRulesWithScheduledChanges] = useState(
    []
  );
  const [tablePage, setTablePage] = useState(0);
  const [productChannelOptions, setProductChannelOptions] = useState([]);
  const searchQueries = query.product ? [query.product, query.channel] : null;
  const [productChannelFilter, setProductChannelFilter] = useState(
    searchQueries
      ? searchQueries.filter(Boolean).join(productChannelSeparator)
      : ALL
  );
  const [products, fetchProducts] = useAction(getProducts);
  const [channels, fetchChannels] = useAction(getChannels);
  const [rules, fetchRules] = useAction(getRules);
  const [scheduledChanges, fetchScheduledChanges] = useAction(
    getScheduledChanges
  );
  const isLoading = products.loading || channels.loading || rules.loading;
  const error =
    products.error || channels.error || rules.error || scheduledChanges.error;
  const handleFilterChange = ({ target: { value } }) => {
    const [product, channel] = value.split(productChannelSeparator);
    const query =
      value !== ALL
        ? stringify({ product, channel }, { addQueryPrefix: true })
        : '';

    props.history.push(`/rules${query}`);

    setProductChannelFilter(value);
    setTablePage(0);
  };

  const pairExists = (product, channel) =>
    rules.data &&
    rules.data.data.rules.some(
      rule => rule.product === product && rule.channel === channel
    );

  useEffect(() => {
    if (!products.data || !channels.data || !rules.data) {
      return;
    }

    const prods = products.data.data.product;
    const chs = channels.data.data.channel;
    const options = [];

    prods.forEach(product => {
      options.push(product);

      chs.forEach(channel => {
        if (!channel.endsWith('*') && pairExists(product, channel)) {
          options.push(`${product}${productChannelSeparator}${channel}`);
        }
      });
    });

    setProductChannelOptions(options.sort());
  }, [products.data, channels.data, rules.data]);

  useEffect(() => {
    Promise.all([
      fetchScheduledChanges(),
      fetchRules(),
      fetchProducts(),
      fetchChannels(),
    ]).then(([sc, r]) => {
      if (!sc.data || !r.data) {
        return;
      }

      const scheduledChanges = sc.data.data.scheduled_changes;
      const { rules } = r.data.data;
      const rulesWithScheduledChanges = rules.map(rule => {
        const sc = scheduledChanges.find(sc => rule.rule_id === sc.rule_id);

        if (sc) {
          Object.assign(rule, { scheduledChange: sc });
          Object.assign(rule.scheduledChange, {
            when: new Date(rule.scheduledChange.when),
          });
        }

        return rule;
      });

      scheduledChanges.forEach(sc => {
        if (sc.change_type === 'insert') {
          const rule = { scheduledChange: sc };

          Object.assign(rule, { scheduledChange: sc });
          Object.assign(rule.scheduledChange, {
            when: new Date(rule.scheduledChange.when),
          });

          rulesWithScheduledChanges.push(rule);
        }
      });

      // Rules are sorted by priority. Rules that are
      // pending (ie: still just a Scheduled Change) will be inserted based
      // on the priority in the Scheduled Change. Rules that have Scheduled
      // updates or deletes will remain sorted on their current priority
      // because it's more important to make it easy to assess current state
      // than future state.
      const sortedRules = rulesWithScheduledChanges.sort((ruleA, ruleB) => {
        const priorityA =
          ruleA.priority === null || ruleA.priority === undefined
            ? ruleA.scheduledChange.priority
            : ruleA.priority;
        const priorityB =
          ruleB.priority === null || ruleB.priority === undefined
            ? ruleB.scheduledChange.priority
            : ruleB.priority;

        return priorityB - priorityA;
      });

      setRulesWithScheduledChanges(sortedRules);
    });
  }, []);
  const filteredRulesWithScheduledChanges = useMemo(
    () =>
      productChannelFilter === ALL
        ? rulesWithScheduledChanges
        : rulesWithScheduledChanges.filter(rule => {
            const [productFilter, channelFilter] = searchQueries;
            const ruleProduct =
              rule.product ||
              (rule.scheduledChange && rule.scheduledChange.product);
            const ruleChannel =
              rule.channel ||
              (rule.scheduledChange && rule.scheduledChange.channel);

            if (ruleProduct !== productFilter) {
              return false;
            }

            if (
              channelFilter &&
              ruleChannel.replace('*', '') !== channelFilter
            ) {
              return false;
            }

            return true;
          }),
    [productChannelFilter, rulesWithScheduledChanges]
  );
  const paginatedRules = filteredRulesWithScheduledChanges.slice(
    tablePage * RULES_ROWS_PER_PAGE,
    tablePage * RULES_ROWS_PER_PAGE + RULES_ROWS_PER_PAGE
  );
  const pagination = (
    <TablePagination
      classes={{
        toolbar: classes.tablePaginationToolbar,
        spacer: classes.tablePaginationSpacer,
      }}
      component="div"
      rowsPerPageOptions={[]}
      count={filteredRulesWithScheduledChanges.length}
      onChangePage={(e, page) => setTablePage(page)}
      page={tablePage}
      rowsPerPage={RULES_ROWS_PER_PAGE}
    />
  );

  return (
    <Dashboard title="Rules">
      {isLoading && <Spinner loading />}
      {error && <ErrorPanel error={error} />}
      {!isLoading && productChannelOptions && (
        <Fragment>
          <div className={classes.options}>
            {pagination}
            <TextField
              className={classes.dropdown}
              select
              label={`Product${productChannelSeparator}Channel`}
              value={productChannelFilter}
              onChange={handleFilterChange}>
              <MenuItem value="all">All Rules</MenuItem>
              {productChannelOptions.map(option => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
          </div>
          {paginatedRules && (
            <Grid container spacing={4}>
              {paginatedRules.map(rule => (
                <Grid
                  key={`${rule.product}-${rule.channel}-${rule.rule_id}`}
                  item
                  xs={12}>
                  <RuleCard key={rule.rule_id} rule={rule} />
                </Grid>
              ))}
            </Grid>
          )}
          {pagination}
          <Link to="/rules/create">
            <Tooltip title="Add Rule">
              <Fab color="primary" className={classes.fab}>
                <PlusIcon />
              </Fab>
            </Tooltip>
          </Link>
        </Fragment>
      )}
    </Dashboard>
  );
}

export default ListRules;
