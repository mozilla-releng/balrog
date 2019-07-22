import React, { Fragment, useEffect, useState, useMemo } from 'react';
import { stringify, parse } from 'qs';
import { addSeconds } from 'date-fns';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { makeStyles, useTheme } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import PlusIcon from 'mdi-react/PlusIcon';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import RuleCard from '../../../components/RuleCard';
import DialogAction from '../../../components/DialogAction';
import DateTimePicker from '../../../components/DateTimePicker';
import VariableSizeList from '../../../components/VariableSizeList';
import Link from '../../../utils/Link';
import getDiffedProperties from '../../../utils/getDiffedProperties';
import useAction from '../../../hooks/useAction';
import {
  getProducts,
  getChannels,
  getRules,
  getScheduledChanges,
  getScheduledChangeByRuleId,
  deleteRule,
} from '../../../services/rules';
import { getRequiredSignoffs } from '../../../services/requiredSignoffs';
import { ruleMatchesRequiredSignoff } from '../../../utils/requiredSignoffs';
import {
  RULE_DIFF_PROPERTIES,
  DIALOG_ACTION_INITIAL_STATE,
  OBJECT_NAMES,
  SNACKBAR_INITIAL_STATE,
} from '../../../utils/constants';
import Snackbar from '../../../components/Snackbar';

const ALL = 'all';
const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  options: {
    display: 'flex',
    justifyContent: 'flex-end',
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
  ruleCard: {
    margin: theme.spacing.unit,
  },
}));

function ListRules(props) {
  const classes = useStyles();
  const theme = useTheme();
  const { search, hash } = props.location;
  const query = parse(search.slice(1));
  const hashQuery = parse(hash.replace('#', ''));
  const productChannelSeparator = ' : ';
  const [snackbarState, setSnackbarState] = useState(SNACKBAR_INITIAL_STATE);
  const [ruleIdHash, setRuleIdHash] = useState(null);
  const [scheduledIdHash, setScheduledIdHash] = useState(null);
  const [rulesWithScheduledChanges, setRulesWithScheduledChanges] = useState(
    []
  );
  const [productChannelOptions, setProductChannelOptions] = useState([]);
  const searchQueries = query.product ? [query.product, query.channel] : null;
  const [productChannelFilter, setProductChannelFilter] = useState(
    searchQueries
      ? searchQueries.filter(Boolean).join(productChannelSeparator)
      : ALL
  );
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [scheduleDeleteDate, setScheduleDeleteDate] = useState(
    addSeconds(new Date(), -30)
  );
  const [dateTimePickerError, setDateTimePickerError] = useState(null);
  const [scrollToRow, setScrollToRow] = useState(null);
  const [products, fetchProducts] = useAction(getProducts);
  const [channels, fetchChannels] = useAction(getChannels);
  const [rules, fetchRules] = useAction(getRules);
  const [scheduledChanges, fetchScheduledChanges] = useAction(
    getScheduledChanges
  );
  const fetchRequiredSignoffs = useAction(getRequiredSignoffs)[1];
  const delRule = useAction(deleteRule)[1];
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
  };

  const handleSnackbarOpen = ({ message, variant = 'success' }) => {
    setSnackbarState({ message, variant, open: true });
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarState(SNACKBAR_INITIAL_STATE);
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
      fetchRequiredSignoffs(OBJECT_NAMES.PRODUCT_REQUIRED_SIGNOFF),
      fetchProducts(),
      fetchChannels(),
    ]).then(([sc, r, rs]) => {
      if (!sc.data || !r.data || !rs.data) {
        return;
      }

      const scheduledChanges = sc.data.data.scheduled_changes;
      const requiredSignoffs = rs.data.data.required_signoffs;
      const { rules } = r.data.data;
      const rulesWithScheduledChanges = rules.map(rule => {
        const sc = scheduledChanges.find(sc => rule.rule_id === sc.rule_id);
        const returnedRule = Object.assign({}, rule);

        if (sc) {
          returnedRule.scheduledChange = sc;
          returnedRule.scheduledChange.when = new Date(
            returnedRule.scheduledChange.when
          );
        }

        returnedRule.requiredSignoffs = {};
        requiredSignoffs.forEach(rs => {
          if (ruleMatchesRequiredSignoff(rule, rs)) {
            returnedRule.requiredSignoffs[rs.role] = rs.signoffs_required;
          }
        });

        return returnedRule;
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
  const handleDateTimePickerError = error => {
    setDateTimePickerError(error);
  };

  const handleDateTimeChange = date => {
    setScheduleDeleteDate(date);
    setDateTimePickerError(null);
  };

  const handleDialogError = error => {
    setDialogState({ ...dialogState, error });
  };

  const dialogBody =
    dialogState.item &&
    (Object.keys(dialogState.item.requiredSignoffs).length > 0 ? (
      <DateTimePicker
        disablePast
        inputVariant="outlined"
        fullWidth
        label="When"
        onError={handleDateTimePickerError}
        helperText={
          dateTimePickerError ||
          (scheduleDeleteDate < new Date() ? 'Scheduled for ASAP' : undefined)
        }
        onDateTimeChange={handleDateTimeChange}
        value={scheduleDeleteDate}
      />
    ) : (
      `This will delete rule ${dialogState.item.rule_id}.`
    ));
  const filteredRulesCount = filteredRulesWithScheduledChanges.length;
  const handleRuleDelete = rule => {
    setDialogState({
      ...dialogState,
      open: true,
      title: 'Delete Rule?',
      confirmText: 'Delete',
      item: rule,
    });
  };

  const handleDialogClose = () => {
    setDialogState(DIALOG_ACTION_INITIAL_STATE);
  };

  const handleDialogComplete = result => {
    if (typeof result === 'number') {
      // The rule was directly deleted, just remove it.
      setRulesWithScheduledChanges(
        rulesWithScheduledChanges.filter(i => i.rule_id !== result)
      );
      handleSnackbarOpen({
        message: `Rule ${result} deleted`,
      });
    } else {
      // A change was scheduled, we need to update the card
      // to reflect that.
      setRulesWithScheduledChanges(
        rulesWithScheduledChanges.map(r => {
          if (r.rule_id !== result.rule_id) {
            return r;
          }

          const newRule = { ...r };

          newRule.scheduledChange = result;

          return newRule;
        })
      );
      handleSnackbarOpen({
        message: `Rule ${result.rule_id} successfully scheduled`,
      });
    }

    handleDialogClose();
  };

  const handleDialogSubmit = async () => {
    const dialogRule = dialogState.item;
    const { error } = await delRule({
      ruleId: dialogRule.rule_id,
      dataVersion: dialogRule.data_version,
    });

    if (error) {
      throw error;
    }

    if (Object.keys(dialogRule.requiredSignoffs).length > 0) {
      return (await getScheduledChangeByRuleId(dialogRule.rule_id)).data
        .scheduled_changes[0];
    }

    return dialogRule.rule_id;
  };

  const getRowHeight = ({ index }) => {
    const rule = filteredRulesWithScheduledChanges[index];
    const hasScheduledChanges = Boolean(rule.scheduledChange);
    // actions row
    let height = 7 * theme.spacing(1);

    if (hasScheduledChanges && rule.scheduledChange.change_type === 'insert') {
      const diffedProperties = getDiffedProperties(
        RULE_DIFF_PROPERTIES,
        rule,
        rule.scheduledChange
      );

      // diff viewer
      height += diffedProperties.length * 21 + theme.spacing(8);
    } else {
      // card title
      height += theme.spacing(7);

      // != checks for both null and undefined
      const keys = Object.keys(rule).filter(key => rule[key] != null);
      const firstColumn = ['mapping', 'fallbackMapping', 'backgroundRate'];
      const secondColumn = ['data_version', 'rule_id'];
      const thirdColumn = [
        'version',
        'buildID',
        'buildTarget',
        'locale',
        'distribution',
        'distVersion',
        'osVersion',
        'instructionSet',
        'memory',
        'headerArchitecture',
        'mig64',
        'jaws',
      ];
      // card rows
      const rows = Math.max(
        keys.filter(key => firstColumn.includes(key)).length,
        keys.filter(key => secondColumn.includes(key)).length,
        keys.filter(key => thirdColumn.includes(key)).length
      );

      height += rows * theme.spacing(8);

      // row with comment
      // (max 2 lines of comments otherwise we display a scroller)
      if (rule.comment) {
        height += theme.spacing(10);
      }

      if (hasScheduledChanges) {
        // divider + row with the chip label
        height += theme.spacing(6);

        if (rule.scheduledChange.change_type === 'delete') {
          // row with "all properties will be deleted"
          height += theme.spacing(5);
        } else if (rule.scheduledChange.change_type === 'update') {
          const diffedProperties = getDiffedProperties(
            RULE_DIFF_PROPERTIES,
            rule,
            rule.scheduledChange
          );

          // diff viewer
          height += diffedProperties.length * 21 + theme.spacing(5);
        }
      }
    }

    // space below the card (margin)
    height += theme.spacing(6);

    return height;
  };

  const Row = ({ index, style }) => {
    const rule = filteredRulesWithScheduledChanges[index];

    return (
      <div
        key={
          rule.rule_id
            ? rule.rule_id
            : Object.values(rule.scheduledChange).join('-')
        }
        style={style}>
        <RuleCard
          className={classes.ruleCard}
          key={rule.rule_id}
          rule={rule}
          onRuleDelete={handleRuleDelete}
        />
      </div>
    );
  };

  useEffect(() => {
    if (filteredRulesCount) {
      if (hashQuery.ruleId && hashQuery.ruleId !== ruleIdHash) {
        const ruleId = Number(hashQuery.ruleId);

        if (ruleId) {
          const itemNumber = filteredRulesWithScheduledChanges
            .map(rule => rule.rule_id)
            .indexOf(ruleId);

          setScrollToRow(itemNumber);
          setRuleIdHash(hashQuery.ruleId);
        }
      } else if (hashQuery.scId && hashQuery.scId !== scheduledIdHash) {
        const scId = Number(hashQuery.scId);

        if (scId) {
          const itemNumber = filteredRulesWithScheduledChanges
            .map(rule => rule.scheduledChange && rule.scheduledChange.sc_id)
            .indexOf(scId);

          setScrollToRow(itemNumber);
          setScheduledIdHash(hashQuery.scId);
        }
      }
    }
  }, [hashQuery, filteredRulesCount]);

  return (
    <Dashboard title="Rules">
      {isLoading && <Spinner loading />}
      {error && <ErrorPanel fixed error={error} />}
      {!isLoading && productChannelOptions && (
        <Fragment>
          <div className={classes.options}>
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
          {filteredRulesWithScheduledChanges && (
            <Fragment>
              <VariableSizeList
                rowRenderer={Row}
                scrollToRow={scrollToRow}
                rowHeight={getRowHeight}
                rowCount={filteredRulesCount}
              />
            </Fragment>
          )}
          <Link to="/rules/create">
            <Tooltip title="Add Rule">
              <Fab color="primary" className={classes.fab}>
                <PlusIcon />
              </Fab>
            </Tooltip>
          </Link>
        </Fragment>
      )}
      <DialogAction
        open={dialogState.open}
        title={dialogState.title}
        body={dialogBody}
        confirmText={dialogState.confirmText}
        onSubmit={handleDialogSubmit}
        onError={handleDialogError}
        error={dialogState.error}
        onComplete={handleDialogComplete}
        onClose={handleDialogClose}
      />
      <Snackbar onClose={handleSnackbarClose} {...snackbarState} />
    </Dashboard>
  );
}

export default ListRules;
