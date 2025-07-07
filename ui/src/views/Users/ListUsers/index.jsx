import React, { Fragment, useState, useEffect } from 'react';
import { clone } from 'ramda';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { makeStyles } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import PlusIcon from 'mdi-react/PlusIcon';
import Dashboard from '../../../components/Dashboard';
import DialogAction from '../../../components/DialogAction';
import ErrorPanel from '../../../components/ErrorPanel';
import { makeSignoff, revokeSignoff } from '../../../services/signoffs';
import { getUsers, getScheduledChanges } from '../../../services/users';
import useAction from '../../../hooks/useAction';
import UserCard from '../../../components/UserCard';
import { withUser } from '../../../utils/AuthContext';
import { DIALOG_ACTION_INITIAL_STATE } from '../../../utils/constants';
import Link from '../../../utils/Link';

const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  userCard: {
    marginBottom: theme.spacing(2),
  },
}));

function ListUsers({ user }) {
  const username = user.email;
  const classes = useStyles();
  const [users, setUsers] = useState({});
  const [usersAction, fetchUsers] = useAction(getUsers);
  const [userScheduledChangesAction, fetchUserScheduledChanges] = useAction(
    getScheduledChanges
  );
  const [roles, setRoles] = useState([]);
  const [signoffRole, setSignoffRole] = useState('');
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [signoffAction, signoff] = useAction(props =>
    makeSignoff({ type: 'permissions', ...props })
  );
  const [revokeAction, revoke] = useAction(props =>
    revokeSignoff({ type: 'permissions', ...props })
  );
  const isLoading = usersAction.loading || userScheduledChangesAction.loading;
  const error =
    usersAction.error ||
    userScheduledChangesAction.error ||
    revokeAction.error ||
    (roles.length === 1 && signoffAction.error);
  const handleSignoffRoleChange = ({ target: { value } }) =>
    setSignoffRole(value);
  const dialogBody = (
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

  useEffect(() => {
    fetchUsers().then(({ data, error }) => {
      const userData = data.data;

      fetchUserScheduledChanges().then(resp => {
        if (!resp.error) {
          // create data of all user permissions and scheduled changes
          resp.data.data.scheduled_changes.forEach(sc => {
            if (!(sc.username in userData)) {
              userData[sc.username] = {
                roles: {},
                permissions: {},
                scheduledPermissions: {},
              };
            }

            if (!('scheduledPermissions' in userData[sc.username])) {
              userData[sc.username].scheduledPermissions = {};
            }

            userData[sc.username].scheduledPermissions[sc.permission] = sc;
          });
          setUsers(userData);

          // set-up information about the currently logged in user
          if (!error) {
            const roleList = userData[username].roles.map(
              roleData => roleData.role
            );

            setRoles(roleList);

            if (roleList.length > 0) {
              setSignoffRole(roleList[0]);
            }
          }
        }
      });
    });
  }, []);

  const updateSignoffs = ({ signoffRole, updatedUser, permission }) => {
    const result = clone(users);

    result[updatedUser].scheduledPermissions[permission].signoffs[
      username
    ] = signoffRole;

    setUsers(result);
  };

  const doSignoff = async (signoffRole, entry) => {
    const { error } = await signoff({ scId: entry.sc_id, role: signoffRole });

    return {
      error,
      result: {
        signoffRole,
        updatedUser: entry.username,
        permission: entry.permission,
      },
    };
  };

  const handleSignoff = async (...props) => {
    if (roles.length === 1) {
      const { error, result } = await doSignoff(signoffRole, ...props);

      if (!error) {
        updateSignoffs(result);
      }
    } else {
      setDialogState({
        ...dialogState,
        open: true,
        title: 'Signoff as…',
        confirmText: 'Sign off',
        item: props,
      });
    }
  };

  const handleRevoke = async entry => {
    const updatedUser = entry.username;
    const { permission } = entry;
    const { error } = await revoke({ scId: entry.sc_id });

    if (!error) {
      const result = clone(users);

      delete result[updatedUser].scheduledPermissions[permission].signoffs[
        username
      ];

      setUsers(result);
    }
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

  const handleDialogSubmit = async () => {
    const { error, result } = await doSignoff(signoffRole, ...dialogState.item);

    if (error) {
      throw error;
    }

    return result;
  };

  const handleDialogActionComplete = result => {
    updateSignoffs(result);
    handleDialogClose();
  };

  return (
    <Dashboard title="Users">
      {isLoading && <Spinner loading />}
      {error && <ErrorPanel fixed error={error} />}
      {!isLoading && users && (
        <Fragment>
          {Object.keys(users)
            .sort()
            .map(user => (
              <UserCard
                className={classes.userCard}
                key={user}
                username={user}
                roles={users[user].roles}
                permissions={users[user].permissions}
                scheduledPermissions={users[user].scheduledPermissions}
                onSignoff={handleSignoff}
                onRevoke={handleRevoke}
              />
            ))}
          <Link to="/users/create">
            <Tooltip title="Add User">
              <Fab
                color="primary"
                className={classes.fab}
                classes={{ root: classes.fab }}>
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
        onComplete={handleDialogActionComplete}
        onClose={handleDialogClose}
        onExited={handleDialogExited}
      />
    </Dashboard>
  );
}

export default withUser(ListUsers);
