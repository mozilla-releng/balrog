import React, { useMemo, useState, useEffect, useRef, Fragment } from 'react';
import { clone } from 'ramda';
import classNames from 'classnames';
import PlusIcon from 'mdi-react/PlusIcon';
import { makeStyles, useTheme } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import Drawer from '@material-ui/core/Drawer';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { Typography } from '@material-ui/core';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import MessagePanel from '../../../components/MessagePanel';
import ReleaseCard from '../../../components/ReleaseCard';
import useAction from '../../../hooks/useAction';
import Link from '../../../utils/Link';
import {
  getReleases,
  getReleasesV2,
  getRelease,
  getReleaseV2,
  deleteReleaseV2,
  setReadOnlyV2,
  deleteRelease,
  setReadOnly,
  getScheduledChanges,
  getScheduledChangeById,
  addScheduledChange,
  getRequiredSignoffsForProduct,
  makeSignoffV2,
  revokeSignoffV2,
} from '../../../services/releases';
import { getUserInfo } from '../../../services/users';
import { makeSignoff, revokeSignoff } from '../../../services/signoffs';
import VariableSizeList from '../../../components/VariableSizeList';
import SearchBar from '../../../components/SearchBar';
import DialogAction from '../../../components/DialogAction';
import DiffRelease from '../../../components/DiffRelease';
import Snackbar from '../../../components/Snackbar';
import {
  CONTENT_MAX_WIDTH,
  DIALOG_ACTION_INITIAL_STATE,
  SNACKBAR_INITIAL_STATE,
  RELEASE_ROOT_LEVEL_KEY,
} from '../../../utils/constants';
import { withUser } from '../../../utils/AuthContext';
import elementsHeight from '../../../utils/elementsHeight';

const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  releaseCard: {
    margin: 2,
  },
  releaseCardSelected: {
    border: `2px solid ${theme.palette.primary.light}`,
  },
  drawerPaper: {
    maxWidth: CONTENT_MAX_WIDTH,
    margin: '0 auto',
    padding: theme.spacing(1),
    maxHeight: '80vh',
  },
}));

function ListReleases(props) {
  const classes = useStyles();
  const theme = useTheme();
  const username = (props.user && props.user.email) || '';
  const {
    buttonHeight,
    body1TextHeight,
    body2TextHeight,
    h6TextHeight,
    subtitle1TextHeight,
    signoffSummarylistSubheaderTextHeight,
  } = elementsHeight(theme);
  const releaseListRef = useRef(null);
  const { hash } = props.location;
  const [releaseNameHash, setReleaseNameHash] = useState(null);
  const [scrollToRow, setScrollToRow] = useState(null);
  const [searchValue, setSearchValue] = useState('');
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [snackbarState, setSnackbarState] = useState(SNACKBAR_INITIAL_STATE);
  const [releases, setReleases] = useState([]);
  const [roles, setRoles] = useState([]);
  const [signoffRole, setSignoffRole] = useState('');
  const [drawerState, setDrawerState] = useState({ open: false, item: {} });
  const [matchHighlight, setMatchHighlight] = useState({});
  const [requiredSignoffsForProduct, setRequiredSignoffsForProduct] = useState(
    null
  );
  const [releasesAction, fetchReleases] = useAction(getReleases);
  const [releasesV2Action, fetchReleasesV2] = useAction(getReleasesV2);
  const [releaseAction, fetchRelease] = useAction(getRelease);
  const [releaseV2Action, fetchReleaseV2] = useAction(getReleaseV2);
  const [scheduledChangesAction, fetchScheduledChanges] = useAction(
    getScheduledChanges
  );
  const delRelease = useAction(deleteRelease)[1];
  const delReleaseV2 = useAction(deleteReleaseV2)[1];
  const setReadOnlyFlag = useAction(setReadOnly)[1];
  const setReadOnlyFlagV2 = useAction(setReadOnlyV2)[1];
  const [signoffAction, signoff] = useAction(props =>
    makeSignoff({ type: 'releases', ...props })
  );
  const [revokeAction, revoke] = useAction(props =>
    revokeSignoff({ type: 'releases', ...props })
  );
  const [signoffV2Action, signoffV2] = useAction(makeSignoffV2);
  const [revokeV2Action, revokeV2] = useAction(revokeSignoffV2);
  const [rolesAction, fetchRoles] = useAction(getUserInfo);
  const isLoading =
    releasesAction.loading ||
    releasesV2Action.loading ||
    scheduledChangesAction.loading;
  const error =
    releasesAction.error ||
    releasesV2Action.error ||
    scheduledChangesAction.error ||
    rolesAction.error ||
    releaseAction.error ||
    releaseV2Action.error ||
    revokeAction.error ||
    revokeV2Action.error ||
    (roles.length === 1 && signoffAction.error) ||
    (roles.length === 1 && signoffV2Action.error);
  const filteredReleases = useMemo(() => {
    if (!releases) {
      return [];
    }

    if (!searchValue) {
      return releases;
    }

    const values = searchValue.trim().split(' ');
    const regexp = values.reduce(
      (re, value) => `${re}[A-Za-z0-9.-]*(${value})`,
      ''
    );

    return releases.filter(release => {
      const regex = new RegExp(regexp, 'dgi');
      const matches = regex.exec(release.name);

      if (matches) {
        const toHighlight = matches.indices;

        setMatchHighlight(prevState => ({
          ...prevState,
          [release.name]: toHighlight,
        }));
      }

      return matches;
    });
  }, [releases, searchValue]);
  const filteredReleasesCount = filteredReleases.length;
  const handleSignoffRoleChange = ({ target: { value } }) =>
    setSignoffRole(value);
  const requiresSignoffs = release =>
    release.required_signoffs &&
    Object.entries(release.required_signoffs).length > 0;
  const requiresSignoffsChangeReadOnly = release =>
    requiresSignoffs(release) ||
    (requiredSignoffsForProduct[release.product] &&
      Object.entries(requiredSignoffsForProduct[release.product]).length > 0);
  const getRequiredSignoffsChangeReadOnly = release =>
    requiresSignoffs(release)
      ? release.required_signoffs
      : requiredSignoffsForProduct[release.product];
  const buildScheduledChange = sc => {
    const scheduledChange = sc;

    scheduledChange.when = new Date(sc.when);

    return scheduledChange;
  };

  const buildScheduledChangeV2 = (rel, scheduledChanges) => {
    // V2 API Releases can have multiple scheduled changes, but they are
    // generally treated as one larger unit. We can safely take most of the
    // metadata from one, as it applies to all of them.
    // read_only is slightly special in that it may exist either on exactly 1
    // scheduled change, or zero. To handle this, we default to the current
    // state of it on the actual Release, and override below if it is found.
    const scheduledChange = {
      signoffs: scheduledChanges[0].signoffs,
      read_only: rel.read_only,
      when: new Date(scheduledChanges[0].when),
      change_type: scheduledChanges[0].change_type,
    };

    scheduledChanges.forEach(sc => {
      if ('read_only' in sc && sc.read_only !== rel.read_only) {
        scheduledChange.read_only = sc.read_only;
      }
    });

    return scheduledChange;
  };

  useEffect(() => {
    Promise.all([
      fetchReleases(),
      fetchScheduledChanges(),
      fetchReleasesV2(),
    ]).then(([relData, scData, relV2Data]) => {
      setReleases(
        // Releases may only exist in either the old or new API, not both,
        // so we can concat the results together.
        relData.data.data.releases
          .map(r => {
            const sc = scData.data.data.scheduled_changes.find(
              sc => r.name === sc.name
            );
            const release = clone(r);

            release.api_version = 1;

            if (sc) {
              release.scheduledChange = buildScheduledChange(sc);
            }

            return release;
          })
          .concat(
            relV2Data.data.data.releases.map(r => {
              // V2 data is largely the same as V1, but we need to
              // massage the scheduled changes a little bit, so it's
              // easiest to create a new Object and copy over what we
              // need.
              const release = {
                name: r.name,
                data_version: r.data_version,
                product: r.product,
                read_only: r.read_only,
                rule_info: r.rule_info,
                required_signoffs: r.required_signoffs,
                product_required_signoffs: r.product_required_signoffs,
                api_version: 2,
              };

              if (r.scheduled_changes.length > 0) {
                release.scheduledChange = buildScheduledChangeV2(
                  r,
                  r.scheduled_changes
                );
              }

              return release;
            })
          )
      );
    });
  }, []);

  useEffect(() => {
    if (!requiredSignoffsForProduct && releases.length > 0) {
      const productsReleases = releases.reduce((acc, release) => {
        const pr = acc;

        if (release.product in pr) return pr;

        // Required signoffs for product will be fetched only when the current
        // release does not have the required signoffs information.
        if (!requiresSignoffs(release)) {
          pr[release.product] = release.name;
        }

        return pr;
      }, {});
      // Releases that are not associated to rules, will not have required
      // signoffs information, in this scenario, to turn release as modifiable,
      // it is necessary get required signoff for the release product.
      // How it is a very specific release logic, the endpoint gets
      // the release name and infers the product to evaluate the signoffs.
      // Once required signoffs for product was evaluated for a given product,
      // it is not necessary evaluate again, so to get the signoffs,
      // one release is enougth.
      const signoffsForProductRequests = Object.entries(
        productsReleases
      ).map(async ([product, name]) =>
        getRequiredSignoffsForProduct(name).then(response => [
          product,
          response.data.required_signoffs,
        ])
      );

      Promise.all(signoffsForProductRequests).then(requests => {
        setRequiredSignoffsForProduct(
          requests.reduce((acc, [product, rs]) => {
            const rsfp = acc;

            rsfp[product] = rs;

            return rsfp;
          }, {})
        );
      });
    }
  }, [releases]);

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
    if (hash !== releaseNameHash && filteredReleasesCount) {
      const name = hash.replace('#', '') || null;

      if (name) {
        const itemNumber = filteredReleases
          .map(release => release.name)
          .indexOf(name);

        setScrollToRow(itemNumber);
        setReleaseNameHash(hash);
      }
    }
  }, [hash, releaseNameHash, filteredReleases]);

  const handleDrawerClose = () => {
    setDrawerState({
      ...drawerState,
      open: false,
    });
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

  const handleSearchChange = ({ target: { value } }) => {
    setSearchValue(value);
  };

  const handleDialogClose = () => {
    setDialogState({
      ...dialogState,
      open: false,
    });
  };

  const handleDialogExited = () => {
    setDialogState(DIALOG_ACTION_INITIAL_STATE);
  };

  const handleDialogError = error => {
    setDialogState({
      ...dialogState,
      error,
    });
  };

  const scheduleReadWriteChange = async release => {
    const sc = {
      change_type: 'update',
      when: new Date().getTime() + 30000,
      name: release.name,
      product: release.product,
      read_only: false,
      data_version: release.data_version,
    };
    const { data, error } = await addScheduledChange(sc);

    if (error) throw error;

    const { data: scData, error: scError } = await getScheduledChangeById(
      data.sc_id
    );

    if (scError) throw scError;

    return { name: release.name, sc: scData.scheduled_change };
  };

  const updateReadonlyFlag = async release => {
    const { error, data } = await setReadOnlyFlag({
      name: release.name,
      readOnly: !release.read_only,
      dataVersion: release.data_version,
    });

    if (error) {
      throw error;
    }

    return { name: release.name, new_data_version: data.data.new_data_version };
  };

  const updateReadOnlyFlagV2 = async release => {
    const { error, data } = await setReadOnlyFlagV2(
      release.name,
      !release.read_only,
      release.data_version
    );

    if (error) {
      throw error;
    }

    return { name: release.name, ...data.data };
  };

  const handleReadOnlySubmit = async () => {
    const release = dialogState.item;

    if (release.api_version === 1) {
      if (release.read_only && requiresSignoffsChangeReadOnly(release)) {
        return scheduleReadWriteChange(release);
      }

      return updateReadonlyFlag(release);
    }

    return updateReadOnlyFlagV2(release);
  };

  const handleReadOnlyComplete = result => {
    setReleases(
      releases.map(r => {
        if (r.name !== result.name) {
          return r;
        }

        const ret = clone(r);

        if (r.api_version === 1) {
          if (result.sc) {
            ret.scheduledChange = buildScheduledChange(result.sc);
          } else {
            ret.read_only = !r.read_only;
            ret.data_version = result.new_data_version;
          }
        } else if (result[RELEASE_ROOT_LEVEL_KEY].sc_id) {
          ret.scheduledChange = buildScheduledChangeV2(ret, [
            result[RELEASE_ROOT_LEVEL_KEY],
          ]);
          ret.scheduledChange.read_only = !r.read_only;
        } else {
          ret.read_only = !r.read_only;
          ret.data_version = result[RELEASE_ROOT_LEVEL_KEY];
        }

        return ret;
      })
    );

    if (result.sc) {
      releaseListRef.current.recomputeRowHeights();
    }

    handleDialogClose();
  };

  const handleDeleteSubmit = async () => {
    const release = dialogState.item;
    let error = null;

    if (release.api_version === 1) {
      ({ error } = await delRelease({
        name: release.name,
        dataVersion: release.data_version,
      }));
    } else {
      ({ error } = await delReleaseV2(release.name));
    }

    if (error) {
      throw error;
    }

    return release.name;
  };

  const handleDeleteComplete = name => {
    setReleases(releases.filter(r => r.name !== name));
    handleSnackbarOpen({
      message: `${name} deleted`,
    });

    handleDialogClose();
  };

  const updateSignoffs = ({ roleToSignoffWith, release }) => {
    setReleases(
      releases.map(r => {
        if (
          !r.scheduledChange ||
          r.scheduledChange.sc_id !== release.scheduledChange.sc_id
        ) {
          return r;
        }

        const newRelease = clone(r);

        newRelease.scheduledChange.signoffs[username] = roleToSignoffWith;

        return newRelease;
      })
    );
  };

  const doSignoff = async (roleToSignoffWith, release) => {
    if (release.api_version === 1) {
      const { error } = await signoff({
        scId: release.scheduledChange.sc_id,
        role: roleToSignoffWith,
      });

      return { error, result: { roleToSignoffWith, release } };
    }

    const { error } = await signoffV2(release.name, roleToSignoffWith);

    return { error, result: { roleToSignoffWith, release } };
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

  const accessChangeDialogBody = dialogState.item && (
    <Fragment>
      <Typography component="p" gutterBottom paragraph>
        This would make {dialogState.item.name}&nbsp;
        {dialogState.item.read_only ? 'writable' : 'read only'}
      </Typography>
      {dialogState.item.read_only &&
        requiresSignoffsChangeReadOnly(dialogState.item) && (
          <MessagePanel
            variant="warning"
            alwaysOpen
            message={`Changes will require signoffs: ${Object.entries(
              getRequiredSignoffsChangeReadOnly(dialogState.item)
            )
              .map(([role, count]) => `${count} from ${role}`)
              .join(', ')}.`}
          />
        )}
    </Fragment>
  );
  const handleAccessChange = ({ release, checked }) => {
    setDialogState({
      ...dialogState,
      open: true,
      title: checked ? 'Read Only?' : 'Read/Write?',
      confirmText: 'Yes',
      destructive: false,
      item: release,
      mode: 'accessChange',
      handleSubmit: handleReadOnlySubmit,
      handleComplete: handleReadOnlyComplete,
    });
  };

  const deleteDialogBody =
    dialogState.item && `This will delete ${dialogState.item.name}`;
  const handleDelete = release => {
    setDialogState({
      ...dialogState,
      open: true,
      title: 'Delete Release?',
      confirmText: 'Delete',
      item: release,
      destructive: true,
      mode: 'delete',
      handleSubmit: handleDeleteSubmit,
      handleComplete: handleDeleteComplete,
    });
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
  const handleSignoff = async release => {
    if (roles.length === 1) {
      const { error, result } = await doSignoff(roles[0], release);

      if (!error) {
        updateSignoffs(result);
      }
    } else {
      setDialogState({
        ...dialogState,
        open: true,
        destructive: false,
        title: 'Signoff as…',
        confirmText: 'Sign off',
        item: release,
        mode: 'signoff',
        handleSubmit: handleSignoffDialogSubmit,
        handleComplete: handleSignoffDialogComplete,
      });
    }
  };

  const handleRevoke = async release => {
    let error = null;

    if (release.api_version === 1) {
      ({ error } = await revoke({
        scId: release.scheduledChange.sc_id,
        role: release.scheduledChange.signoffs[username],
      }));
    } else {
      ({ error } = await revokeV2(release.name));
    }

    if (!error) {
      setReleases(
        releases.map(r => {
          if (
            !r.scheduledChange ||
            r.scheduledChange.sc_id !== release.scheduledChange.sc_id
          ) {
            return r;
          }

          const newRelease = clone(r);

          delete newRelease.scheduledChange.signoffs[username];

          return newRelease;
        })
      );
    }
  };

  const handleViewScheduledChangeDiff = async release => {
    if (release.api_version === 1) {
      const result = await fetchRelease(release.name);

      setDrawerState({
        ...drawerState,
        item: {
          firstRelease: result.data.data,
          secondRelease: release.scheduledChange.data,
          firstFilename: `Data Version: ${release.data_version}`,
          secondFilename: 'Scheduled Change',
        },
        open: true,
      });
    } else {
      const result = await fetchReleaseV2(release.name);

      setDrawerState({
        ...drawerState,
        item: {
          firstRelease: result.data.data.blob,
          secondRelease: result.data.data.sc_blob,
          firstFilename: `Current Version`,
          secondFilename: 'Scheduled Change',
        },
        open: true,
      });
    }
  };

  const Row = ({ index, style }) => {
    const release = filteredReleases[index];
    const isSelected = Boolean(hash && hash.replace('#', '') === release.name);

    return (
      <div key={release.name} style={style}>
        <ReleaseCard
          className={classNames(classes.releaseCard, {
            [classes.releaseCardSelected]: isSelected,
          })}
          release={release}
          releaseHighlight={matchHighlight && matchHighlight[release.name]}
          onAccessChange={handleAccessChange}
          onReleaseDelete={handleDelete}
          onViewScheduledChangeDiff={handleViewScheduledChangeDiff}
          onSignoff={() => handleSignoff(release)}
          onRevoke={() => handleRevoke(release)}
        />
      </div>
    );
  };

  const getRowHeight = ({ index }) => {
    const listItemTextMargin = 6;
    const release = filteredReleases[index];
    // An approximation
    const ruleIdsLineCount =
      Math.ceil(Object.keys(release.rule_info).length / 10) || 1;
    // card header
    let height = h6TextHeight + body1TextHeight() + theme.spacing(2);

    // list padding top and bottom
    height += theme.spacing(2);

    // first row (data version) + ListItemText margins
    height += body1TextHeight() + body2TextHeight() + 2 * listItemTextMargin;

    // rule ids row + ListItemText margins
    height +=
      body1TextHeight() +
      // Height of <Chip size="small" ... /> is hard-coded to 24px
      // https://github.com/mui-org/material-ui/blob/b968c9a375d2d71745fa0165ac0d8d77bef74bc6/packages/material-ui/src/Chip/Chip.js#L46
      ruleIdsLineCount * (24 + theme.spacing(1)) +
      2 * listItemTextMargin;

    // actions row
    height += buttonHeight + theme.spacing(2);
    // space below the card (margin)
    height += theme.spacing(4);

    if (release.scheduledChange && release.scheduledChange.when) {
      // divider
      height += theme.spacing(2) + 1;

      // Scheduled changes row, which includes some text, a button, and a chip.
      // Which one is largest depends on platform/browser.
      height += Math.max(subtitle1TextHeight(), theme.spacing(3), buttonHeight);

      if (Object.keys(release.required_signoffs).length > 0) {
        const requiredRoles = Object.keys(release.required_signoffs).length;
        const nSignoffs = Object.keys(release.scheduledChange.signoffs).length;
        // Required Roles and Signoffs are beside one another, so we only
        // need to account for the one with the most items.
        const signoffRows = Math.max(requiredRoles, nSignoffs);

        // Padding above the summary
        height += theme.spacing(2);

        // The "Requires Signoff From" title and the margin beneath it
        height += signoffSummarylistSubheaderTextHeight + theme.spacing(0.5);

        // Space for however many rows exist.
        height += signoffRows * (body2TextHeight() + theme.spacing(0.5));

        // Padding below the summary
        height += theme.spacing(1);
      }
    }

    return height;
  };

  const getDialogBody = () => {
    if (dialogState.mode === 'delete') {
      return deleteDialogBody;
    }

    if (dialogState.mode === 'signoff') {
      return signoffDialogBody;
    }

    return accessChangeDialogBody;
  };

  const getDialogSubmit = () => {
    if (dialogState.mode === 'delete') {
      return handleDeleteSubmit;
    }

    if (dialogState.mode === 'signoff') {
      return handleSignoffDialogSubmit;
    }

    return handleReadOnlySubmit;
  };

  const getDialogComplete = () => {
    if (dialogState.mode === 'delete') {
      return handleDeleteComplete;
    }

    if (dialogState.mode === 'signoff') {
      return handleSignoffDialogComplete;
    }

    return handleReadOnlyComplete;
  };

  return (
    <Dashboard title="Releases">
      <SearchBar
        placeholder="Search a release…"
        onChange={handleSearchChange}
        value={searchValue}
      />
      {isLoading && <Spinner loading />}
      {error && <ErrorPanel fixed error={error} />}
      {!isLoading && filteredReleases && (
        <VariableSizeList
          ref={releaseListRef}
          rowRenderer={Row}
          scrollToRow={scrollToRow}
          rowHeight={getRowHeight}
          rowCount={filteredReleasesCount}
        />
      )}
      <DialogAction
        open={dialogState.open}
        title={dialogState.title}
        destructive={dialogState.destructive}
        body={getDialogBody()}
        error={dialogState.error}
        confirmText={dialogState.confirmText}
        onSubmit={getDialogSubmit()}
        onClose={handleDialogClose}
        onExited={handleDialogExited}
        onError={handleDialogError}
        onComplete={getDialogComplete()}
      />
      <Drawer
        classes={{ paper: classes.drawerPaper }}
        anchor="bottom"
        open={drawerState.open}
        onClose={handleDrawerClose}>
        <DiffRelease
          firstRelease={drawerState.item.firstRelease}
          secondRelease={drawerState.item.secondRelease}
          firstFilename={drawerState.item.firstFilename}
          secondFilename={drawerState.item.secondFilename}
        />
      </Drawer>
      <Snackbar onClose={handleSnackbarClose} {...snackbarState} />
      {!isLoading && (
        <Link to="/releases/create/v2">
          <Tooltip title="Add Release">
            <Fab color="primary" className={classes.fab}>
              <PlusIcon />
            </Fab>
          </Tooltip>
        </Link>
      )}
    </Dashboard>
  );
}

export default withUser(ListReleases);
