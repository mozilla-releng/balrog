import { withAuth0 } from '@auth0/auth0-react';
import Fab from '@material-ui/core/Fab';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Tooltip from '@material-ui/core/Tooltip';
import SpeedDialAction from '@material-ui/lab/SpeedDialAction';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import classNames from 'classnames';
import ContentSaveIcon from 'mdi-react/ContentSaveIcon';
import DeleteIcon from 'mdi-react/DeleteIcon';
import React, { Fragment, useEffect, useState } from 'react';
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
  getReleasesV2,
  getReleaseV2,
  setRelease,
} from '../../../services/releases';
import { getProducts } from '../../../services/rules';
import { SNACKBAR_INITIAL_STATE } from '../../../utils/constants';

const useStyles = makeStyles((theme) => ({
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

function ReleaseV2(props) {
  const classes = useStyles();
  const {
    auth0,
    isNewRelease,
    match: {
      params: { releaseName },
    },
  } = props;
  const [releaseNameValue, setReleaseNameValue] = useState(releaseName || '');
  const [productTextValue, setProductTextValue] = useState('');
  const [releaseEditorValue, setReleaseEditorValue] = useState('{}');
  const [dataVersions, setDataVersions] = useState({});
  const [isReadOnly, setIsReadOnly] = useState(false);
  const [hasScheduledChange, setHasScheduledChange] = useState(false);
  const [snackbarState, setSnackbarState] = useState(SNACKBAR_INITIAL_STATE);
  const [release, fetchRelease] = useAction(getReleaseV2);
  const [setRelAction, setRel] = useAction(setRelease);
  const [fetchReleasesAction, fetchReleases] = useAction(getReleasesV2);
  const [products, fetchProducts] = useAction(getProducts);
  const isLoading =
    release.loading || fetchReleasesAction.loading || products.loading;
  const actionLoading = setRelAction.loading;
  const error =
    release.error ||
    fetchReleasesAction.error ||
    products.error ||
    setRelAction.error;

  useEffect(() => {
    if (releaseName) {
      Promise.all([fetchRelease(releaseName), fetchReleases()]).then(
        ([fetchedRelease, fetchedReleases]) => {
          const { data } = fetchedRelease.data;
          const metadata = fetchedReleases.data.data.releases.find(
            (r) => r.name === releaseName,
          );

          setProductTextValue(metadata.product);
          setIsReadOnly(metadata.read_only);
          setDataVersions(data.data_versions);
          setHasScheduledChange(Object.keys(data.sc_blob).length > 0);
          setReleaseEditorValue(
            JSON.stringify(
              Object.keys(data.sc_blob).length > 0 ? data.sc_blob : data.blob,
              null,
              2,
            ),
          );
        },
      );
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
    const { error } = await setRel({
      name: releaseNameValue,
      blob: JSON.parse(releaseEditorValue),
      product: productTextValue,
    });

    if (!error) {
      props.history.push(`/releases#${releaseNameValue}`);
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

    // If a Release already has a change scheduled, it needs to be cancelled
    // before we can schedule a new one. We can do this by setting it to the
    // current data.
    if (hasScheduledChange) {
      const { error } = await setRel({
        name: releaseName,
        product: productTextValue,
        blob: release.data.data.blob,
        old_data_versions: dataVersions,
      });

      if (error) {
        throw error;
      }
    }

    const { error } = await setRel({
      name: releaseNameValue,
      blob: JSON.parse(releaseEditorValue),
      oldDataVersions: dataVersions,
      when,
    });

    if (!error) {
      props.history.push(`/releases#${releaseNameValue}`);
    }
  };

  const handleScheduledChangeDelete = async () => {
    // Setting the Release the current data will cancel any
    // pending scheduled changes.
    const { error } = await setRel({
      name: releaseName,
      product: productTextValue,
      blob: release.data.data.blob,
      old_data_versions: dataVersions,
    });

    if (!error) {
      props.history.push(`/releases#${releaseNameValue}`);
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
        setProductTextValue(content.product || '');
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
      {isLoading && <Spinner loading />}
      {!isLoading && error && <ErrorPanel fixed error={error} />}
      {!isLoading && (
        <Fragment>
          <TextField
            disabled={!isNewRelease}
            fullWidth
            label="Release"
            onChange={handleReleaseNameChange}
            value={releaseNameValue}
          />
          <br />
          <br />
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
          <br />
          <br />
          <div className={classes.uploadReleaseDiv}>
            <label htmlFor="upload-release-file">
              <input
                disabled={isReadOnly}
                accept=".json"
                className={classes.inputOfTypeFile}
                id="upload-release-file"
                type="file"
                onChange={handleUploadRelease}
              />
              <Button
                disabled={isReadOnly}
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
          <br />
          <br />
          <Fragment>
            <Tooltip title={isNewRelease ? 'Create Release' : 'Update Release'}>
              {/* Add <div /> to avoid material-ui error "you are providing
              a disabled `button` child to the Tooltip component." */}
              <div
                className={classNames(
                  classes.fabWithTooltip,
                  classes.saveButton,
                  {
                    [classes.secondFab]: hasScheduledChange && !isReadOnly,
                    [classes.fab]: !hasScheduledChange || isReadOnly,
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
                  <ContentSaveIcon />
                </Fab>
              </div>
            </Tooltip>
            {hasScheduledChange && !isReadOnly && (
              <SpeedDial
                FabProps={{
                  disabled:
                    !auth0.user ||
                    actionLoading ||
                    isReadOnly ||
                    !hasScheduledChange,
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
        </Fragment>
      )}
    </Dashboard>
  );
}

export default withAuth0(ReleaseV2);
