import { withAuth0 } from '@auth0/auth0-react';
import DeleteIcon from '@mui/icons-material/Delete';
import SaveIcon from '@mui/icons-material/Save';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';
import Fab from '@mui/material/Fab';
import SpeedDialAction from '@mui/material/SpeedDialAction';
import TextField from '@mui/material/TextField';
import Tooltip from '@mui/material/Tooltip';
import classNames from 'classnames';
import React, { Fragment, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { makeStyles } from 'tss-react/mui';
import AutoCompleteText from '../../../components/AutoCompleteText';
import getSuggestions from '../../../components/AutoCompleteText/getSuggestions';
import Button from '../../../components/Button';
import CodeEditor from '../../../components/CodeEditor';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import Snackbar from '../../../components/Snackbar';
import SpeedDial from '../../../components/SpeedDial';
import useAction from '../../../hooks/useAction';
import {
  addScheduledChange,
  createRelease,
  deleteScheduledChange,
  getRelease,
  getReleases,
  getScheduledChangeByName,
  updateScheduledChange,
} from '../../../services/releases';
import { getProducts } from '../../../services/rules';
import { SNACKBAR_INITIAL_STATE } from '../../../utils/constants';

const useStyles = makeStyles()((theme) => ({
  fab: {
    ...theme.mixins.fab,
  },
  secondFab: {
    ...theme.mixins.fab,
    right: theme.spacing(12),
  },
  // Ensure fab  has higher priority than the code editor.
  // Otherwise, the fab is not clickable.
  saveButton: {
    zIndex: 10,
  },
  inputOfTypeFile: {
    display: 'none',
  },
  uploadReleaseDiv: {
    marginBottom: '-2em',
    display: 'flex',
    justifyContent: 'flex-end',
  },
  uploadReleaseButton: {
    borderRadius: 0,
  },
  fabWithTooltip: {
    height: theme.spacing(7),
    width: theme.spacing(7),
  },
}));

function Release(props) {
  const { classes } = useStyles();
  const params = useParams();
  const { releaseName } = params;
  const navigate = useNavigate();
  const { auth0, isNewRelease } = props;
  const [releaseNameValue, setReleaseNameValue] = useState(releaseName || '');
  const [productTextValue, setProductTextValue] = useState('');
  const [releaseEditorValue, setReleaseEditorValue] = useState('{}');
  const [scId, setScId] = useState(null);
  const [dataVersion, setDataVersion] = useState(null);
  const [scDataVersion, setScDataVersion] = useState(null);
  const [isReadOnly, setIsReadOnly] = useState(false);
  const [snackbarState, setSnackbarState] = useState(SNACKBAR_INITIAL_STATE);
  const [release, fetchRelease] = useAction(getRelease);
  const [createRelAction, createRel] = useAction(createRelease);
  const [addSCAction, addSC] = useAction(addScheduledChange);
  const [updateSCAction, updateSC] = useAction(updateScheduledChange);
  const [deleteSCAction, deleteSC] = useAction(deleteScheduledChange);
  const [scheduledChangeNameAction, fetchScheduledChangeByName] = useAction(
    getScheduledChangeByName,
  );
  const fetchReleases = useAction(getReleases)[1];
  const [products, fetchProducts] = useAction(getProducts);
  const isLoading =
    release.loading || products.loading || scheduledChangeNameAction.loading;
  const actionLoading =
    createRelAction.loading ||
    addSCAction.loading ||
    updateSCAction.loading ||
    deleteSCAction.loading;
  const error =
    release.error ||
    products.error ||
    createRelAction.error ||
    addSCAction.error ||
    updateSCAction.error ||
    deleteSCAction.error ||
    scheduledChangeNameAction.error;

  useEffect(() => {
    if (releaseName) {
      Promise.all([
        fetchRelease(releaseName),
        fetchScheduledChangeByName(releaseName),
        fetchReleases(),
      ]).then(([fetchedRelease, fetchedSC, fetchedReleases]) => {
        if (fetchedSC.data.data.count > 0) {
          const sc = fetchedSC.data.data.scheduled_changes[0];

          setReleaseEditorValue(JSON.stringify(sc.data, null, 2));
          setProductTextValue(sc.product);
          setDataVersion(sc.data_version);
          setScId(sc.sc_id);
          setScDataVersion(sc.sc_data_version);
        } else {
          setReleaseEditorValue(
            JSON.stringify(fetchedRelease.data.data, null, 2),
          );

          if (fetchedReleases.data) {
            const r = fetchedReleases.data.data.releases.find(
              (r) => r.name === releaseName,
            );

            setProductTextValue(r.product);
            setDataVersion(r.data_version);
            setIsReadOnly(r.read_only);
          }
        }
      });
    }

    fetchProducts();
  }, [releaseName]);

  const handleProductChange = (value) => {
    setProductTextValue(value);
  };

  const handleReleaseNameChange = ({ target: { value } }) => {
    setReleaseNameValue(value);
  };

  const handleReleaseEditorChange = (value) => {
    setReleaseEditorValue(value);
  };

  const handleReleaseCreate = async () => {
    // Newly created Releases never need signoff, so we can always
    // safely create them directly instead of using Scheduled Changes.
    const { error } = await createRel(
      releaseNameValue,
      productTextValue,
      releaseEditorValue,
    );

    if (!error) {
      navigate(`/releases#${releaseNameValue}`);
    }
  };

  const handleReleaseUpdate = async () => {
    // Updates to Releases require signoff in some circumstances,
    // but we don't have a need to schedule them for specific times.
    // Because of this, we always schedule them for slightly in the future,
    // which means that changes that don't require signoff will happen
    // almost immediately, and changes that do require signoff will wait
    // until those are completed.
    const when = Date.now() + 30000;
    let error = null;

    if (scId) {
      ({ error } = await updateSC({
        scId,
        when,
        sc_data_version: scDataVersion,
        data_version: dataVersion,
        data: releaseEditorValue,
      }));
    } else {
      ({ error } = await addSC({
        change_type: 'update',
        when,
        name: releaseNameValue,
        product: productTextValue,
        data: releaseEditorValue,
        data_version: dataVersion,
      }));
    }

    if (!error) {
      navigate(`/releases#${releaseNameValue}`);
    }
  };

  const handleScheduledChangeDelete = async () => {
    const { error } = await deleteSC({
      scId,
      scDataVersion,
    });

    if (!error) {
      navigate(`/releases#${releaseNameValue}`);
    }
  };

  const handleSnackbarClose = (_event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarState({
      ...SNACKBAR_INITIAL_STATE,
      // Keep same variant otherwise there will be a split second where
      // the color of the snackbar may change if the variant is not 'success'.
      // This is due to the fact that closing the snackbar is not instant but
      // rather an animation.
      variant: snackbarState.variant,
    });
  };

  const handleSnackbarOpen = ({ message, variant = 'success' }) => {
    setSnackbarState({ message, variant, open: true });
  };

  const handleUploadRelease = (ev) => {
    const file = ev.target.files[0];
    const reader = new FileReader();

    reader.addEventListener('load', (e) => {
      try {
        const content = JSON.parse(e.target.result);

        setReleaseEditorValue(JSON.stringify(content, null, 2));
        setProductTextValue(content.product);
        setReleaseNameValue(content.name);
      } catch (e) {
        handleSnackbarOpen({
          message: e.message,
          variant: 'error',
        });
      }
    });

    reader.addEventListener('error', (e) => {
      handleSnackbarOpen({
        message: e.message,
        variant: 'error',
      });
      reader.abort();
    });

    reader.readAsText(file);
  };

  return (
    <Dashboard
      title={isNewRelease ? 'Create Release' : `Update Release ${releaseName}`}
    >
      {isLoading && (
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress />
        </Box>
      )}
      {!isLoading && error && <ErrorPanel error={error} />}
      {!isLoading && (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            height: '100%',
            gap: '2em',
          }}
        >
          <TextField
            disabled={!isNewRelease}
            fullWidth
            label="Release"
            onChange={handleReleaseNameChange}
            value={releaseNameValue}
          />
          <AutoCompleteText
            onValueChange={handleProductChange}
            value={productTextValue}
            getSuggestions={
              products.data && getSuggestions(products.data.data.product.sort())
            }
            label="Product"
            required
            disabled={!isNewRelease}
            inputProps={{
              autoFocus: true,
              fullWidth: true,
            }}
          />
          <div className={classes.uploadReleaseDiv}>
            <label htmlFor="upload-release-file">
              <input
                disabled={!auth0.user || isReadOnly}
                accept=".json"
                className={classes.inputOfTypeFile}
                id="upload-release-file"
                type="file"
                onChange={handleUploadRelease}
              />
              <Button
                disabled={!auth0.user || isReadOnly}
                size="small"
                variant="outlined"
                component="span"
                className={classes.uploadReleaseButton}
              >
                Upload Release
              </Button>
            </label>
          </div>
          <CodeEditor
            onChange={handleReleaseEditorChange}
            value={releaseEditorValue}
            readOnly={isReadOnly}
          />
          <Fragment>
            <Tooltip title={isNewRelease ? 'Create Release' : 'Update Release'}>
              {/* Add <div /> to avoid material-ui error "you are providing
              a disabled `button` child to the Tooltip component." */}
              <div
                className={classNames(
                  classes.fabWithTooltip,
                  classes.saveButton,
                  {
                    [classes.secondFab]: scId && !isReadOnly,
                    [classes.fab]: !scId || isReadOnly,
                  },
                )}
              >
                <Fab
                  disabled={!auth0.user || actionLoading || isReadOnly}
                  onClick={
                    isNewRelease ? handleReleaseCreate : handleReleaseUpdate
                  }
                  color="primary"
                >
                  <SaveIcon />
                </Fab>
              </div>
            </Tooltip>
            {scId && !isReadOnly && (
              <SpeedDial
                FabProps={{
                  disabled: !auth0.user || actionLoading || isReadOnly || !scId,
                }}
                ariaLabel="Secondary Actions"
              >
                <SpeedDialAction
                  icon={<DeleteIcon />}
                  tooltipOpen
                  tooltipTitle="Cancel Pending Change"
                  onClick={handleScheduledChangeDelete}
                />
              </SpeedDial>
            )}
          </Fragment>
          <Snackbar onClose={handleSnackbarClose} {...snackbarState} />
        </Box>
      )}
    </Dashboard>
  );
}

export default withAuth0(Release);
