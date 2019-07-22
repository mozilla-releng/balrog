import React, { useEffect, useState, Fragment } from 'react';
import { bool } from 'prop-types';
import { clone, defaultTo } from 'ramda';
import { makeStyles } from '@material-ui/styles';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import Fab from '@material-ui/core/Fab';
import SpeedDialAction from '@material-ui/lab/SpeedDialAction';
import Tooltip from '@material-ui/core/Tooltip';
import ContentSaveIcon from 'mdi-react/ContentSaveIcon';
import Button from '@material-ui/core/Button';
import DeleteIcon from 'mdi-react/DeleteIcon';
import PlusIcon from 'mdi-react/PlusIcon';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import AutoCompleteText from '../../../components/AutoCompleteText';
import getSuggestions from '../../../components/AutoCompleteText/getSuggestions';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import SpeedDial from '../../../components/SpeedDial';
import useAction from '../../../hooks/useAction';
import { getProducts } from '../../../services/rules';
import { getUserInfo } from '../../../services/users';
import { ALL_PERMISSIONS } from '../../../utils/constants';
import {
  supportsProductRestriction,
  supportsActionRestriction,
  getSupportedActions,
} from '../../../utils/userUtils';

const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
    right: theme.spacing(12),
  },
  fullWidth: {
    width: '100%',
  },
  addGrid: {
    marginTop: theme.spacing(0),
  },
  gridWithIcon: {
    marginTop: theme.spacing(3),
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
  const getEmptyPermission = () => ({
    name: '',
    options: {
      products: [],
      actions: [],
    },
    metadata: {
      isAdditional: true,
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
  const [username, setUsername] = useState('');
  const [roles, setRoles] = useState([]);
  // eslint-disable-next-line no-unused-vars
  const [originalRoles, setOriginalRoles] = useState([]);
  const [additionalRoles, setAdditionalRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  // eslint-disable-next-line no-unused-vars
  const [originalPermissions, setOriginalPermissions] = useState([]);
  const [additionalPermissions, setAdditionalPermissions] = useState(
    isNewUser ? [getEmptyPermission()] : []
  );
  const [products, setProducts] = useState([]);
  const [productsAction, fetchProducts] = useAction(getProducts);
  const [userAction, fetchUser] = useAction(getUserInfo);
  // eslint-disable-next-line no-unused-vars
  const [saveAction, saveUser] = useAction(() => {});
  const isLoading = userAction.loading || productsAction.loading;
  const error = userAction.error || productsAction.error || saveAction.error;
  const defaultToEmptyString = defaultTo('');

  useEffect(() => {
    if (!isNewUser) {
      Promise.all([fetchUser(existingUsername), fetchProducts()]).then(
        ([userdata, productdata]) => {
          const roles = Object.keys(userdata.data.data.roles).map(name => ({
            name,
            data_version: userdata.data.data.roles[name].data_version,
            metadata: {
              isAdditional: false,
            },
          }));
          const permissions = Object.keys(userdata.data.data.permissions).map(
            name => {
              const details = userdata.data.data.permissions[name];

              return {
                name,
                options: details.options || { products: [], actions: [] },
                data_version: details.data_version,
                metadata: {
                  isAdditional: false,
                  productText: '',
                  actionText: '',
                },
              };
            }
          );

          setUsername(userdata.data.data.username);
          setRoles(roles);
          setOriginalRoles(clone(roles));
          setPermissions(permissions);
          setOriginalPermissions(clone(permissions));
          setProducts(productdata.data.data.product);
        }
      );
    }
  }, []);

  const handleUsernameChange = ({ target: { value } }) => setUsername(value);
  const handleRoleNameChange = (role, index, value) => {
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
      })
    );
  };

  const handleRoleAdd = () => {
    setAdditionalRoles(additionalRoles.concat([getEmptyRole()]));
  };

  const handleRoleDelete = (role, index) => {
    const excludeRole = (entry, i) => !(i === index);

    if (role.metadata.isAdditional) {
      setAdditionalRoles(additionalRoles.filter(excludeRole));
    } else {
      setRoles(roles.filter(excludeRole));
    }
  };

  const handlePermissionAdd = () => {
    setAdditionalPermissions(
      additionalPermissions.concat([getEmptyPermission()])
    );
  };

  const handlePermissionNameChange = (permission, index) => value => {
    setAdditionalPermissions(
      additionalPermissions.map((entry, i) => {
        if (i !== index) {
          return entry;
        }

        const result = entry;

        result.name = value;

        return result;
      })
    );
  };

  const handlePermissionDelete = (permission, index) => {
    const excludePermission = (entry, i) => !(i === index);

    if (permission.metadata.isAdditional) {
      setAdditionalPermissions(additionalPermissions.filter(excludePermission));
    } else {
      setPermissions(permissions.filter(excludePermission));
    }
  };

  const handleRestrictionChange = (permission, restriction) => chips => {
    const updateRestrictions = entry => {
      if (entry.name !== permission.name) {
        return entry;
      }

      const result = entry;

      result.options[restriction] = chips;

      return result;
    };

    return permission.metadata.isAdditional
      ? setAdditionalPermissions(additionalPermissions.map(updateRestrictions))
      : setPermissions(permissions.map(updateRestrictions));
  };

  const handleRestrictionTextChange = (permission, key) => value => {
    const updateText = entry => {
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

  const handleUserSave = () => {};
  const handleUserDelete = () => {};
  const renderRole = (role, index) => (
    <Grid container spacing={2} key={index}>
      <Grid item xs={11}>
        <TextField
          disabled={role.metadata.isAdditional ? false : !isNewUser}
          onChange={e => handleRoleNameChange(role, index, e.target.value)}
          value={role.name}
          fullWidth
        />
      </Grid>
      <Grid item xs={1} className={classes.gridDelete}>
        <IconButton
          className={classes.iconButton}
          onClick={() => handleRoleDelete(role, index)}>
          <DeleteIcon />
        </IconButton>
      </Grid>
    </Grid>
  );
  const renderPermission = (permission, index) => (
    <Grid container spacing={2} key={index}>
      <Grid item xs={3}>
        <AutoCompleteText
          value={defaultToEmptyString(permission.name)}
          onValueChange={handlePermissionNameChange(permission, index)}
          getSuggestions={getSuggestions(ALL_PERMISSIONS)}
          label="Name"
          required
          disabled={!permission.metadata.isAdditional}
        />
      </Grid>
      <Grid item xs={4}>
        <AutoCompleteText
          multi
          disabled={!supportsProductRestriction(permission.name)}
          selectedItems={permission.options.products}
          onSelectedItemsChange={handleRestrictionChange(
            permission,
            'products'
          )}
          onValueChange={handleRestrictionTextChange(permission, 'productText')}
          value={permission.metadata.productText}
          getSuggestions={getSuggestions(products)}
          label="Product Restrictions"
        />
      </Grid>
      <Grid item xs={4}>
        <AutoCompleteText
          multi
          disabled={!supportsActionRestriction(permission.name)}
          selectedItems={permission.options.actions}
          onSelectedItemsChange={handleRestrictionChange(permission, 'actions')}
          onValueChange={handleRestrictionTextChange(permission, 'actionText')}
          value={permission.metadata.actionText}
          getSuggestions={getSuggestions(getSupportedActions(permission.name))}
          label="Action Restrictions"
        />
      </Grid>
      <Grid item xs={1} className={classes.gridDelete}>
        <IconButton
          className={classes.iconButton}
          onClick={() => handlePermissionDelete(permission, index)}>
          <DeleteIcon />
        </IconButton>
      </Grid>
    </Grid>
  );

  return (
    <Dashboard title="Users">
      {error && <ErrorPanel fixed error={error} />}
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
            <Typography variant="h5">Roles</Typography>
            {roles.map(renderRole)}
            {additionalRoles.map(renderRole)}
            <Grid item xs className={classes.addGrid}>
              <Grid item xs={11}>
                <Button
                  onClick={handleRoleAdd}
                  className={classes.fullWidth}
                  variant="outlined">
                  <PlusIcon />
                </Button>
              </Grid>
            </Grid>
            <br />
            <br />
            <br />
            <Typography variant="h5">Permissions</Typography>
            {permissions.map(renderPermission)}
            {additionalPermissions.map(renderPermission)}
            <Grid item xs className={classes.addGrid}>
              <Grid item xs={11}>
                <Button
                  onClick={handlePermissionAdd}
                  className={classes.fullWidth}
                  variant="outlined">
                  <PlusIcon />
                </Button>
              </Grid>
            </Grid>
          </form>
          <Tooltip title="Save User">
            <Fab
              disabled={saveAction.loading}
              onClick={handleUserSave}
              color="primary"
              className={classes.fab}>
              <ContentSaveIcon />
            </Fab>
          </Tooltip>
          {!isNewUser && (
            <SpeedDial ariaLabel="Secondary Actions">
              <SpeedDialAction
                disabled={saveAction.loading}
                icon={<DeleteIcon />}
                tooltipOpen
                tooltipTitle="Delete Signoff"
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
