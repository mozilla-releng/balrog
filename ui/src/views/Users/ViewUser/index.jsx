import Fab from '@material-ui/core/Fab';
import Grid from '@material-ui/core/Grid';
import IconButton from '@material-ui/core/IconButton';
import TextField from '@material-ui/core/TextField';
import Tooltip from '@material-ui/core/Tooltip';
import Typography from '@material-ui/core/Typography';
import SpeedDialAction from '@material-ui/lab/SpeedDialAction';
import { makeStyles } from '@material-ui/styles';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import ContentSaveIcon from 'mdi-react/ContentSaveIcon';
import DeleteIcon from 'mdi-react/DeleteIcon';
import PlusIcon from 'mdi-react/PlusIcon';
import { bool } from 'prop-types';
import { clone, defaultTo, propOr } from 'ramda';
import React, { Fragment, useEffect, useState } from 'react';
import AutoCompleteText from '../../../components/AutoCompleteText';
import getSuggestions from '../../../components/AutoCompleteText/getSuggestions';
import Button from '../../../components/Button';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import SpeedDial from '../../../components/SpeedDial';
import useAction from '../../../hooks/useAction';
import { getRequiredSignoffs } from '../../../services/requiredSignoffs';
import { getProducts } from '../../../services/rules';
import {
  getScheduledChanges,
  getUserInfo,
  userExists,
} from '../../../services/users';
import { ALL_PERMISSIONS, OBJECT_NAMES } from '../../../utils/constants';
import {
  getSupportedActions,
  supportsActionRestriction,
  supportsProductRestriction,
} from '../../../utils/userUtils';
import updateUser from '../utils/updateUser';

const useStyles = makeStyles((theme) => ({
  fab: {
    ...theme.mixins.fab,
    right: theme.spacing(12),
  },
  fullWidth: {
    width: '100%',
  },
  addGrid: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(10),
  },
  gridWithIcon: {
    marginTop: theme.spacing(3),
    display: 'flex',
    alignItems: 'end',
  },
  gridDelete: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  iconButton: {
    marginTop: theme.spacing(1),
  },
}));

function ViewUser({ isNewUser, ...props }) {
  const getEmptyPermission = (additional = false) => ({
    name: '',
    options: {
      products: [],
      actions: [],
    },
    sc: null,
    metadata: {
      isAdditional: additional,
      productText: '',
      actionText: '',
    },
  });
  const getEmptyRole = () => ({
    name: '',
    data_version: null,
    metadata: {
      isAdditional: true,
    },
  });
  const {
    match: {
      params: { username: existingUsername },
    },
  } = props;
  const classes = useStyles();
  const [username, setUsername] = useState(isNewUser ? '' : existingUsername);
  const [roles, setRoles] = useState([]);
  const [originalRoles, setOriginalRoles] = useState([]);
  const [additionalRoles, setAdditionalRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [originalPermissions, setOriginalPermissions] = useState([]);
  const [additionalPermissions, setAdditionalPermissions] = useState(
    isNewUser ? [getEmptyPermission(true)] : [],
  );
  const [products, setProducts] = useState([]);
  const setRequiredSignoffs = useState([])[1];
  const [userError, setUserError] = useState(null);
  const [rsAction, fetchRS] = useAction(getRequiredSignoffs);
  const [productsAction, fetchProducts] = useAction(getProducts);
  const [userAction, fetchUser] = useAction(getUserInfo);
  const [SCAction, fetchSC] = useAction(getScheduledChanges);
  const [saveAction, saveUser] = useAction(updateUser);
  const isLoading =
    userAction.loading ||
    productsAction.loading ||
    rsAction.loading ||
    SCAction.loading;
  const error =
    userError ||
    userAction.error ||
    productsAction.error ||
    saveAction.error ||
    rsAction.error ||
    SCAction.error;
  const defaultToEmptyString = defaultTo('');

  useEffect(() => {
    Promise.all([
      userExists(existingUsername).then((exists) =>
        exists ? fetchUser(existingUsername) : null,
      ),
      fetchProducts(),
      fetchRS(OBJECT_NAMES.PRODUCT_REQUIRED_SIGNOFF),
      fetchSC(),
    ]).then(([userdata, productdata, rs, scheduledChanges]) => {
      const roles =
        userdata === null
          ? []
          : Object.keys(userdata.data.data.roles).map((name) => ({
              name,
              data_version: userdata.data.data.roles[name].data_version,
              metadata: {
                isAdditional: false,
              },
            }));
      const permissions =
        userdata === null
          ? []
          : Object.keys(userdata.data.data.permissions).map((name) => {
              const details = userdata.data.data.permissions[name];
              const sc = scheduledChanges.data.data.scheduled_changes.filter(
                (sc) =>
                  sc.username === existingUsername && sc.permission === name,
              );
              const permission = {
                name,
                options: details.options || { products: [], actions: [] },
                data_version: details.data_version,
                sc: null,
                metadata: {
                  isAdditional: false,
                  productText: '',
                  actionText: '',
                },
              };

              // Copy any scheduled changes associated with an existing
              // permission into the list of permissions.
              if (sc.length > 0) {
                // The backend refers to permission names as the 'permission'
                // attribute of an object, but we prefer to call it 'name', so
                // we have to adjust that.
                sc[0].name = sc[0].permission;
                delete sc[0].permission;

                permission.sc = sc[0];

                if (!permission.sc.options) {
                  permission.sc.options = { products: [], actions: [] };
                }
              }

              return permission;
            });

      // Scheduled inserts don't have an existing permission to associate
      // with, so we need to create an empty one, and add to it.
      scheduledChanges.data.data.scheduled_changes.forEach((sc) => {
        if (sc.change_type === 'insert' && sc.username === existingUsername) {
          const p = getEmptyPermission();

          p.name = sc.permission;
          p.sc = clone(sc);
          p.sc.name = sc.permission;
          delete p.sc.permission;

          if (!p.sc.options) {
            p.sc.options = { products: [], actions: [] };
          }

          permissions.push(p);
        }
      });

      if (!isNewUser && permissions.length === 0) {
        setUserError('User does not exist!');

        return;
      }

      setRoles(roles);
      setOriginalRoles(clone(roles));
      setPermissions(permissions);
      setOriginalPermissions(clone(permissions));
      setProducts(productdata.data.data.product);
      setRequiredSignoffs(rs.data.data.required_signoffs);
    });
  }, []);

  const handleUsernameChange = ({ target: { value } }) => setUsername(value);
  const handleRoleNameChange = (_role, index, value) => {
    // Only additional roles' names can be changed, so we don't need to
    // handle existing roles here.
    setAdditionalRoles(
      additionalRoles.map((entry, i) => {
        if (i !== index) {
          return entry;
        }

        const result = entry;

        result.name = value;

        return result;
      }),
    );
  };

  const handleRoleAdd = () => {
    setAdditionalRoles(additionalRoles.concat([getEmptyRole()]));
  };

  const handleRoleDelete = (role, index) => {
    const excludeRole = (_entry, i) => !(i === index);

    if (role.metadata.isAdditional) {
      setAdditionalRoles(additionalRoles.filter(excludeRole));
    } else {
      setRoles(roles.filter(excludeRole));
    }
  };

  const handlePermissionAdd = () => {
    setAdditionalPermissions(
      additionalPermissions.concat([getEmptyPermission(true)]),
    );
  };

  const handlePermissionNameChange = (_permission, index) => (value) => {
    setAdditionalPermissions(
      additionalPermissions.map((entry, i) => {
        if (i !== index) {
          return entry;
        }

        const result = entry;

        result.name = value;

        return result;
      }),
    );
  };

  const handlePermissionDelete = (permission, index) => {
    const excludePermission = (_entry, i) => !(i === index);

    if (permission.metadata.isAdditional) {
      setAdditionalPermissions(additionalPermissions.filter(excludePermission));
    } else {
      setPermissions(permissions.filter(excludePermission));
    }
  };

  const handleRestrictionChange = (permission, restriction) => (chips) => {
    const updateRestrictions = (entry) => {
      if (entry.name !== permission.name) {
        return entry;
      }

      const result = entry;

      if (result.sc) {
        result.sc.options[restriction] = chips;
      } else {
        result.options[restriction] = chips;
      }

      return result;
    };

    return permission.metadata.isAdditional
      ? setAdditionalPermissions(additionalPermissions.map(updateRestrictions))
      : setPermissions(permissions.map(updateRestrictions));
  };

  const handleRestrictionTextChange = (permission, key) => (value) => {
    const updateText = (entry) => {
      if (entry.name !== permission.name) {
        return entry;
      }

      const result = entry;

      result.metadata[key] = value;

      return result;
    };

    return permission.metadata.isAdditional
      ? setAdditionalPermissions(additionalPermissions.map(updateText))
      : setPermissions(permissions.map(updateText));
  };

  const handleUserSave = async () => {
    const { error } = await saveUser({
      username,
      roles,
      originalRoles,
      additionalRoles,
      permissions,
      originalPermissions,
      additionalPermissions,
    });

    if (!error) {
      props.history.push('/users');
    }
  };

  const handleUserDelete = async () => {
    // We can use the existing saveUser function to delete a user
    // as long as we set current/additional roles and permissions
    // to empty arrays.
    const { error } = await saveUser({
      username,
      roles: [],
      originalRoles,
      additionalRoles: [],
      permissions: [],
      originalPermissions,
      additionalPermissions: [],
    });

    if (!error) {
      props.history.push('/users');
    }
  };

  const renderRole = (role, index) => (
    <Grid container spacing={2} key={index} className={classes.gridWithIcon}>
      <Grid item xs={11}>
        <TextField
          disabled={role.metadata.isAdditional ? false : !isNewUser}
          onChange={(e) => handleRoleNameChange(role, index, e.target.value)}
          value={role.name}
          fullWidth
        />
      </Grid>
      <Grid item xs={1} className={classes.gridDelete}>
        <IconButton onClick={() => handleRoleDelete(role, index)}>
          <DeleteIcon />
        </IconButton>
      </Grid>
    </Grid>
  );
  const renderPermission = (permission, index) => (
    <Grid container spacing={2} key={index} className={classes.gridWithIcon}>
      <Grid item xs={3}>
        <AutoCompleteText
          value={defaultToEmptyString(
            permission.sc ? permission.sc.name : permission.name,
          )}
          onValueChange={handlePermissionNameChange(
            permission.sc || permission,
            index,
          )}
          getSuggestions={getSuggestions(ALL_PERMISSIONS.sort())}
          label="Name"
          required
          disabled={!permission.metadata.isAdditional}
        />
      </Grid>
      <Grid item xs={4}>
        <AutoCompleteText
          multi
          disabled={
            (permission.sc && permission.sc.change_type === 'delete') ||
            !supportsProductRestriction(
              permission.sc ? permission.sc.name : permission.name,
            )
          }
          selectedItems={
            permission.sc
              ? propOr([], 'products')(permission.sc.options)
              : permission.options.products
          }
          onSelectedItemsChange={handleRestrictionChange(
            permission,
            'products',
          )}
          onValueChange={handleRestrictionTextChange(permission, 'productText')}
          value={permission.metadata.productText}
          getSuggestions={getSuggestions(products.sort())}
          label="Product Restrictions"
        />
      </Grid>
      <Grid item xs={4}>
        <AutoCompleteText
          multi
          disabled={
            (permission.sc && permission.sc.change_type === 'delete') ||
            !supportsActionRestriction(
              permission.sc ? permission.sc.name : permission.name,
            )
          }
          selectedItems={
            permission.sc
              ? propOr([], 'actions')(permission.sc.options)
              : permission.options.actions
          }
          onSelectedItemsChange={handleRestrictionChange(permission, 'actions')}
          onValueChange={handleRestrictionTextChange(permission, 'actionText')}
          value={permission.metadata.actionText}
          getSuggestions={getSuggestions(
            getSupportedActions(permission.name).sort(),
          )}
          label="Action Restrictions"
        />
      </Grid>
      {/* TODO: This delete button functions weirdly when a permission
          is scheduled to be deleted. If used, it will _cancel_ the
          deletion. Need to find a better way to handle this. */}
      <Grid item xs={1} className={classes.gridDelete}>
        <IconButton
          className={classes.iconButton}
          onClick={() => handlePermissionDelete(permission, index)}
        >
          <DeleteIcon />
        </IconButton>
      </Grid>
    </Grid>
  );

  return (
    <Dashboard title="Users">
      {error && <ErrorPanel error={error} />}
      {isLoading && <Spinner loading />}
      {!isLoading && (
        <Fragment>
          <form autoComplete="off">
            <Grid container spacing={2}>
              <Grid item xs>
                <TextField
                  required
                  disabled={!isNewUser}
                  onChange={handleUsernameChange}
                  fullWidth
                  label="Username"
                  value={username}
                  autoFocus
                />
              </Grid>
            </Grid>
            <br />
            <br />
            <br />
            {!isNewUser && !userError && (
              <Fragment>
                <Typography variant="h5">Roles</Typography>
                {roles.map(renderRole)}
                {additionalRoles.map(renderRole)}
                <Grid item xs className={classes.addGrid}>
                  <Grid item xs={11}>
                    <Button
                      color="primary"
                      onClick={handleRoleAdd}
                      className={classes.fullWidth}
                      variant="outlined"
                    >
                      <PlusIcon />
                    </Button>
                  </Grid>
                </Grid>
              </Fragment>
            )}
            {!userError && (
              <Fragment>
                <Typography variant="h5">Permissions</Typography>
                {permissions.map(renderPermission)}
                {additionalPermissions.map(renderPermission)}
                <Grid item xs className={classes.addGrid}>
                  <Grid item xs={11}>
                    <Button
                      color="primary"
                      onClick={handlePermissionAdd}
                      className={classes.fullWidth}
                      variant="outlined"
                    >
                      <PlusIcon />
                    </Button>
                  </Grid>
                </Grid>
              </Fragment>
            )}
          </form>
          <Tooltip title="Save User">
            <Fab
              disabled={saveAction.loading || userError}
              onClick={handleUserSave}
              color="primary"
              className={classes.fab}
            >
              <ContentSaveIcon />
            </Fab>
          </Tooltip>
          {!isNewUser && (
            <SpeedDial ariaLabel="Secondary Actions">
              <SpeedDialAction
                FabProps={{ disabled: saveAction.loading || userError }}
                icon={<DeleteIcon />}
                tooltipOpen
                tooltipTitle="Delete User"
                onClick={handleUserDelete}
              />
            </SpeedDial>
          )}
        </Fragment>
      )}
    </Dashboard>
  );
}

ViewUser.propTypes = {
  isNewUser: bool,
};

ViewUser.defaultProps = {
  isNewUser: false,
};

export default ViewUser;
