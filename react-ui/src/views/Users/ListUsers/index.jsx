import React, { Fragment, useState, useEffect } from 'react';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { makeStyles } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import PlusIcon from 'mdi-react/PlusIcon';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import { getUsers } from '../../../services/users';
import useAction from '../../../hooks/useAction';
import UserCard from '../../../components/UserCard';
import getUsersInfo from '../utils/getUsersInfo';

const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  userCard: {
    marginBottom: theme.spacing(2),
  },
}));

function ListUsers() {
  const classes = useStyles();
  const [users, setUsers] = useState({});
  const [usersAction, fetchUsers] = useAction(getUsers);
  const [userInfoAction, fetchUserInfo] = useAction(getUsersInfo);
  const isLoading = usersAction.loading || userInfoAction.loading;
  const error = usersAction.error || userInfoAction.error;

  useEffect(() => {
    fetchUsers().then(({ data, error }) => {
      if (!error) {
        fetchUserInfo(Object.keys(data.data)).then(({ data, error }) => {
          if (!error) {
            setUsers(data);
          }
        });
      }
    });
  }, []);

  const handleUserAdd = () => {};

  return (
    <Dashboard title="Users">
      {isLoading && <Spinner loading />}
      {error && <ErrorPanel fixed error={error} />}
      {!isLoading && users && (
        <Fragment>
          {Object.keys(users).map(user => (
            <UserCard
              className={classes.userCard}
              key={user}
              username={user}
              roles={users[user].roles}
              permissions={users[user].permissions}
            />
          ))}
          <Tooltip title="Add User">
            <Fab
              color="primary"
              className={classes.fab}
              classes={{ root: classes.fab }}
              onClick={handleUserAdd}>
              <PlusIcon />
            </Fab>
          </Tooltip>
        </Fragment>
      )}
    </Dashboard>
  );
}

export default ListUsers;
