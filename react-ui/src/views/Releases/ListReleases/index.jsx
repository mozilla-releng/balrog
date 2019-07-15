import React, { useMemo, useState, useEffect } from 'react';
import PlusIcon from 'mdi-react/PlusIcon';
import { makeStyles, useTheme } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import Dashboard from '../../../components/Dashboard';
import ReleaseCard from '../../../components/ReleaseCard';
import useAction from '../../../hooks/useAction';
import Link from '../../../utils/Link';
import { getReleases } from '../../../services/releases';
import VariableSizeList from '../../../components/VariableSizeList';
import SearchBar from '../../../components/SearchBar';
import DialogAction from '../../../components/DialogAction';
import { DIALOG_ACTION_INITIAL_STATE } from '../../../utils/constants';

const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  releaseCard: {
    margin: 2,
  },
}));

function ListPermissions(props) {
  const classes = useStyles();
  const theme = useTheme();
  const { hash } = props.location;
  const [releaseNameHash, setReleaseNameHash] = useState(null);
  const [scrollToRow, setScrollToRow] = useState(null);
  const [searchValue, setSearchValue] = useState('');
  const [dialogState, setDialogState] = useState(DIALOG_ACTION_INITIAL_STATE);
  const [releases, fetchReleases] = useAction(getReleases);
  const isLoading = releases.loading;
  const filteredReleases = useMemo(() => {
    if (!releases.data) {
      return [];
    }

    if (!searchValue) {
      return releases.data.data.releases;
    }

    return releases.data.data.releases.filter(release =>
      release.name.toLowerCase().includes(searchValue.toLowerCase())
    );
  }, [releases.data, searchValue]);
  const filteredReleasesCount = filteredReleases.length;

  useEffect(() => {
    fetchReleases();
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

  const handleAccessChange = ({ release, checked }) => {
    setDialogState({
      open: true,
      title: checked ? 'Read Only?' : 'Read/Write?',
      confirmText: 'Yes',
      body: `This would make ${release.name} ${
        checked ? 'read only' : 'writable'
      }.`,
      item: release,
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
        />
      </div>
    );
  };

  const getRowHeight = ({ index }) => {
    const release = filteredReleases[index];
    // An approximation
    const ruleIdsLineCount = Math.ceil(release.rule_ids.length / 10) || 1;
    // card header
    let height = theme.spacing(9);

    // first row
    height += theme.spacing(7);
    // rule ids row
    height += theme.spacing(3) + ruleIdsLineCount * theme.spacing(3);
    // actions row
    height += 7 * theme.spacing(1);
    // space below the card (margin)
    height += theme.spacing(6);

    return height;
  };

  const handleSearchChange = ({ target: { value } }) => {
    setSearchValue(value);
  };

  // TODO Add mutation
  const handleDialogSubmit = () => {};
  const handleDialogClose = () => {
    setDialogState({
      ...dialogState,
      open: false,
    });
  };

  const handleDialogError = error => {
    setDialogState({
      ...dialogState,
      error,
    });
  };

  return (
    <Dashboard title="Releases">
      <SearchBar
        placeholder="Search a release..."
        onChange={handleSearchChange}
        value={searchValue}
      />
      {isLoading && <Spinner loading />}
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
        onSubmit={handleDialogSubmit}
        onClose={handleDialogClose}
        onError={handleDialogError}
        onComplete={handleDialogClose}
      />
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

export default ListPermissions;
