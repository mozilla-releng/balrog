import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Fab from '@mui/material/Fab';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormLabel from '@mui/material/FormLabel';
import Grid from '@mui/material/GridLegacy';
import IconButton from '@mui/material/IconButton';
import RadioGroup from '@mui/material/RadioGroup';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';
import Typography from '@mui/material/Typography';
import classNames from 'classnames';
import ContentSaveIcon from 'mdi-react/ContentSaveIcon';
import DeleteIcon from 'mdi-react/DeleteIcon';
import PlusIcon from 'mdi-react/PlusIcon';
import { bool } from 'prop-types';
import React, { Fragment, useEffect, useState } from 'react';
import { NumericFormat } from 'react-number-format';
import { useNavigate, useParams } from 'react-router-dom';
import { makeStyles } from 'tss-react/mui';
import AutoCompleteText from '../../../components/AutoCompleteText';
import getSuggestions from '../../../components/AutoCompleteText/getSuggestions';
import Button from '../../../components/Button';
import Dashboard from '../../../components/Dashboard';
import DialogAction from '../../../components/DialogAction';
import ErrorPanel from '../../../components/ErrorPanel';
import Radio from '../../../components/Radio';
import SpeedDial from '../../../components/SpeedDial';
import useAction from '../../../hooks/useAction';
import { getChannels, getProducts } from '../../../services/rules';
import { DIALOG_ACTION_INITIAL_STATE } from '../../../utils/constants';
import getRequiredSignoffs from '../utils/getRequiredSignoffs';
import getRolesFromRequiredSignoffs from '../utils/getRolesFromRequiredSignoffs';
import updateRequiredSignoffs from '../utils/updateRequiredSignoffs';

let additionalRoleId = 0;
const useStyles = makeStyles()((theme) => ({
  iconButtonGrid: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
  },
  iconButton: {
    marginTop: theme.spacing(1),
  },
  fab: {
    ...theme.mixins.fab,
    right: theme.spacing(12),
  },
  gridWithIcon: {
    marginTop: theme.spacing(3),
  },
  addRoleButton: {
    width: '100%',
  },
  addRoleGrid: {
    marginTop: theme.spacing(5),
  },
  gridSection: {
    marginBottom: theme.spacing(10),
  },
  paper: {
    position: 'absolute',
    zIndex: 1,
    marginTop: theme.spacing(1),
    left: 0,
    right: 0,
  },
}));

function ViewSignoff({ isNewSignoff }) {
  const navigate = useNavigate();
  const getEmptyRole = (id = 0) => ({
    name: '',
    signoffs_required: null,
    data_version: null,
    sc: null,
    metadata: {
      isAdditionalRole: true,
      id,
    },
  });
  const params = useParams();
  const { product, channel } = params;
  const { classes } = useStyles();
  const [channelTextValue, setChannelTextValue] = useState(channel || '');
  const [productTextValue, setProductTextValue] = useState(product || '');
  const [type, setType] = useState(channel ? 'channel' : 'permission');
  const [roles, setRoles] = useState([]);
  const [originalRoles, setOriginalRoles] = useState([]);
  const [additionalRoles, setAdditionalRoles] = useState(
    isNewSignoff ? [getEmptyRole()] : [],
  );
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [requiredSignoffs, getRS] = useAction(getRequiredSignoffs);
  const [products, fetchProducts] = useAction(getProducts);
  const [channels, fetchChannels] = useAction(getChannels);
  const [saveAction, saveRS] = useAction(updateRequiredSignoffs);
  const isLoading =
    requiredSignoffs.loading || products.loading || channels.loading;
  const error =
    requiredSignoffs.error ||
    products.error ||
    // Don't show this in the main error bar if the confirmation dialog was
    // used. This has the side effect of the error moving from the dialog
    // to the main error bar if the dialog is closed, which is arguably
    // desirable?
    (!dialogState.open && saveAction.error);
  const dialogBody = channelTextValue
    ? `This will delete all Required Signoffs for the ${productTextValue} ${channelTextValue} channel`
    : `This will delete all Required Signoffs for ${productTextValue} permissions`;
  const handleTypeChange = ({ target: { value } }) => setType(value);
  const handleChannelChange = (value) => setChannelTextValue(value);
  const handleProductChange = (value) => setProductTextValue(value);
  const handleRoleValueChange =
    (role) =>
    ({ floatValue: value }) => {
      const setRole = (entry) => {
        if (entry.name !== role.name) {
          return entry;
        }

        const result = entry;

        if (result.sc) {
          result.sc.signoffs_required = value;
        } else {
          result.signoffs_required = value;
        }

        return result;
      };

      return role.metadata.isAdditionalRole
        ? setAdditionalRoles(additionalRoles.map(setRole))
        : setRoles(roles.map(setRole));
    };

  const handleRoleNameChange =
    (_role, index) =>
    ({ target: { value } }) => {
      const setRole = additionalRoles.map((entry, i) => {
        if (i !== index) {
          return entry;
        }

        const result = entry;

        result.name = value;

        return result;
      });

      setAdditionalRoles(setRole);
    };

  const handleRoleAdd = () => {
    additionalRoleId += 1;
    const role = getEmptyRole(additionalRoleId);

    setAdditionalRoles(additionalRoles.concat([role]));
  };

  const handleRoleDelete = (role, index) => () => {
    const excludeRole = (_entry, i) => !(i === index);

    return role.metadata.isAdditionalRole
      ? setAdditionalRoles(additionalRoles.filter(excludeRole))
      : setRoles(roles.filter(excludeRole));
  };

  const handleSignoffSave = async () => {
    const { error } = await saveRS({
      product: productTextValue,
      channel: channelTextValue,
      roles,
      originalRoles,
      additionalRoles,
      isNewSignoff,
    });

    if (!error) {
      navigate('/required-signoffs');
    }
  };

  const handleSignoffDelete = () =>
    setDialogState({
      ...dialogState,
      open: true,
      title: 'Delete Required Signoffs?',
      confirmText: 'Delete',
    });
  const handleDialogSubmit = async () => {
    const { error } = await saveRS({
      product: productTextValue,
      channel: channelTextValue,
      // pass nothing for current and additional roles
      // to make sure all existing roles are scheduled
      // for deletion.
      roles: [],
      originalRoles,
      additionalRoles: [],
      isNewSignoff,
    });

    if (error) {
      throw error;
    }
  };

  const handleDialogClose = () => setDialogState(DIALOG_ACTION_INITIAL_STATE);
  const handleDialogActionComplete = () => {
    navigate('/required-signoffs');
  };

  const handleDialogError = (error) =>
    setDialogState({ ...dialogState, error });

  useEffect(() => {
    if (isNewSignoff) {
      Promise.all([fetchProducts(), fetchChannels()]);
    } else {
      Promise.all([fetchProducts(), fetchChannels(), getRS()]).then(
        ([_prods, _chs, rs]) => {
          const roles = getRolesFromRequiredSignoffs(rs.data, product, channel);

          setRoles(roles);
          setOriginalRoles(JSON.parse(JSON.stringify(roles)));
        },
      );
    }
  }, [product, channel]);

  const renderRole = (role, index) => (
    <Grid
      key={role.metadata.id}
      className={classes.gridWithIcon}
      container
      spacing={2}
    >
      <Grid item xs>
        <TextField
          required
          disabled={role.metadata.isAdditionalRole ? false : !isNewSignoff}
          onChange={handleRoleNameChange(role, index)}
          fullWidth
          label="Role"
          value={role.name}
        />
      </Grid>
      <Grid item xs>
        <NumericFormat
          allowNegative={false}
          required
          label="Signoffs Required"
          fullWidth
          value={role.sc ? role.sc.signoffs_required : role.signoffs_required}
          customInput={TextField}
          onValueChange={handleRoleValueChange(role, index)}
          decimalScale={0}
        />
      </Grid>
      <Grid className={classes.iconButtonGrid} item xs={1}>
        <IconButton
          onClick={handleRoleDelete(role, index)}
          className={classes.iconButton}
          size="large"
        >
          <DeleteIcon />
        </IconButton>
      </Grid>
    </Grid>
  );

  return (
    <Dashboard title="Required Signoff">
      {error && <ErrorPanel error={error} />}
      {isLoading && (
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress />
        </Box>
      )}
      {!isLoading && (
        <Fragment>
          <form autoComplete="off">
            <Grid className={classes.gridSection} container spacing={2}>
              <Grid item xs={12}>
                <AutoCompleteText
                  onValueChange={handleProductChange}
                  value={productTextValue}
                  getSuggestions={
                    products.data &&
                    getSuggestions(products.data.data.product.sort())
                  }
                  label="Product"
                  required
                  inputProps={{
                    autoFocus: true,
                    fullWidth: true,
                    disabled: !isNewSignoff,
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl margin="normal" component="fieldset">
                  <FormLabel component="legend">Type</FormLabel>
                  <RadioGroup
                    aria-label="Type"
                    name="type"
                    value={type}
                    onChange={handleTypeChange}
                  >
                    <FormControlLabel
                      disabled={!isNewSignoff}
                      value="channel"
                      control={<Radio />}
                      label="Channel"
                    />
                    <FormControlLabel
                      disabled={!isNewSignoff}
                      value="permission"
                      control={<Radio />}
                      label="Permission"
                    />
                  </RadioGroup>
                </FormControl>
              </Grid>
              {type === 'channel' && (
                <Grid item xs={12}>
                  <AutoCompleteText
                    value={channelTextValue}
                    onValueChange={handleChannelChange}
                    getSuggestions={
                      channels.data &&
                      getSuggestions(channels.data.data.channel.sort())
                    }
                    label="Channel"
                    required
                    inputProps={{
                      fullWidth: true,
                      disabled: !isNewSignoff,
                    }}
                  />
                </Grid>
              )}
            </Grid>
            <Typography variant="h5">Roles</Typography>
            {roles.map(renderRole)}
            {additionalRoles.map(renderRole)}
            <Grid
              className={classNames(classes.addRoleGrid, classes.gridSection)}
              container
            >
              <Grid item xs={11}>
                <Button
                  onClick={handleRoleAdd}
                  className={classes.addRoleButton}
                  color="primary"
                  variant="outlined"
                >
                  <PlusIcon />
                </Button>
              </Grid>
            </Grid>
          </form>
          <Tooltip title="Save Signoff">
            <Fab
              disabled={saveAction.loading}
              onClick={handleSignoffSave}
              color="primary"
              className={classes.fab}
            >
              <ContentSaveIcon />
            </Fab>
          </Tooltip>
          {!isNewSignoff && (
            <SpeedDial ariaLabel="Secondary Actions">
              <SpeedDialAction
                FabProps={{ disabled: saveAction.loading }}
                icon={<DeleteIcon />}
                tooltipOpen
                tooltipTitle="Delete Required Signoffs"
                onClick={handleSignoffDelete}
              />
            </SpeedDial>
          )}
        </Fragment>
      )}
      <DialogAction
        open={dialogState.open}
        title={dialogState.title}
        body={dialogBody}
        confirmText={dialogState.confirmText}
        destructive
        onSubmit={handleDialogSubmit}
        onError={handleDialogError}
        error={dialogState.error}
        onComplete={handleDialogActionComplete}
        onClose={handleDialogClose}
      />
    </Dashboard>
  );
}

ViewSignoff.propTypes = {
  // Set to true if user is not updating an existing signoff.
  isNewSignoff: bool,
};

ViewSignoff.defaultProps = {
  isNewSignoff: false,
};

export default ViewSignoff;
