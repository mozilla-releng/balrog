import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import MenuItem from '@mui/material/MenuItem';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { parse, stringify } from 'qs';
import React, { Fragment, useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router';
import { makeStyles } from 'tss-react/mui';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import useAction from '../../../hooks/useAction';
import { getUsers } from '../../../services/users';

const ALL = 'all';
const useStyles = makeStyles()((theme) => ({
  title: {
    marginBottom: theme.spacing(3),
  },
  paper: {
    backgroundColor: theme.palette.background.paper,
  },
  roleWrapper: {
    marginBottom: theme.spacing(4),
  },
  options: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  dropdown: {
    minWidth: 200,
    marginBottom: theme.spacing(2),
  },
}));

function ListRoles() {
  const { classes } = useStyles();
  const { search } = useLocation();
  const navigate = useNavigate();
  const query = parse(search.slice(1));
  const [usersAction, fetchUsers] = useAction(getUsers);
  const [roleFilter, setRoleFilter] = useState(ALL);
  const isLoading = usersAction.loading;
  const { error } = usersAction;
  const roles = useMemo(() => {
    if (!usersAction.data) {
      return [];
    }

    return Array.from(
      new Set(
        Object.values(usersAction.data.data).flatMap(({ roles }) =>
          roles.map(({ role }) => role),
        ),
      ),
    );
  }, [usersAction.data]);
  const users = useMemo(() => {
    if (!usersAction.data) {
      return [];
    }

    return Object.entries(usersAction.data.data).map(
      ([username, { roles }]) => ({
        username,
        roles,
      }),
    );
  }, [usersAction.data]);
  const filteredRoles = useMemo(
    () => (roleFilter === ALL ? roles : [roleFilter]),
    [roles, roleFilter],
  );

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleFilterChange = ({ target: { value } }) => {
    setRoleFilter(value);

    const qs = {
      ...query,
      role: value !== 'all' ? value : undefined,
    };

    navigate(`/roles${stringify(qs, { addQueryPrefix: true })}`);
  };

  return (
    <Dashboard title="Roles">
      {isLoading && (
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress />
        </Box>
      )}
      {error && <ErrorPanel error={error} />}
      {Boolean(filteredRoles.length) && Boolean(users.length) && (
        <Fragment>
          <div className={classes.options}>
            <TextField
              className={classes.dropdown}
              select
              label="Role"
              value={roleFilter}
              onChange={handleFilterChange}
            >
              <MenuItem value="all">All Roles</MenuItem>
              {roles.map((role) => (
                <MenuItem key={role} value={role}>
                  {role}
                </MenuItem>
              ))}
            </TextField>
          </div>
          {filteredRoles.map((role) => (
            <div key={role} className={classes.roleWrapper}>
              <Typography variant="h6" className={classes.title}>
                {role}
              </Typography>
              <div className={classes.paper}>
                <List>
                  {users
                    .filter((user) =>
                      user.roles.map(({ role }) => role).includes(role),
                    )
                    .map((user) => (
                      <ListItem key={user.username}>
                        <ListItemText primary={user.username} />
                      </ListItem>
                    ))}
                </List>
              </div>
            </div>
          ))}
        </Fragment>
      )}
    </Dashboard>
  );
}

export default ListRoles;
