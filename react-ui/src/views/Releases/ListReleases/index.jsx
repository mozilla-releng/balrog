import React, { useMemo, useState, useEffect } from 'react';
import PlusIcon from 'mdi-react/PlusIcon';
import { makeStyles, useTheme } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import Dashboard from '../../../components/Dashboard';
import ErrorPanel from '../../../components/ErrorPanel';
import ReleaseCard from '../../../components/ReleaseCard';
import useAction from '../../../hooks/useAction';
import Link from '../../../utils/Link';
import { getReleases, deleteRelease } from '../../../services/releases';
import VariableSizeList from '../../../components/VariableSizeList';
import SearchBar from '../../../components/SearchBar';
import DialogAction from '../../../components/DialogAction';
import Snackbar from '../../../components/Snackbar';
import {
  DIALOG_ACTION_INITIAL_STATE,
  SNACKBAR_INITIAL_STATE,
} from '../../../utils/constants';
import elementsHeight from '../../../utils/elementsHeight';

const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  releaseCard: {
    margin: 2,
  },
}));

function ListReleases(props) {
  const classes = useStyles();
  const theme = useTheme();
  const {
    buttonHeight,
    body1TextHeight,
    body2TextHeight,
    h6TextHeight,
  } = elementsHeight(theme);
  const { hash } = props.location;
  const [releaseNameHash, setReleaseNameHash] = useState(null);
  const [scrollToRow, setScrollToRow] = useState(null);
  const [searchValue, setSearchValue] = useState('');
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [snackbarState, setSnackbarState] = useState(SNACKBAR_INITIAL_STATE);
  const [releases, setReleases] = useState([]);
  const [releasesAction, fetchReleases] = useAction(getReleases);
  const delRelease = useAction(deleteRelease)[1];
  const isLoading = releasesAction.loading;
  // eslint-disable-next-line prefer-destructuring
  const error = releasesAction.error;
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

  useEffect(() => {
    fetchReleases().then(r => {
      setReleases(r.data.data.releases);
    });
  }, []);

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
  }, [hash, filteredReleases]);

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

  // TODO Add mutation
  const handleReadOnlySubmit = () => {};
  const handleReadOnlyClose = state => {
    setDialogState({
      ...state,
      open: false,
    });
  };

  const handleReadOnlyError = (state, error) => {
    setDialogState({
      ...state,
      error,
    });
  };

  const handleDeleteSubmit = async state => {
    const release = state.item;
    const { error } = await delRelease({
      name: release.name,
      dataVersion: release.data_version,
    });

    if (error) {
      throw error;
    }

    return release.name;
  };

  // Setting state like this ends up with an error in the console:
  // Failed prop type: The prop `confirmText` is marked as required
  // in `DialogAction`, but its value is `undefined`
  const handleDeleteClose = state => {
    setDialogState({
      ...state,
      open: false,
    });
  };

  const handleDeleteComplete = (state, name) => {
    setReleases(releases.filter(r => r.name !== name));
    handleSnackbarOpen({
      message: `${name} deleted`,
    });

    handleDeleteClose(state);
  };

  const handleDeleteError = (state, error) => {
    setDialogState({
      ...state,
      error,
    });
  };

  const handleAccessChange = ({ release, checked }) => {
    setDialogState({
      open: true,
      title: checked ? 'Read Only?' : 'Read/Write?',
      confirmText: 'Yes',
      body: `This would make ${release.name} ${
        checked ? 'read only' : 'writable'
      }.`,
      destructive: false,
      item: release,
      handleSubmit: handleReadOnlySubmit,
      handleClose: handleReadOnlyClose,
      handleError: handleReadOnlyError,
      handleComplete: handleReadOnlyClose,
    });
  };

  const handleDelete = release => {
    setDialogState({
      open: true,
      title: 'Delete Release?',
      confirmText: 'Delete',
      body: `This will delete ${release.name}`,
      item: release,
      destructive: true,
      handleSubmit: handleDeleteSubmit,
      handleClose: handleDeleteClose,
      handleError: handleDeleteError,
      handleComplete: handleDeleteComplete,
    });
  };

  const Row = ({ index, style }) => {
    const release = filteredReleases[index];

    return (
      <div key={release.name} style={style}>
        <ReleaseCard
          className={classes.releaseCard}
          release={release}
          onAccessChange={handleAccessChange}
          onReleaseDelete={handleDelete}
        />
      </div>
    );
  };

  const getRowHeight = ({ index }) => {
    const listItemTextMargin = 6;
    const release = filteredReleases[index];
    // An approximation
    const ruleIdsLineCount = Math.ceil(release.rule_ids.length / 10) || 1;
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

    return height;
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
        title={dialogState.title}
        body={dialogState.body}
        open={dialogState.open}
        error={dialogState.error}
        confirmText={dialogState.confirmText}
        onSubmit={() => dialogState.handleSubmit(dialogState)}
        onClose={() => dialogState.handleClose(dialogState)}
        onError={error => dialogState.handleError(dialogState, error)}
        onComplete={name => dialogState.handleComplete(dialogState, name)}
      />
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

export default ListReleases;
