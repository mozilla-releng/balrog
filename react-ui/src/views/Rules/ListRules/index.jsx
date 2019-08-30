import React, { Fragment, useEffect, useState, useMemo, useRef } from 'react';
import classNames from 'classnames';
import { stringify, parse } from 'qs';
import { addSeconds } from 'date-fns';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { makeStyles, useTheme } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
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
  addScheduledChange,
  deleteScheduledChange,
  deleteRule,
} from '../../../services/rules';
import { getRequiredSignoffs } from '../../../services/requiredSignoffs';
import { makeSignoff, revokeSignoff } from '../../../services/signoffs';
import { getUserInfo } from '../../../services/users';
import { ruleMatchesRequiredSignoff } from '../../../utils/requiredSignoffs';
import {
  RULE_DIFF_PROPERTIES,
  DIALOG_ACTION_INITIAL_STATE,
  OBJECT_NAMES,
  SNACKBAR_INITIAL_STATE,
} from '../../../utils/constants';
import { withUser } from '../../../utils/AuthContext';
import remToPx from '../../../utils/remToPx';
import elementsHeight from '../../../utils/elementsHeight';
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
    margin: theme.spacing(1),
  },
  ruleCardSelected: {
    border: `2px solid ${theme.palette.primary.light}`,
  },
}));

function ListRules(props) {
  const classes = useStyles();
  const theme = useTheme();
  const username = (props.user && props.user.email) || '';
  const { search, hash } = props.location;
  const query = parse(search.slice(1));
  const hashQuery = parse(hash.replace('#', ''));
  const {
    body1TextHeight,
    body2TextHeight,
    subtitle1TextHeight,
    buttonHeight,
    signoffSummarylistSubheaderTextHeight,
  } = elementsHeight(theme);
  const productChannelSeparator = ' : ';
  const [snackbarState, setSnackbarState] = useState(SNACKBAR_INITIAL_STATE);
  const [ruleIdHash, setRuleIdHash] = useState(null);
  const [scheduledIdHash, setScheduledIdHash] = useState(null);
  const [rulesWithScheduledChanges, setRulesWithScheduledChanges] = useState(
    []
  );
  const [productChannelOptions, setProductChannelOptions] = useState([]);
  const searchQueries = query.product ? [query.product, query.channel] : null;
  const [productChannelFilter, setProductChannelFilter] = useState(ALL);
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [scheduleDeleteDate, setScheduleDeleteDate] = useState(
    addSeconds(new Date(), -30)
  );
  const [dateTimePickerError, setDateTimePickerError] = useState(null);
  const [scrollToRow, setScrollToRow] = useState(null);
  const [roles, setRoles] = useState([]);
  const [signoffRole, setSignoffRole] = useState('');
  const ruleListRef = useRef(null);
  const [products, fetchProducts] = useAction(getProducts);
  const [channels, fetchChannels] = useAction(getChannels);
  const [rules, fetchRules] = useAction(getRules);
  const [scheduledChanges, fetchScheduledChanges] = useAction(
    getScheduledChanges
  );
  const fetchRequiredSignoffs = useAction(getRequiredSignoffs)[1];
  const delRule = useAction(deleteRule)[1];
  const scheduleDelRule = useAction(addScheduledChange)[1];
  const delSC = useAction(deleteScheduledChange)[1];
  const [signoffAction, signoff] = useAction(props =>
    makeSignoff({ type: 'rules', ...props })
  );
  const [revokeAction, revoke] = useAction(props =>
    revokeSignoff({ type: 'rules', ...props })
  );
  const [rolesAction, fetchRoles] = useAction(getUserInfo);
  const isLoading = products.loading || channels.loading || rules.loading;
  const error =
    products.error ||
    channels.error ||
    rules.error ||
    rolesAction.error ||
    scheduledChanges.error ||
    revokeAction.error ||
    (roles.length === 1 && signoffAction.error);
  const handleFilterChange = ({ target: { value } }) => {
    const [product, channel] = value.split(productChannelSeparator);
    const query =
      value !== ALL
        ? stringify({ product, channel }, { addQueryPrefix: true })
        : '';

    props.history.push(`/rules${query}`);

    setProductChannelFilter(value);
  };

  const handleSignoffRoleChange = ({ target: { value } }) =>
    setSignoffRole(value);
  const handleSnackbarOpen = ({ message, variant = 'success' }) => {
    setSnackbarState({ message, variant, open: true });
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarState(SNACKBAR_INITIAL_STATE);
  };

  const isScheduledInsert = rule =>
    rule.scheduledChange && rule.scheduledChange.change_type === 'insert';
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

        returnedRule.required_signoffs = {};
        requiredSignoffs.forEach(rs => {
          if (ruleMatchesRequiredSignoff(rule, rs)) {
            returnedRule.required_signoffs[rs.role] = rs.signoffs_required;
          }
        });

        return returnedRule;
      });

      scheduledChanges.forEach(sc => {
        if (sc.change_type === 'insert') {
          const rule = { scheduledChange: sc };

          Object.assign(rule, {
            scheduledChange: sc,
            required_signoffs: sc.required_signoffs,
          });
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

  useEffect(() => {
    if (username) {
      fetchRoles(username).then(userInfo => {
        const roleList =
          (userInfo.data && Object.keys(userInfo.data.data.roles)) || [];

        setRoles(roleList);

        if (roleList.length > 0) {
          setSignoffRole(roleList[0]);
        }
      });
    }
  }, [username]);

  useEffect(() => {
    setProductChannelFilter(
      searchQueries
        ? searchQueries.filter(Boolean).join(productChannelSeparator)
        : ALL
    );
  }, [searchQueries]);

  const filteredRulesWithScheduledChanges = useMemo(
    () =>
      productChannelFilter === ALL || !searchQueries
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
    [searchQueries, productChannelFilter, rulesWithScheduledChanges]
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

  const handleDialogClose = () => {
    setDialogState({ ...dialogState, open: false });
  };

  const handleDialogExited = () => {
    setDialogState(DIALOG_ACTION_INITIAL_STATE);
  };

  const handleDeleteDialogComplete = result => {
    if (result.change_type === 'delete') {
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
      ruleListRef.current.recomputeRowHeights();
      handleSnackbarOpen({
        message: `Rule ${result.rule_id} successfully scheduled`,
      });
    } else if (result.rule_id) {
      // The rule was directly deleted, just remove it.
      setRulesWithScheduledChanges(
        rulesWithScheduledChanges.filter(i => i.rule_id !== result.rule_id)
      );
      handleSnackbarOpen({
        message: `Rule ${result.rule_id} deleted`,
      });
    } else {
      setRulesWithScheduledChanges(
        rulesWithScheduledChanges.filter(
          i => !i.scheduledChange || i.scheduledChange.sc_id !== result.sc_id
        )
      );
      handleSnackbarOpen({
        message: `Scheduled Rule deleted`,
      });
    }

    handleDialogClose();
  };

  const handleDeleteDialogSubmit = async () => {
    const dialogRule = dialogState.item;
    const now = new Date();
    const when =
      scheduleDeleteDate >= now
        ? scheduleDeleteDate.getTime()
        : now.getTime() + 5000;
    let error = null;
    let ret = null;

    // removing a scheduled insert
    if (isScheduledInsert(dialogRule)) {
      ({ error } = await delSC({
        scId: dialogRule.scheduledChange.sc_id,
        scDataVersion: dialogRule.scheduledChange.sc_data_version,
      }));
      ret = { sc_id: dialogRule.scheduledChange.sc_id };
    }
    // directly deleting a rule that doesn't require signoff
    else if (Object.keys(dialogRule.required_signoffs).length === 0) {
      ({ error } = await delRule({
        ruleId: dialogRule.rule_id,
        dataVersion: dialogRule.data_version,
      }));
      ret = { rule_id: dialogRule.rule_id };
    }
    // scheduling deletion of a rule that requires signoff
    else {
      ({ error } = await scheduleDelRule({
        change_type: 'delete',
        when,
        rule_id: dialogRule.rule_id,
        data_version: dialogRule.data_version,
      }));
      // eslint-disable-next-line prefer-destructuring
      ret = (await getScheduledChangeByRuleId(dialogRule.rule_id)).data
        .scheduled_changes[0];
    }

    if (error) {
      throw error;
    }

    return ret;
  };

  const signoffDialogBody = (
    <FormControl component="fieldset">
      <RadioGroup
        aria-label="Role"
        name="role"
        value={signoffRole}
        onChange={handleSignoffRoleChange}>
        {roles.map(r => (
          <FormControlLabel key={r} value={r} label={r} control={<Radio />} />
        ))}
      </RadioGroup>
    </FormControl>
  );
  const filteredRulesCount = filteredRulesWithScheduledChanges.length;
  const updateSignoffs = ({ roleToSignoffWith, rule }) => {
    setRulesWithScheduledChanges(
      rulesWithScheduledChanges.map(r => {
        if (
          !r.scheduledChange ||
          r.scheduledChange.sc_id !== rule.scheduledChange.sc_id
        ) {
          return r;
        }

        const newRule = { ...r };

        newRule.scheduledChange.signoffs[username] = roleToSignoffWith;

        return newRule;
      })
    );
  };

  const doSignoff = async (roleToSignoffWith, rule) => {
    const { error } = await signoff({
      scId: rule.scheduledChange.sc_id,
      role: roleToSignoffWith,
    });

    return { error, result: { roleToSignoffWith, rule } };
  };

  const handleSignoffDialogSubmit = async () => {
    const { error, result } = await doSignoff(signoffRole, dialogState.item);

    if (error) {
      throw error;
    }

    return result;
  };

  const handleSignoffDialogComplete = result => {
    updateSignoffs(result);
    handleDialogClose();
  };

  const handleSignoff = async rule => {
    if (roles.length === 1) {
      const { error, result } = await doSignoff(roles[0], rule);

      if (!error) {
        updateSignoffs(result);
      }
    } else {
      setDialogState({
        ...dialogState,
        open: true,
        title: 'Signoff as…',
        confirmText: 'Sign off',
        item: rule,
        mode: 'signoff',
        handleComplete: handleSignoffDialogComplete,
        handleSubmit: handleSignoffDialogSubmit,
      });
    }
  };

  const handleRevoke = async rule => {
    const { error } = await revoke({
      scId: rule.scheduledChange.sc_id,
      role: rule.scheduledChange.signoffs[username],
    });

    if (!error) {
      setRulesWithScheduledChanges(
        rulesWithScheduledChanges.map(r => {
          if (
            !r.scheduledChange ||
            r.scheduledChange.sc_id !== rule.scheduledChange.sc_id
          ) {
            return r;
          }

          const newRule = { ...r };

          delete newRule.scheduledChange.signoffs[username];

          return newRule;
        })
      );
    }
  };

  const deleteDialogBody =
    dialogState.item &&
    (!isScheduledInsert(dialogState.item) &&
    Object.keys(dialogState.item.required_signoffs).length > 0 ? (
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
      `This will delete ${
        isScheduledInsert(dialogState.item)
          ? 'the scheduled rule'
          : `rule ${dialogState.item.rule_id}`
      }.`
    ));
  const handleRuleDelete = rule => {
    setDialogState({
      ...dialogState,
      open: true,
      title: 'Delete Rule?',
      confirmText: 'Delete',
      destructive: true,
      item: rule,
      mode: 'delete',
      handleComplete: handleDeleteDialogComplete,
      handleSubmit: handleDeleteDialogSubmit,
    });
  };

  const getDialogSubmit = () => {
    if (dialogState.mode === 'delete') {
      return handleDeleteDialogSubmit;
    }

    return handleSignoffDialogSubmit;
  };

  const getRowHeight = ({ index }) => {
    const rule = filteredRulesWithScheduledChanges[index];
    const hasScheduledChanges = Boolean(rule.scheduledChange);
    // Padding top and bottom included
    const listPadding = theme.spacing(1);
    const listItemTextMargin = 6;
    const diffRowHeight = remToPx(theme.typography.body2.fontSize) * 1.5;
    // <CardContent /> padding
    let height = theme.spacing(2);

    // actions row
    height += buttonHeight + theme.spacing(2);

    if (!hasScheduledChanges || rule.scheduledChange.change_type !== 'insert') {
      // avatar height (title) + padding
      height += theme.spacing(4) + theme.spacing(3);

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

      height +=
        rows *
          (body1TextHeight() + body2TextHeight() + 2 * listItemTextMargin) +
        2 * listPadding;

      // row with comment
      // (max 8*10px; ~3 lines of comments otherwise we display a scroller)
      if (rule.comment) {
        height += theme.spacing(10) + 2 * listItemTextMargin + 2 * listPadding;
      }
    }

    if (hasScheduledChanges) {
      // row with the chip label
      height += Math.max(subtitle1TextHeight(), theme.spacing(3));

      if (rule.scheduledChange.change_type === 'delete') {
        // row with "all properties will be deleted" + padding
        height += body2TextHeight() + theme.spacing(2);
      } else if (
        rule.scheduledChange.change_type === 'update' ||
        rule.scheduledChange.change_type === 'insert'
      ) {
        const diffedProperties = getDiffedProperties(
          RULE_DIFF_PROPERTIES,
          rule,
          rule.scheduledChange
        );

        // diff viewer + marginTop
        height += diffedProperties.length * diffRowHeight + theme.spacing(1);
      }

      if (
        rule.scheduledChange.change_type === 'delete' ||
        rule.scheduledChange.change_type === 'update'
      ) {
        // divider
        height += theme.spacing(2) + 1;
      }

      if (Object.keys(rule.scheduledChange.required_signoffs).length > 0) {
        const requiredRoles = Object.keys(
          rule.scheduledChange.required_signoffs
        ).length;
        const nSignoffs = Object.keys(rule.scheduledChange.signoffs).length;
        // Required Roles and Signoffs are beside one another, so we only
        // need to account for the one with the most items.
        const signoffRows = Math.max(requiredRoles, nSignoffs);

        // Padding above the summary
        height += theme.spacing(2);

        // The "Requires Signoff From" title and the margin beneath it
        height += signoffSummarylistSubheaderTextHeight + theme.spacing(0.5);

        // Space for however many rows exist.
        height += signoffRows * body2TextHeight();
      }
    }

    // space below the card (margin)
    height += theme.spacing(6);

    return height;
  };

  const isRuleSelected = rule => {
    if (!hashQuery.ruleId && !hashQuery.scId) {
      return false;
    }

    if (hashQuery.ruleId) {
      return Boolean(rule.rule_id === Number(hashQuery.ruleId));
    }

    if (hashQuery.scId) {
      return Boolean(
        rule.scheduledChange &&
          Number(rule.scheduledChange.sc_id === hashQuery.scId)
      );
    }
  };

  const Row = ({ index, style }) => {
    const rule = filteredRulesWithScheduledChanges[index];
    const isSelected = isRuleSelected(rule);

    return (
      <div
        key={
          rule.rule_id
            ? rule.rule_id
            : Object.values(rule.scheduledChange).join('-')
        }
        style={style}>
        <RuleCard
          className={classNames(classes.ruleCard, {
            [classes.ruleCardSelected]: isSelected,
          })}
          key={rule.rule_id}
          rule={rule}
          rulesFilter={searchQueries}
          onRuleDelete={handleRuleDelete}
          onSignoff={() => handleSignoff(rule)}
          onRevoke={() => handleRevoke(rule)}
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
                ref={ruleListRef}
                rowRenderer={Row}
                scrollToRow={scrollToRow}
                rowHeight={getRowHeight}
                rowCount={filteredRulesCount}
              />
            </Fragment>
          )}
          <Link
            to={{
              pathname: '/rules/create',
              state: { rulesFilter: searchQueries },
            }}>
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
        destructive={dialogState.destructive}
        body={
          dialogState.mode === 'delete' ? deleteDialogBody : signoffDialogBody
        }
        confirmText={dialogState.confirmText}
        onSubmit={getDialogSubmit()}
        onError={handleDialogError}
        error={dialogState.error}
        onComplete={dialogState.handleComplete}
        onClose={handleDialogClose}
        onExited={handleDialogExited}
      />
      <Snackbar onClose={handleSnackbarClose} {...snackbarState} />
    </Dashboard>
  );
}

export default withUser(ListRules);
