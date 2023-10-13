import React, { Fragment, useState, useEffect } from 'react';
import classNames from 'classnames';
import { bool } from 'prop-types';
import { defaultTo, assocPath, pick } from 'ramda';
import { stringify } from 'qs';
import NumberFormat from 'react-number-format';
import { makeStyles } from '@material-ui/styles';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
import Tooltip from '@material-ui/core/Tooltip';
import Fab from '@material-ui/core/Fab';
import SpeedDialAction from '@material-ui/lab/SpeedDialAction';
import ContentSaveIcon from 'mdi-react/ContentSaveIcon';
import DeleteIcon from 'mdi-react/DeleteIcon';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import AutoCompleteText from '../../../components/AutoCompleteText';
import getSuggestions from '../../../components/AutoCompleteText/getSuggestions';
import DateTimePicker from '../../../components/DateTimePicker';
import SpeedDial from '../../../components/SpeedDial';
import useAction from '../../../hooks/useAction';
import {
  getScheduledChangeByRuleId,
  getScheduledChangeByScId,
  getRule,
  getProducts,
  getChannels,
  addScheduledChange,
  updateScheduledChange,
  deleteScheduledChange,
} from '../../../services/rules';
import { getReleaseNames, getReleaseNamesV2 } from '../../../services/releases';
import { withUser } from '../../../utils/AuthContext';
import {
  EMPTY_MENU_ITEM_CHAR,
  SPLIT_WITH_NEWLINES_AND_COMMA_REGEX,
  RULE_PRODUCT_UNSUPPORTED_PROPERTIES,
} from '../../../utils/constants';
// ALL IMPORTS TO FETCH REQUIRED SIGNOFFS BELOW:
import { OBJECT_NAMES } from '../../../utils/constants';
import { getRequiredSignoffs } from '../../../services/requiredSignoffs';
import Typography from '@material-ui/core/Typography';

const initialRule = {
  alias: '',
  backgroundRate: 0,
  buildID: '',
  buildTarget: '',
  channel: '',
  comment: '',
  distVersion: '',
  distribution: '',
  fallbackMapping: '',
  headerArchitecture: '',
  instructionSet: '',
  jaws: EMPTY_MENU_ITEM_CHAR,
  locale: '',
  mapping: '',
  memory: '',
  mig64: EMPTY_MENU_ITEM_CHAR,
  osVersion: '',
  priority: 0,
  product: '',
  update_type: 'minor',
  version: '',
};
const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  secondFab: {
    ...theme.mixins.fab,
    right: theme.spacing(12),
  },
  fabWithTooltip: {
    height: theme.spacing(7),
    width: theme.spacing(7),
  },
  scheduleDiv: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: theme.spacing(4),
  },
  scheduleIcon: {
    marginRight: theme.spacing(3),
  },
}));

function Rule({ isNewRule, user, ...props }) {
  const classes = useStyles();
  const rulesFilter =
    props.location.state && props.location.state.rulesFilter
      ? props.location.state.rulesFilter
      : [];
  const [rule, setRule] = useState(initialRule);
  const [allRequiredSignOffs, setAllrequiredSignoffs] = useState([]);
  const [releaseNames, setReleaseNames] = useState([]);
  const [products, fetchProducts] = useAction(getProducts);
  const [channels, fetchChannels] = useAction(getChannels);
  const [releaseNamesAction, fetchReleaseNames] = useAction(getReleaseNames);
  const [releaseNamesV2Action, fetchReleaseNamesV2] = useAction(
    getReleaseNamesV2
  );
  // 30 seconds - to make sure the helper text "Scheduled for ASAP" shows up
  const [scheduleDate, setScheduleDate] = useState(new Date());
  const [dateTimePickerError, setDateTimePickerError] = useState(null);
  const [fetchRuleAction, fetchRule] = useAction(getRule);
  const [scheduledChangeActionRuleId, fetchScheduledChangeByRuleId] = useAction(
    getScheduledChangeByRuleId
  );
  const [scheduledChangeActionScId, fetchScheduledChangeByScId] = useAction(
    getScheduledChangeByScId
  );
  const [addSCAction, addSC] = useAction(addScheduledChange);
  const [updateSCAction, updateSC] = useAction(updateScheduledChange);
  const [deleteSCAction, deleteSC] = useAction(deleteScheduledChange);
  const isLoading =
    fetchRuleAction.loading || products.loading || channels.loading;
  const actionLoading =
    releaseNamesAction.loading ||
    releaseNamesV2Action.loading ||
    addSCAction.loading ||
    updateSCAction.loading ||
    deleteSCAction.loading ||
    scheduledChangeActionRuleId.loading ||
    scheduledChangeActionScId.loading;
  const error =
    releaseNamesAction.error ||
    releaseNamesV2Action.error ||
    fetchRuleAction.error ||
    scheduledChangeActionRuleId.error ||
    scheduledChangeActionScId.error ||
    addSCAction.error ||
    updateSCAction.error ||
    deleteSCAction.error;
  const { ruleId, scId } = props.match.params;
  const hasScheduledChange = !!rule.sc_id;
  const defaultToEmptyString = defaultTo('');
  const osVersionTextValue = defaultToEmptyString(rule.osVersion)
    .split(SPLIT_WITH_NEWLINES_AND_COMMA_REGEX)
    .join('\n');
  const localeTextValue = defaultToEmptyString(rule.locale)
    .split(SPLIT_WITH_NEWLINES_AND_COMMA_REGEX)
    .join('\n');
  const handleInputChange = ({ target: { name, value } }) => {
    setRule(assocPath([name], value, rule));
  };

  const handleTextFieldWithNewLinesChange = ({ target: { name, value } }) => {
    setRule(assocPath([name], value.split('\n').join(','), rule));
  };

  const handleProductChange = value =>
    setRule(assocPath(['product'], value, rule));
  const handleChannelChange = value =>
    setRule(assocPath(['channel'], value, rule));
  const handleMappingChange = value =>
    setRule(assocPath(['mapping'], value, rule));
  const handleFallbackMappingChange = value =>
    setRule(assocPath(['fallbackMapping'], value, rule));
  const handleNumberChange = name => ({ floatValue: value }) => {
    setRule(assocPath([name], value, rule));
  };

  const redirectWithRulesFilter = hashFilter => {
    const [product, channel] = rulesFilter;
    const query = stringify({ product, channel }, { addQueryPrefix: true });

    props.history.push(`/rules${query}#${hashFilter}`);
  };

  useEffect(() => {
    Promise.all([fetchReleaseNames(), fetchReleaseNamesV2()]).then(
      ([names, namesV2]) => {
        if (names.data.data && namesV2.data) {
          setReleaseNames(
            names.data.data.names.concat(namesV2.data.data).sort()
          );
        }
      }
    );
  }, []);

  const handleDateTimeChange = date => {
    setScheduleDate(date);
    setDateTimePickerError(null);
  };

  const handleDateTimePickerError = error => {
    setDateTimePickerError(error);
  };

  const handleScheduleChangeDelete = async () => {
    const { error } = await deleteSC({
      scId: rule.sc_id,
      scDataVersion: rule.sc_data_version,
    });

    if (!error) {
      redirectWithRulesFilter(`ruleId=${rule.rule_id}`);
    }
  };

  const productSupportsField = field =>
    !(
      rule.product in RULE_PRODUCT_UNSUPPORTED_PROPERTIES &&
      RULE_PRODUCT_UNSUPPORTED_PROPERTIES[rule.product].includes(field)
    );
  const filterProductData = data =>
    pick(Object.keys(data).filter(productSupportsField), data);
  const handleCreateRule = async () => {
    const now = new Date();
    const when =
      scheduleDate >= now ? scheduleDate.getTime() : now.getTime() + 30000;
    const data = {
      alias: rule.alias,
      backgroundRate: rule.backgroundRate,
      buildID: rule.buildID,
      buildTarget: rule.buildTarget,
      channel: rule.channel,
      comment: rule.comment,
      distVersion: rule.distVersion,
      distribution: rule.distribution,
      fallbackMapping: rule.fallbackMapping,
      headerArchitecture: rule.headerArchitecture,
      instructionSet: rule.instructionSet,
      jaws: rule.jaws === EMPTY_MENU_ITEM_CHAR ? null : rule.jaws === 'true',
      locale: rule.locale,
      mapping: rule.mapping,
      memory: rule.memory,
      mig64: rule.mig64 === EMPTY_MENU_ITEM_CHAR ? null : rule.mig64 === 'true',
      osVersion: rule.osVersion,
      priority: rule.priority,
      product: rule.product,
      update_type: rule.update_type,
      version: rule.version,
    };
    const { data: response, error } = await addSC({
      change_type: 'insert',
      when,
      ...filterProductData(data),
    });

    if (!error) {
      redirectWithRulesFilter(`scId=${response.data.sc_id}`);
    }
  };

  const handleUpdateRule = async () => {
    const now = new Date();
    const when =
      scheduleDate >= now ? scheduleDate.getTime() : now.getTime() + 30000;
    const data = {
      alias: rule.alias,
      backgroundRate: rule.backgroundRate,
      buildID: rule.buildID,
      buildTarget: rule.buildTarget,
      channel: rule.channel,
      comment: rule.comment,
      distVersion: rule.distVersion,
      distribution: rule.distribution,
      fallbackMapping: rule.fallbackMapping,
      headerArchitecture: rule.headerArchitecture,
      instructionSet: rule.instructionSet,
      jaws: rule.jaws === EMPTY_MENU_ITEM_CHAR ? null : rule.jaws === 'true',
      locale: rule.locale,
      mapping: rule.mapping,
      memory: rule.memory,
      mig64: rule.mig64 === EMPTY_MENU_ITEM_CHAR ? null : rule.mig64 === 'true',
      osVersion: rule.osVersion,
      priority: rule.priority,
      product: rule.product,
      update_type: rule.update_type,
      version: rule.version,
    };

    if (hasScheduledChange) {
      const { error } = await updateSC({
        scId: rule.sc_id,
        sc_data_version: rule.sc_data_version,
        data_version: rule.data_version,
        when,
        ...filterProductData(data),
      });

      if (!error) {
        redirectWithRulesFilter(`scId=${rule.sc_id}`);
      }
    } else {
      const { data: response, error } = await addSC({
        rule_id: rule.rule_id,
        data_version: rule.data_version,
        change_type: 'update',
        when,
        ...filterProductData(data),
      });

      if (!error) {
        if (response.data.sc_id) {
          redirectWithRulesFilter(`scId=${response.data.sc_id}`);
        } else {
          redirectWithRulesFilter(`ruleId=${rule.rule_id}`);
        }
      }
    }
  };

  useEffect(() => {
    // Some fields (jaws and mig64 at the time of writing) are optional
    // boolean fields. Because input fields can't handle null or boolean
    // values, they get stored as EMPTY_MENU_ITEM_CHAR or a string
    // true/false when they change in the UI. In order to keep things
    // consistent, we do the same to the data fetched from the server.
    const getOptionalBooleanValue = current =>
      current === null ? EMPTY_MENU_ITEM_CHAR : String(current);

    if (!isNewRule) {
      Promise.all([
        fetchRule(ruleId),
        fetchScheduledChangeByRuleId(ruleId),
        fetchProducts(),
        fetchChannels(),
        fetchReleaseNames(),
        fetchReleaseNamesV2(),
      ]).then(([fetchedRuleResponse, fetchedSCResponse]) => {
        if (fetchedSCResponse.data.data.count > 0) {
          const sc = fetchedSCResponse.data.data.scheduled_changes[0];

          sc.jaws = getOptionalBooleanValue(sc.jaws);
          sc.mig64 = getOptionalBooleanValue(sc.mig64);

          setRule({
            ...rule,
            ...sc,
          });
          setScheduleDate(new Date(sc.when));
        } else {
          const r = fetchedRuleResponse.data.data;

          r.jaws = getOptionalBooleanValue(r.jaws);
          r.mig64 = getOptionalBooleanValue(r.mig64);

          setRule({
            ...rule,
            ...r,
          });
        }
      });
    } else {
      Promise.all([
        // Handles loading a scheduled change if an id was provided
        ruleId ? fetchRule(ruleId) : null,
        scId ? fetchScheduledChangeByScId(scId) : null,
        fetchProducts(),
        fetchChannels(),
        fetchReleaseNames(),
      ]).then(([ruleResponse, scResponse]) => {
        const r = ruleResponse ? ruleResponse.data.data : {};
        const sc = scResponse ? scResponse.data.data.scheduled_change : {};

        if (Object.keys(r).length > 0) {
          r.jaws = getOptionalBooleanValue(r.jaws);
          r.mig64 = getOptionalBooleanValue(r.mig64);
        }

        if (Object.keys(sc).length > 0) {
          sc.jaws = getOptionalBooleanValue(sc.jaws);
          sc.mig64 = getOptionalBooleanValue(sc.mig64);
        }

        setRule({
          ...rule,
          ...r,
          ...sc,
        });
      });
    }
  }, [ruleId, scId]);

  const today = new Date();

  // This will make sure the helperText
  // will always be displayed for a "today" date
  today.setHours(0, 0, 0, 0);

  // To avoid nested ternary
  const getTitle = () => {
    if (isNewRule) {
      if (scId) {
        return `Update Scheduled Rule ${scId}${
          rule.alias ? ` (${rule.alias})` : ''
        }`;
      }

      return 'Create Rule';
    }

    return `Update Rule ${ruleId}${rule.alias ? ` (${rule.alias})` : ''}`;
  };

  const [requiredSignoffs, fetchRequiredSignoffs] =
  useAction(getRequiredSignoffs);

  useEffect(() => {
    let myPromise = new Promise((res) => {
      res(fetchRequiredSignoffs(OBJECT_NAMES.PRODUCT_REQUIRED_SIGNOFF));
    });
    myPromise.then((rs) => {
      setAllrequiredSignoffs(rs.data.data.required_signoffs);
    });
  }, []);

  // SignOff style
  const signoffStyle = {
    div: {
      display: "flex",
      flexFlow: "row wrap",
      width: "100%",
      margin: "8px 0 8px 0",
      alignItems: "center",
    },
    p1: {
      marginRight: "8px",
      color: "gray",
    },
    p2: {
      color: "black",
    },
  };

  return (
    <Dashboard title={getTitle()}>
    {isLoading && <Spinner loading />}
    {error && <ErrorPanel fixed error={error} />}
    {!isLoading && (
      /*
      THE SIGN OFF DETAIL SHOULD GO JUST UNDERNEATH THE OPENING FRAGMENT
      It should be in the form : 
      "SignOffs Required : 1 signoff from a releng user" 
      */
      <Fragment>
        {/* SHOWS REQUIRED SIGNOFFS */}
        <div style={signoffStyle.div}>
          <Typography component="p" variant="body2" style={signoffStyle.p1}>Required Signoff(s) :</Typography>
          {allRequiredSignOffs.map((reqSignOff, index, all) => {
            if (
              rule.product === reqSignOff.product &&
              rule.channel === `${reqSignOff.channel}*`
            ) {
              return (
                <Typography component="p" variant="body2" key={index} style={signoffStyle.p2}>{`${
                  reqSignOff.signoffs_required
                } member${reqSignOff.count > 1 ? "s" : ""} of ${
                  reqSignOff.role
                }${all[index + 1] ? "," : ""}`}</Typography>
              );
            } else {
              return (
                <Typography component="p" variant="body2" key={index} style={signoffStyle.p2}>
                  No signoffs provided for this product in local development
                </Typography>
              );
            }
          })}
          {/* END OF REQUIRED SIGNOFFS INFO */}
        </div>
        <div className={classes.scheduleDiv}>
            <DateTimePicker
              todayLabel="ASAP"
              disablePast
              inputVariant="outlined"
              fullWidth
              label="When"
              onError={handleDateTimePickerError}
              helperText={
                dateTimePickerError ||
                (scheduleDate < new Date()
                  ? 'This will be scheduled for ASAP'
                  : undefined)
              }
              onDateTimeChange={handleDateTimeChange}
              value={scheduleDate}
            />
          </div>
          <Grid container spacing={4}>
            <Grid item xs={12} sm={6}>
              <AutoCompleteText
                value={defaultToEmptyString(rule.product)}
                onValueChange={handleProductChange}
                getSuggestions={
                  products.data &&
                  getSuggestions(products.data.data.product.sort())
                }
                label="Product"
                required
                inputProps={{
                  autoFocus: true,
                  fullWidth: true,
                }}
              />
            </Grid>
            {productSupportsField('channel') && (
              <Grid item xs={12} sm={6}>
                <AutoCompleteText
                  value={defaultToEmptyString(rule.channel)}
                  onValueChange={handleChannelChange}
                  getSuggestions={
                    channels.data &&
                    getSuggestions(channels.data.data.channel.sort())
                  }
                  label="Channel"
                  required
                  inputProps={{
                    fullWidth: true,
                  }}
                />
              </Grid>
            )}
            {productSupportsField('mapping') && (
              <Grid item xs={12} sm={6}>
                <AutoCompleteText
                  value={defaultToEmptyString(rule.mapping)}
                  onValueChange={handleMappingChange}
                  getSuggestions={getSuggestions(releaseNames)}
                  label="Mapping"
                  required
                  inputProps={{
                    fullWidth: true,
                  }}
                />
              </Grid>
            )}
            {productSupportsField('fallbackMapping') && (
              <Grid item xs={12} sm={6}>
                <AutoCompleteText
                  value={defaultToEmptyString(rule.fallbackMapping)}
                  onValueChange={handleFallbackMappingChange}
                  getSuggestions={getSuggestions(releaseNames)}
                  label="Fallback Mapping"
                  inputProps={{
                    fullWidth: true,
                  }}
                />
              </Grid>
            )}
            {productSupportsField('backgroundRate') && (
              <Grid item xs={12} sm={6}>
                <NumberFormat
                  allowNegative={false}
                  label="Background Rate"
                  fullWidth
                  value={rule.backgroundRate}
                  customInput={TextField}
                  onValueChange={handleNumberChange('backgroundRate')}
                  decimalScale={0}
                />
              </Grid>
            )}
            {productSupportsField('priority') && (
              <Grid item xs={12} sm={6}>
                <NumberFormat
                  allowNegative={false}
                  label="Priority"
                  fullWidth
                  value={defaultToEmptyString(rule.priority)}
                  customInput={TextField}
                  onValueChange={handleNumberChange('priority')}
                  decimalScale={0}
                />
              </Grid>
            )}
            {productSupportsField('version') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Version"
                  value={defaultToEmptyString(rule.version)}
                  name="version"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('buildID') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Build ID"
                  value={defaultToEmptyString(rule.buildID)}
                  name="buildID"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('locale') && (
              <Grid item xs={12} md={6}>
                <TextField
                  helperText="Enter each locale on its own line"
                  multiline
                  rows={4}
                  fullWidth
                  label="Locale"
                  value={localeTextValue}
                  name="locale"
                  onChange={handleTextFieldWithNewLinesChange}
                />
              </Grid>
            )}
            {productSupportsField('osVersion') && (
              <Grid item xs={12} md={6}>
                <TextField
                  helperText="Enter each OS version on its own line"
                  multiline
                  rows={4}
                  fullWidth
                  label="OS Version"
                  value={osVersionTextValue}
                  name="osVersion"
                  onChange={handleTextFieldWithNewLinesChange}
                />
              </Grid>
            )}
            {productSupportsField('buildTarget') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Build Target"
                  value={defaultToEmptyString(rule.buildTarget)}
                  name="buildTarget"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('instructionSet') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Instruction Set"
                  value={defaultToEmptyString(rule.instructionSet)}
                  name="instructionSet"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('memory') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Memory"
                  value={defaultToEmptyString(rule.memory)}
                  name="memory"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('jaws') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Incompatible JAWS Screen Reader"
                  select
                  value={rule.jaws || EMPTY_MENU_ITEM_CHAR}
                  name="jaws"
                  onChange={handleInputChange}>
                  <MenuItem value={EMPTY_MENU_ITEM_CHAR}>
                    {EMPTY_MENU_ITEM_CHAR}
                  </MenuItem>
                  <MenuItem value="true">Yes</MenuItem>
                  <MenuItem value="false">No</MenuItem>
                </TextField>
              </Grid>
            )}
            {productSupportsField('distribution') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Distribution"
                  value={defaultToEmptyString(rule.distribution)}
                  name="distribution"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('distVersion') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Distribution Version"
                  value={defaultToEmptyString(rule.distVersion)}
                  name="distVersion"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('headerArchitecture') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Header Architecture"
                  value={defaultToEmptyString(rule.headerArchitecture)}
                  name="headerArchitecture"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('mig64') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="64-bit Migration Opt-in"
                  select
                  value={rule.mig64 || EMPTY_MENU_ITEM_CHAR}
                  name="mig64"
                  onChange={handleInputChange}>
                  <MenuItem value={EMPTY_MENU_ITEM_CHAR}>
                    {EMPTY_MENU_ITEM_CHAR}
                  </MenuItem>
                  <MenuItem value="true">Yes</MenuItem>
                  <MenuItem value="false">No</MenuItem>
                </TextField>
              </Grid>
            )}
            {productSupportsField('alias') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Alias"
                  value={defaultToEmptyString(rule.alias)}
                  name="alias"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
            {productSupportsField('update_type') && (
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  select
                  required
                  label="Update Type"
                  value={rule.update_type || 'minor'}
                  name="update_type"
                  onChange={handleInputChange}>
                  <MenuItem value="minor">minor</MenuItem>
                  <MenuItem value="major">major</MenuItem>
                </TextField>
              </Grid>
            )}
            {productSupportsField('comment') && (
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="Comment"
                  value={defaultToEmptyString(rule.comment)}
                  name="comment"
                  onChange={handleInputChange}
                />
              </Grid>
            )}
          </Grid>
        </Fragment>
      )}
      {!isLoading && (
        <Fragment>
          <Tooltip title={isNewRule && !scId ? 'Create Rule' : 'Update Rule'}>
            {/* Add <div /> to avoid material-ui error "you are providing
              a disabled `button` child to the Tooltip component." */}
            <div
              className={classNames(classes.fabWithTooltip, {
                [classes.secondFab]: hasScheduledChange,
                [classes.fab]: !hasScheduledChange,
              })}>
              <Fab
                disabled={!user || actionLoading}
                onClick={
                  isNewRule && !scId ? handleCreateRule : handleUpdateRule
                }
                color="primary">
                <ContentSaveIcon />
              </Fab>
            </div>
          </Tooltip>
          {hasScheduledChange && (
            <SpeedDial
              FabProps={{ disabled: !user || actionLoading }}
              ariaLabel="Secondary Actions">
              <SpeedDialAction
                FabProps={{ disabled: actionLoading }}
                icon={<DeleteIcon />}
                tooltipOpen
                tooltipTitle="Cancel Pending Change"
                onClick={handleScheduleChangeDelete}
              />
            </SpeedDial>
          )}
        </Fragment>
      )}
    </Dashboard>
  );
}

Rule.propTypes = {
  isNewRule: bool,
};

Rule.defaultProps = {
  isNewRule: false,
};

export default withUser(Rule);
