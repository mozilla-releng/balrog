import React, { Fragment, useEffect, useState, useMemo, useRef } from 'react';
import classNames from 'classnames';
import { stringify, parse } from 'qs';
import { addSeconds } from 'date-fns';
import { clone } from 'ramda';
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
import FormLabel from '@material-ui/core/FormLabel';
// import Checkbox from '@material-ui/core/Checkbox';
import Switch from '@material-ui/core/Switch';
import SpeedDialAction from '@material-ui/lab/SpeedDialAction';
import Drawer from '@material-ui/core/Drawer';
import PlusIcon from 'mdi-react/PlusIcon';
import PauseIcon from 'mdi-react/PauseIcon';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import EmergencyShutoffCard from '../../../components/EmergencyShutoffCard';
import RuleCard from '../../../components/RuleCard';
import DialogAction from '../../../components/DialogAction';
import DateTimePicker from '../../../components/DateTimePicker';
import VariableSizeList from '../../../components/VariableSizeList';
import SpeedDial from '../../../components/SpeedDial';
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
import {
  getEmergencyShutoffs,
  createEmergencyShutoff,
  deleteEmergencyShutoff,
  getScheduledChanges as getScheduledEmergencyShutoffs,
  scheduleDeleteEmergencyShutoff,
  cancelDeleteEmergencyShutoff,
} from '../../../services/emergency_shutoff';
import {
  getRelease,
  getReleaseV2,
  getScheduledChangeByName,
} from '../../../services/releases';
import { getUserInfo } from '../../../services/users';
import { ruleMatchesRequiredSignoff } from '../../../utils/requiredSignoffs';
import {
  RULE_DIFF_PROPERTIES,
  DIALOG_ACTION_INITIAL_STATE,
  OBJECT_NAMES,
  SNACKBAR_INITIAL_STATE,
  CONTENT_MAX_WIDTH,
} from '../../../utils/constants';
import { withUser } from '../../../utils/AuthContext';
import remToPx from '../../../utils/remToPx';
import elementsHeight from '../../../utils/elementsHeight';
import Snackbar from '../../../components/Snackbar';
import { ruleMatchesChannel } from '../../../utils/rules';

const ALL = 'all';
const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
    right: theme.spacing(12),
  },
  options: {
    background: theme.palette.background.default,
    top: 64,
    right: 0,
    left: 0,
    padding: `${theme.spacing(4)}px ${theme.spacing(4)}px 0`,
    display: 'flex',
    justifyContent: 'center',
    position: 'fixed',
    zIndex: 2,
  },
  checkbox: {
    padding: `${theme.spacing(2)}px ${theme.spacing(1)}px`,
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
  card: {
    margin: theme.spacing(1),
  },
  ruleCardSelected: {
    border: `2px solid ${theme.palette.primary.light}`,
  },
  drawerPaper: {
    maxWidth: CONTENT_MAX_WIDTH,
    margin: '0 auto',
    padding: theme.spacing(1),
    maxHeight: '80vh',
  },
  pendingSignoffFormControl: {
    display: 'flex',
    alignItems: 'center',
  },
  pendingSignoffFormLabel: {
    transform: 'scale(0.75)',
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
    h6TextHeight,
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
  const [rewoundRules, setRewoundRules] = useState([]);
  const searchFieldRef = useRef(null);
  const [searchFieldHeight, setSearchFieldHeight] = useState(0);
  const [productChannelOptions, setProductChannelOptions] = useState([]);
  const productChannelQueries = query.product
    ? [query.product, query.channel]
    : null;
  const [productChannelFilter, setProductChannelFilter] = useState(
    productChannelQueries
      ? productChannelQueries.filter(Boolean).join(productChannelSeparator)
      : ALL
  );
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [scheduleDeleteDate, setScheduleDeleteDate] = useState(
    addSeconds(new Date(), -30)
  );
  const [dateTimePickerError, setDateTimePickerError] = useState(null);
  const [rewindDate, setRewindDate] = useState(
    query.timestamp ? new Date(parseInt(query.timestamp, 10)) : null
  );
  const [rewindDateError, setRewindDateError] = useState(null);
  // const [showRewindDiff, setShowRewindDiff] = useState(false);
  const [scrollToRow, setScrollToRow] = useState(null);
  const [roles, setRoles] = useState([]);
  const [requiredRoles, setRequiredRoles] = useState([]);
  const [emergencyShutoffs, setEmergencyShutoffs] = useState([]);
  const [
    emergencyShutoffReasonComment,
    setEmergencyShutoffReasonComment,
  ] = useState('');
  const [signoffRole, setSignoffRole] = useState('');
  const [drawerState, setDrawerState] = useState({ open: false, item: {} });
  const [drawerReleaseName, setDrawerReleaseName] = useState(null);
  const ruleListRef = useRef(null);
  const [products, fetchProducts] = useAction(getProducts);
  const [channels, fetchChannels] = useAction(getChannels);
  const [rules, fetchRules] = useAction(getRules);
  const [scheduledChanges, fetchScheduledChanges] = useAction(
    getScheduledChanges
  );
  const [requiredSignoffs, fetchRequiredSignoffs] = useAction(
    getRequiredSignoffs
  );
  const [release, fetchRelease] = useAction(getRelease);
  const [releaseV2, fetchReleaseV2] = useAction(getReleaseV2);
  const [scheduledChangeNameAction, fetchScheduledChangeByName] = useAction(
    getScheduledChangeByName
  );
  const [delRuleAction, delRule] = useAction(deleteRule);
  const [scheduleDelRuleAction, scheduleDelRule] = useAction(
    addScheduledChange
  );
  const [delScAction, delSC] = useAction(deleteScheduledChange);
  const [signoffAction, signoff] = useAction(props =>
    makeSignoff({ type: 'rules', ...props })
  );
  const [revokeAction, revoke] = useAction(props =>
    revokeSignoff({ type: 'rules', ...props })
  );
  const [rolesAction, fetchRoles] = useAction(getUserInfo);
  const [emergencyShutoffsAction, fetchEmergencyShutoffs] = useAction(
    getEmergencyShutoffs
  );
  const [
    scheduledEmergencyShutoffsAction,
    fetchScheduledEmergencyShutoffs,
  ] = useAction(getScheduledEmergencyShutoffs);
  const filteredProductChannelIsShutoff =
    productChannelFilter !== ALL &&
    productChannelQueries &&
    productChannelQueries.length === 2
      ? emergencyShutoffs.some(
          es =>
            es.product === productChannelQueries[0] &&
            (!productChannelQueries[1] ||
              es.channel === productChannelQueries[1])
        )
      : false;
  const filteredProductChannelRequiresSignoff =
    requiredSignoffs.data &&
    productChannelQueries &&
    productChannelQueries.length === 2
      ? requiredSignoffs.data.data.required_signoffs.some(
          rs =>
            rs.product === productChannelQueries[0] &&
            rs.channel === productChannelQueries[1]
        )
      : false;
  const [disableUpdatesAction, disableUpdates] = useAction(
    createEmergencyShutoff
  );
  const [enableUpdatesAction, enableUpdates] = useAction(
    deleteEmergencyShutoff
  );
  const [scheduleEnableUpdatesAction, scheduleEnableUpdates] = useAction(
    scheduleDeleteEmergencyShutoff
  );
  const [cancelEnableUpdatesAction, cancelEnableUpdates] = useAction(
    cancelDeleteEmergencyShutoff
  );
  const [signoffEnableUpdatesAction, signoffEnableUpdates] = useAction(props =>
    signoff({ type: 'emergency_shutoff', ...props })
  );
  const [revokeEnableUpdatesAction, revokeEnableUpdates] = useAction(props =>
    revoke({ type: 'emergency_shutoff', ...props })
  );
  const isLoading =
    products.loading ||
    channels.loading ||
    rules.loading ||
    emergencyShutoffsAction.loading;
  const isActionLoading =
    // The first two are to check if "View Release" is currently fetching
    release.loading ||
    releaseV2.loading ||
    scheduledChangeNameAction.loading ||
    delScAction.loading ||
    delRuleAction.loading ||
    signoffAction.loading ||
    scheduleDelRuleAction.loading ||
    signoffEnableUpdatesAction.loading;
  const error =
    products.error ||
    channels.error ||
    rules.error ||
    emergencyShutoffsAction.error ||
    scheduledEmergencyShutoffsAction.error ||
    disableUpdatesAction.error ||
    enableUpdatesAction.error ||
    scheduleEnableUpdatesAction.error ||
    cancelEnableUpdatesAction.error ||
    rolesAction.error ||
    scheduledChanges.error ||
    revokeAction.error ||
    (roles.length === 1 && signoffAction.error) ||
    revokeEnableUpdatesAction.error ||
    (roles.length === 1 && signoffEnableUpdatesAction.error);
  const handleFilterChange = ({ target: { value } }) => {
    setProductChannelFilter(value);

    const [product, channel] =
      value === ALL
        ? [undefined, undefined]
        : value.split(productChannelSeparator);
    const qs = {
      ...query,
      product,
      channel,
    };

    props.history.push(`/rules${stringify(qs, { addQueryPrefix: true })}`);
  };

  const handleShowOnlyScheduledChangesChange = ({ target: { checked } }) => {
    const qs = {
      ...query,
      onlyScheduledChanges: checked ? 1 : undefined,
    };

    props.history.push(`/rules${stringify(qs, { addQueryPrefix: true })}`);
  };

  const handleSignoffRoleChange = ({ target: { value } }) =>
    setSignoffRole(value);
  const handleSnackbarOpen = ({ message, variant = 'success' }) => {
    setSnackbarState({ message, variant, open: true });
  };

  // const handleRewindDiffChange = ({ target: { checked: value } }) =>
  //   setShowRewindDiff(value);
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
    if (!rules.data || !scheduledChanges.data || !requiredSignoffs.data) {
      return;
    }

    if (rewindDate) {
      setRewoundRules(rules.data.data.rules);
    } else {
      const rulesWithScheduledChanges = rules.data.data.rules.map(rule => {
        const sc = scheduledChanges.data.data.scheduled_changes.find(
          sc => rule.rule_id === sc.rule_id
        );
        const returnedRule = { ...rule };

        if (sc) {
          returnedRule.scheduledChange = sc;
          returnedRule.scheduledChange.when = new Date(
            returnedRule.scheduledChange.when
          );
        }

        returnedRule.required_signoffs = {};
        requiredSignoffs.data.data.required_signoffs.forEach(rs => {
          if (ruleMatchesRequiredSignoff(rule, rs)) {
            returnedRule.required_signoffs[rs.role] = rs.signoffs_required;
          }
        });

        return returnedRule;
      });

      scheduledChanges.data.data.scheduled_changes.forEach(sc => {
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
          ruleA.scheduledChange && ruleA.scheduledChange.priority
            ? ruleA.scheduledChange.priority
            : ruleA.priority;
        const priorityB =
          ruleB.scheduledChange && ruleB.scheduledChange.priority
            ? ruleB.scheduledChange.priority
            : ruleB.priority;

        return priorityB - priorityA;
      });

      setRulesWithScheduledChanges(sortedRules);
      setRewoundRules([]);

      if (
        emergencyShutoffsAction.data &&
        scheduledEmergencyShutoffsAction.data
      ) {
        const shutoffs = emergencyShutoffsAction.data.data.shutoffs.map(
          shutoff => {
            const returnedShutoff = clone(shutoff);
            /* eslint-disable-next-line max-len */
            const sc = scheduledEmergencyShutoffsAction.data.data.scheduled_changes.find(
              ses =>
                ses.product === shutoff.product &&
                ses.channel === shutoff.channel
            );

            if (sc) {
              returnedShutoff.scheduledChange = sc;
            }

            return returnedShutoff;
          }
        );

        setEmergencyShutoffs(shutoffs);
      }
    }
  }, [
    rules.data,
    scheduledChanges.data,
    requiredSignoffs.data,
    emergencyShutoffsAction.data,
    scheduledEmergencyShutoffsAction.data,
  ]);

  useEffect(() => {
    fetchRules(rewindDate ? rewindDate.getTime() : null);
  }, [rewindDate]);

  useEffect(() => {
    Promise.all([
      fetchScheduledChanges(),
      fetchRequiredSignoffs(OBJECT_NAMES.PRODUCT_REQUIRED_SIGNOFF),
      fetchEmergencyShutoffs(),
      fetchScheduledEmergencyShutoffs(),
      fetchProducts(),
      fetchChannels(),
    ]);
  }, []);

  useEffect(() => {
    setSearchFieldHeight(searchFieldRef.current.clientHeight);
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

  const filteredRulesWithScheduledChanges = useMemo(() => {
    let filteredRules = clone(rulesWithScheduledChanges);

    // Pending signoff switch
    if (filteredRules && Boolean(query.onlyScheduledChanges)) {
      filteredRules = filteredRules.filter(rule => rule.scheduledChange);
    }

    const rewoundFilteredRules = clone(rewoundRules);
    // use this line for non-diff mode on rewound rules
    let rulesToShow =
      rewoundRules.length === 0 ? filteredRules : rewoundFilteredRules;

    if (!productChannelQueries) {
      return rulesToShow;
    }

    // Product channel dropdown filter
    rulesToShow = rulesToShow.filter(rule => {
      const [productFilter, channelFilter] = productChannelQueries;
      const ruleProduct =
        rule.product || (rule.scheduledChange && rule.scheduledChange.product);

      if (ruleProduct !== productFilter) {
        return false;
      }

      if (channelFilter && !ruleMatchesChannel(rule, channelFilter)) {
        return false;
      }

      return true;
    });

    return rulesToShow;
  }, [
    productChannelQueries,
    rulesWithScheduledChanges,
    query.onlyScheduledChanges,
    rewoundRules,
  ]);
  const handleDateTimePickerError = error => {
    setDateTimePickerError(error);
  };

  const handleDateTimeChange = date => {
    setScheduleDeleteDate(date);
    setDateTimePickerError(null);
  };

  const handleRewindDateTimePickerError = error => {
    setRewindDateError(error);
  };

  const handleRewindDateTimeChange = date => {
    setRewindDate(date);
    setRewindDateError(null);

    const qs = {
      ...query,
      timestamp: date ? date.getTime() : undefined,
    };

    props.history.push(`/rules${stringify(qs, { addQueryPrefix: true })}`);
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

          const newRule = clone(r);

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
        : now.getTime() + 30000;
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
        {roles.map(r => {
          return (
            <FormControlLabel
              key={r}
              value={r}
              label={r}
              control={<Radio />}
              disabled={!(requiredRoles && requiredRoles.includes(r))}
            />
          );
        })}
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

        const newRule = clone(r);

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
    setRequiredRoles(Object.keys(rule.required_signoffs));

    const userRequiredRoles = Object.keys(rule.required_signoffs).filter(r =>
      roles.includes(r)
    );

    if (userRequiredRoles.length === 1) {
      const { error, result } = await doSignoff(userRequiredRoles[0], rule);

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

          const newRule = clone(r);

          delete newRule.scheduledChange.signoffs[username];

          return newRule;
        })
      );
    }
  };

  const deleteDialogBody =
    dialogState.mode === 'delete' &&
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

  const disableUpdatesBody = (
    <FormControl component="fieldset">
      <TextField
        fullWidth
        multiline
        label="Reason comment"
        onChange={({ target: { value } }) => {
          setEmergencyShutoffReasonComment(value);
        }}
        value={emergencyShutoffReasonComment}
      />
    </FormControl>
  );
  const handleDisableUpdatesSubmit = async () => {
    const [product, channel] = productChannelQueries;
    const { error, data } = await disableUpdates(
      product,
      channel,
      emergencyShutoffReasonComment
    );

    if (!error) {
      const result = clone(emergencyShutoffs);

      result.push(data.data);
      setEmergencyShutoffs(result);
      handleSnackbarOpen({
        message: `Updates for the ${product} ${channel} channel have been disabled`,
      });
      setEmergencyShutoffReasonComment('');
    }

    handleDialogClose();
  };

  const handleDisableUpdates = async () => {
    const [product, channel] = productChannelQueries;

    setDialogState({
      ...dialogState,
      open: true,
      title: `Disable updates for ${product} : ${channel} ?`,
      confirmText: 'Yes',
      destructive: false,
      mode: 'disableUpdates',
      handleSubmit: handleDisableUpdatesSubmit,
    });
  };

  const handleEnableUpdates = async () => {
    const [product, channel] = productChannelQueries;
    const esDetails = emergencyShutoffs.find(
      es => es.product === product && es.channel === channel
    );

    if (filteredProductChannelRequiresSignoff) {
      const now = new Date();
      const when = now.getTime() + 30000;
      const { error } = await scheduleEnableUpdates(
        product,
        channel,
        esDetails.data_version,
        when
      );

      if (!error) {
        const {
          error: sesError,
          data: sesData,
        } = await fetchScheduledEmergencyShutoffs();

        if (!sesError) {
          setEmergencyShutoffs(
            emergencyShutoffs.map(es => {
              if (es.product !== product || es.channel !== channel) {
                return es;
              }

              const shutoff = clone(es);
              const sc = sesData.data.scheduled_changes.find(
                ses => ses.product === es.product && ses.channel === es.channel
              );

              if (sc) {
                shutoff.scheduledChange = sc;
              }

              return shutoff;
            })
          );
        }
      }
    } else {
      const { error } = await enableUpdates(
        product,
        channel,
        esDetails.data_version
      );

      if (!error) {
        setEmergencyShutoffs(
          emergencyShutoffs.filter(
            es => es.product !== product || es.channel !== channel
          )
        );
      }
    }
  };

  const handleCancelEnableUpdates = async () => {
    const [product, channel] = productChannelQueries;
    const esDetails = emergencyShutoffs.find(
      es => es.product === product && es.channel === channel
    );
    const { error } = await cancelEnableUpdates(
      esDetails.scheduledChange.sc_id,
      esDetails.scheduledChange.sc_data_version
    );

    if (!error) {
      setEmergencyShutoffs(
        emergencyShutoffs.map(es => {
          if (es.product !== product || es.channel !== channel) {
            return es;
          }

          const shutoff = clone(es);

          delete shutoff.scheduledChange;

          return shutoff;
        })
      );
    }
  };

  const updateSignoffsEnableUpdates = ({
    roleToSignoffWith,
    emergencyShutoff,
  }) => {
    setEmergencyShutoffs(
      emergencyShutoffs.map(es => {
        if (
          !es.scheduledChange ||
          es.scheduledChange.sc_id !== emergencyShutoff.scheduledChange.sc_id
        ) {
          return es;
        }

        const newEs = clone(es);

        newEs.scheduledChange.signoffs[username] = roleToSignoffWith;

        return newEs;
      })
    );
  };

  const doSignoffEnableUpdates = async (
    roleToSignoffWith,
    emergencyShutoff
  ) => {
    const { error } = await signoffEnableUpdates({
      scId: emergencyShutoff.scheduledChange.sc_id,
      role: roleToSignoffWith,
    });

    return { error, result: { roleToSignoffWith, emergencyShutoff } };
  };

  const handleSignoffEnableUpdatesDialogSubmit = async () => {
    const { error, result } = await doSignoffEnableUpdates(
      signoffRole,
      dialogState.item
    );

    if (error) {
      throw error;
    }

    return result;
  };

  const handleSignoffEnableUpdatesDialogComplete = result => {
    updateSignoffsEnableUpdates(result);
    handleDialogClose();
  };

  const handleSignoffEnableUpdates = async () => {
    const [product, channel] = productChannelQueries;
    const esDetails = emergencyShutoffs.find(
      es => es.product === product && es.channel === channel
    );

    if (roles.length === 1) {
      const { error, result } = await doSignoffEnableUpdates(
        roles[0],
        esDetails
      );

      if (!error) {
        updateSignoffsEnableUpdates(result);
      }
    } else {
      setDialogState({
        ...dialogState,
        open: true,
        title: 'Signoff as…',
        confirmText: 'Sign off',
        item: esDetails,
        mode: 'signoffEnableUpdates',
        handleComplete: handleSignoffEnableUpdatesDialogComplete,
        handleSubmit: handleSignoffEnableUpdatesDialogSubmit,
      });
    }
  };

  const handleRevokeEnableUpdates = async () => {
    const [product, channel] = productChannelQueries;
    const esDetails = emergencyShutoffs.find(
      es => es.product === product && es.channel === channel
    );
    const { error } = await revokeEnableUpdates({
      scId: esDetails.scheduledChange.sc_id,
      role: esDetails.scheduledChange.signoffs[username],
    });

    if (!error) {
      setEmergencyShutoffs(
        emergencyShutoffs.map(es => {
          if (
            !es.scheduledChange ||
            es.scheduledChange.sc_id !== esDetails.scheduledChange.sc_id
          ) {
            return es;
          }

          const newEs = clone(es);

          delete newEs.scheduledChange.signoffs[username];

          return newEs;
        })
      );
    }
  };

  const handleViewRelease = ({ currentTarget: { name } }) => {
    // Sometimes the previous opened release drawer may be the same as
    // the one being requested. In that case, we simply open the drawer
    // without having the useEffect take care of
    // fetching the release + opening the drawer
    if (drawerReleaseName === name) {
      setDrawerState({
        ...drawerState,
        open: true,
      });
    } else {
      setDrawerReleaseName(name);
    }
  };

  useEffect(() => {
    if (drawerReleaseName) {
      fetchReleaseV2(drawerReleaseName).then(fetchedRelease => {
        if (!fetchedRelease.error) {
          const item =
            Object.keys(fetchedRelease.data.data.sc_blob).length > 0
              ? JSON.stringify(fetchedRelease.data.data.sc_blob, null, 2)
              : JSON.stringify(fetchedRelease.data.data.blob, null, 2);

          setDrawerState({
            ...drawerState,
            open: true,
            item,
          });
        } else {
          Promise.all([
            fetchRelease(drawerReleaseName),
            fetchScheduledChangeByName(drawerReleaseName),
          ]).then(([fetchedRelease, fetchedSC]) => {
            const item =
              fetchedSC.data.data.count > 0
                ? JSON.stringify(
                    fetchedSC.data.data.scheduled_changes[0].data,
                    null,
                    2
                  )
                : JSON.stringify(fetchedRelease.data.data, null, 2);

            setDrawerState({
              ...drawerState,
              open: true,
              item,
            });
          });
        }
      });
    }
  }, [drawerReleaseName]);

  const handleDrawerClose = () => {
    // We do not set the drawer item key to the initial state to
    // avoid re-fetching if the user decides to view the same mapping again
    setDrawerState({
      ...drawerState,
      open: false,
    });
  };

  const getDialogSubmit = () => {
    const dialogSubmits = {
      delete: handleDeleteDialogSubmit,
      signoff: handleSignoffDialogSubmit,
      disableUpdates: handleDisableUpdatesSubmit,
      signoffEnableUpdates: handleSignoffEnableUpdatesDialogSubmit,
    };

    return dialogSubmits[dialogState.mode];
  };

  const getDialogBody = () => {
    const dialogStates = {
      delete: deleteDialogBody,
      signoff: signoffDialogBody,
      disableUpdates: disableUpdatesBody,
    };

    return dialogStates[dialogState.mode];
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
      height +=
        Math.max(
          // avatar height
          theme.spacing(4),
          // product:channel header height
          h6TextHeight,
          // revisions icon
          theme.spacing(3) + 24
        ) + theme.spacing(1); // top padding

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
      if (rule.comment) {
        height +=
          body1TextHeight() +
          body2TextHeight() +
          2 * listItemTextMargin +
          2 * listPadding;
      }
    }

    if (hasScheduledChanges) {
      // row with the chip label
      height += Math.max(subtitle1TextHeight(), theme.spacing(3));

      if (rule.scheduledChange.change_type === 'delete') {
        // row with "all properties will be deleted"
        height += body2TextHeight();
      } else if (
        rule.scheduledChange.change_type === 'update' ||
        rule.scheduledChange.change_type === 'insert'
      ) {
        const diffedProperties = getDiffedProperties(
          RULE_DIFF_PROPERTIES,
          rule,
          rule.scheduledChange
        );

        // diff viewer + marginTop + height of the
        // horizontal scroller (rough estimate;
        // sometimes there are no scroller as well)
        height +=
          diffedProperties.length * diffRowHeight +
          theme.spacing(1) +
          theme.spacing(2);
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
    height += theme.spacing(4);

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
          Number(rule.scheduledChange.sc_id === Number(hashQuery.scId))
      );
    }
  };

  const Row = ({ index, style }) => {
    // if we're in rewind mode, rule is a historical rule, not the current one
    const rule = filteredRulesWithScheduledChanges[index];
    const isSelected = isRuleSelected(rule);
    // const currentRule = rulesWithScheduledChanges.find(
    //   r => r.rule_id === rule.rule_id
    // );

    // if (rewoundRules.length !== 0) {
    //   // TODO: horrible hack, need to fix this
    //   // maybe add diffAgainst argument to RuleCard
    //   // to control whether or not DiffRule is shown
    //   if (showRewindDiff && currentRule) {
    //     rule.scheduledChange = currentRule;
    //     rule.scheduledChange.change_type = 'update';
    //     rule.scheduledChange.required_signoffs = {};
    //     rule.scheduledChange.signoffs = {};
    //     rule.scheduledChange.when = new Date();
    //   } else if (rule.scheduledChange) {
    //     delete rule.scheduledChange;
    //   }
    // }

    return (
      <div
        key={
          rule.rule_id
            ? rule.rule_id
            : Object.values(rule.scheduledChange).join('-')
        }
        style={style}>
        <RuleCard
          className={classNames(classes.card, {
            [classes.ruleCardSelected]: isSelected,
          })}
          key={rule.rule_id}
          rule={rule}
          rulesFilter={productChannelQueries}
          onRuleDelete={handleRuleDelete}
          canSignoff={
            !rewindDate &&
            rule.required_signoffs &&
            Object.keys(rule.required_signoffs).filter(r => roles.includes(r))
              .length
          }
          onSignoff={() => handleSignoff(rule)}
          onRevoke={() => handleRevoke(rule)}
          onViewReleaseClick={handleViewRelease}
          isRewound={Boolean(rewindDate)}
          actionLoading={isActionLoading}
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
    <Dashboard
      title={
        rewindDate ? `Rules @ ${rewindDate.toString().split('(')[0]}` : 'Rules'
      }>
      {isLoading && <Spinner loading />}
      {error && <ErrorPanel fixed error={error} />}
      {!isLoading && productChannelOptions && (
        <Fragment>
          <div ref={searchFieldRef} className={classes.options}>
            <DateTimePicker
              disableFuture
              clearable
              inputVariant="outlined"
              label="Rewind to..."
              onError={handleRewindDateTimePickerError}
              helperText={rewindDateError}
              onDateTimeChange={handleRewindDateTimeChange}
              value={rewindDate}
            />
            {/* <FormControl className={classes.checkbox}>
              <FormLabel>Diff?</FormLabel>
              <Checkbox
                disabled={!rewindDate}
                checked={showRewindDiff}
                onChange={handleRewindDiffChange}
              />
            </FormControl> */}
            <FormControl className={classes.pendingSignoffFormControl}>
              <FormLabel className={classes.pendingSignoffFormLabel}>
                Filter by rules with scheduled changes
              </FormLabel>
              <Switch
                checked={Boolean(query.onlyScheduledChanges)}
                onChange={handleShowOnlyScheduledChangesChange}
              />
            </FormControl>
            <TextField
              className={classes.dropdown}
              select
              label={`Product${productChannelSeparator}Channel`}
              value={productChannelOptions.length ? productChannelFilter : ''}
              onChange={handleFilterChange}>
              <MenuItem value="all">All Rules</MenuItem>
              {productChannelOptions.map(option => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
          </div>
          <div style={{ marginTop: searchFieldHeight }}>
            {productChannelFilter !== ALL &&
              productChannelQueries &&
              productChannelQueries.length === 2 &&
              emergencyShutoffs.find(
                es =>
                  es.product === productChannelQueries[0] &&
                  es.channel === productChannelQueries[1]
              ) && (
                <EmergencyShutoffCard
                  className={classes.card}
                  emergencyShutoff={emergencyShutoffs.find(
                    es =>
                      es.product === productChannelQueries[0] &&
                      es.channel === productChannelQueries[1]
                  )}
                  onEnableUpdates={handleEnableUpdates}
                  onCancelEnable={handleCancelEnableUpdates}
                  onSignoff={handleSignoffEnableUpdates}
                  onRevoke={handleRevokeEnableUpdates}
                />
              )}
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
          </div>
        </Fragment>
      )}
      <DialogAction
        open={dialogState.open}
        title={dialogState.title}
        destructive={dialogState.destructive}
        body={getDialogBody()}
        confirmText={dialogState.confirmText}
        onSubmit={getDialogSubmit()}
        onError={handleDialogError}
        error={dialogState.error}
        onComplete={dialogState.handleComplete}
        onClose={handleDialogClose}
        onExited={handleDialogExited}
      />
      <Drawer
        classes={{ paper: classes.drawerPaper }}
        anchor="bottom"
        open={drawerState.open}
        onClose={handleDrawerClose}>
        <pre>
          <code>{drawerState.item}</code>
        </pre>
      </Drawer>
      <Snackbar onClose={handleSnackbarClose} {...snackbarState} />
      <Link
        to={{
          pathname: '/rules/create',
          state: { rulesFilter: productChannelQueries },
        }}>
        <Tooltip title="Add Rule">
          <Fab color="primary" className={classes.fab}>
            <PlusIcon />
          </Fab>
        </Tooltip>
      </Link>
      <SpeedDial ariaLabel="Secondary Actions">
        <SpeedDialAction
          FabProps={{
            disabled:
              isLoading ||
              !username ||
              filteredProductChannelIsShutoff ||
              !productChannelQueries ||
              !productChannelQueries[1],
          }}
          icon={<PauseIcon />}
          tooltipOpen
          tooltipTitle="Disable Updates"
          onClick={
            !isLoading &&
            !!username &&
            !filteredProductChannelIsShutoff &&
            !!productChannelQueries &&
            !!productChannelQueries[1]
              ? handleDisableUpdates
              : undefined
          }
        />
      </SpeedDial>
    </Dashboard>
  );
}

export default withUser(ListRules);
