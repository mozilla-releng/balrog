import React, { useMemo, useState, useEffect } from 'react';
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
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import ReleaseCard from '../../../components/ReleaseCard';
import useAction from '../../../hooks/useAction';
import Link from '../../../utils/Link';
import {
  getReleases,
  getRelease,
  deleteRelease,
  setReadOnly,
  getScheduledChanges,
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
  const [releasesAction, fetchReleases] = useAction(getReleases);
  const [releaseAction, fetchRelease] = useAction(getRelease);
  const [scheduledChangesAction, fetchScheduledChanges] = useAction(
    getScheduledChanges
  );
  const delRelease = useAction(deleteRelease)[1];
  const setReadOnlyFlag = useAction(setReadOnly)[1];
  const [signoffAction, signoff] = useAction(props =>
    makeSignoff({ type: 'releases', ...props })
  );
  const [revokeAction, revoke] = useAction(props =>
    revokeSignoff({ type: 'releases', ...props })
  );
  const [rolesAction, fetchRoles] = useAction(getUserInfo);
  const isLoading = releasesAction.loading || scheduledChangesAction.loading;
  // eslint-disable-next-line prefer-destructuring
  const error =
    releasesAction.error ||
    scheduledChangesAction.error ||
    rolesAction.error ||
    releaseAction.error ||
    revokeAction.error ||
    (roles.length === 1 && signoffAction.error);
  const filteredReleases = useMemo(() => {
    if (!releases) {
      return [];
    }

    if (!searchValue) {
      return releases;
    }

    return releases.filter(release =>
      release.name.toLowerCase().includes(searchValue.toLowerCase())
    );
  }, [releases, searchValue]);
  const filteredReleasesCount = filteredReleases.length;
  const handleSignoffRoleChange = ({ target: { value } }) =>
    setSignoffRole(value);

  useEffect(() => {
    Promise.all([fetchReleases(), fetchScheduledChanges()]).then(
      ([relData, scData]) => {
        setReleases(
          relData.data.data.releases.map(r => {
            const sc = scData.data.data.scheduled_changes.find(
              sc => r.name === sc.name
            );
            const release = clone(r);

            if (sc) {
              release.scheduledChange = sc;
              release.scheduledChange.when = new Date(
                release.scheduledChange.when
              );
            }

            // todo: set these
            release.required_signoffs = {};

            return release;
          })
        );
      }
    );
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

  const handleReadOnlySubmit = async () => {
    const release = dialogState.item;
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

  const handleReadOnlyComplete = result => {
    setReleases(
      releases.map(r => {
        if (r.name !== result.name) {
          return r;
        }

        const ret = clone(r);

        ret.read_only = !r.read_only;
        ret.data_version = result.new_data_version;

        return ret;
      })
    );

    handleDialogClose();
  };

  const handleDeleteSubmit = async () => {
    const release = dialogState.item;
    const { error } = await delRelease({
      name: release.name,
      dataVersion: release.data_version,
    });

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

        const newRelease = { ...r };

        newRelease.scheduledChange.signoffs[username] = roleToSignoffWith;

        return newRelease;
      })
    );
  };

  const doSignoff = async (roleToSignoffWith, release) => {
    const { error } = await signoff({
      scId: release.scheduledChange.sc_id,
      role: roleToSignoffWith,
    });

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

  const accessChangeDialogBody =
    dialogState.item &&
    `This would make ${dialogState.item.name} ${
      dialogState.item.read_only ? 'writable' : 'read only'
    }.`;
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
    const { error } = await revoke({
      scId: release.scheduledChange.sc_id,
      role: release.scheduledChange.signoffs[username],
    });

    if (!error) {
      setReleases(
        releases.map(r => {
          if (
            !r.scheduledChange ||
            r.scheduledChange.sc_id !== release.scheduledChange.sc_id
          ) {
            return r;
          }

          const newRelease = { ...r };

          delete newRelease.scheduledChange.signoffs[username];

          return newRelease;
        })
      );
    }
  };

  const handleViewScheduledChangeDiff = async release => {
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
      ruleIdsLineCount * body2TextHeight() +
      2 * listItemTextMargin;

    // actions row
    height += buttonHeight + theme.spacing(2);
    // space below the card (margin)
    height += theme.spacing(6);

    if (release.scheduledChange && release.scheduledChange.sc_id) {
      // divider
      height += theme.spacing(2) + 1;

      // Scheduled changes row, which includes some text, a button, and a chip.
      // Which one is largest depends on platform/browser.
      height += Math.max(subtitle1TextHeight(), theme.spacing(3), buttonHeight);

      if (Object.keys(release.scheduledChange.required_signoffs).length > 0) {
        const requiredRoles = Object.keys(
          release.scheduledChange.required_signoffs
        ).length;
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
        placeholder="Search a release..."
        onChange={handleSearchChange}
        value={searchValue}
      />
      {isLoading && <Spinner loading />}
      {error && <ErrorPanel fixed error={error} />}
      {!isLoading && filteredReleases && (
        <VariableSizeList
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
        <Link to="/releases/create">
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
