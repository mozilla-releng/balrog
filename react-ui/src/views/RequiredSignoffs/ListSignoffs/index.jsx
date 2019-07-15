import React, { Fragment, useEffect, useState } from 'react';
import { titleCase } from 'change-case';
import classNames from 'classnames';
import { view, lensPath } from 'ramda';
import Spinner from '@mozilla-frontend-infra/components/Spinner';
import { makeStyles } from '@material-ui/styles';
import Fab from '@material-ui/core/Fab';
import Tooltip from '@material-ui/core/Tooltip';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import PlusIcon from 'mdi-react/PlusIcon';
import Dashboard from '../../../components/Dashboard';
import SignoffCard from '../../../components/SignoffCard';
import ErrorPanel from '../../../components/ErrorPanel';
import SignoffCardEntry from '../../../components/SignoffCardEntry';
import Link from '../../../utils/Link';
import getRequiredSignoffs from '../utils/getRequiredSignoffs';
import useAction from '../../../hooks/useAction';

const getPermissionChangesLens = product => lensPath([product, 'permissions']);
const getRulesOrReleasesChangesLens = product =>
  lensPath([product, 'channels']);
const useStyles = makeStyles(theme => ({
  fab: {
    ...theme.mixins.fab,
  },
  toolbar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  dropdown: {
    minWidth: 200,
  },
  dropdownDiv: {
    marginBottom: theme.spacing(2),
    display: 'flex',
    flex: 1,
    justifyContent: 'flex-end',
  },
  card: {
    marginBottom: theme.spacing(2),
  },
  lastDivider: {
    display: 'none',
  },
}));

function ListSignoffs() {
  const classes = useStyles();
  const [requiredSignoffs, setRequiredSignoffs] = useState(null);
  const [product, setProduct] = useState('Firefox');
  const [{ error, loading }, getRS] = useAction(getRequiredSignoffs);
  const handleFilterChange = ({ target: { value } }) => setProduct(value);
  const permissionChanges = view(
    getPermissionChangesLens(product),
    requiredSignoffs
  );
  const rulesOrReleasesChanges = view(
    getRulesOrReleasesChangesLens(product),
    requiredSignoffs
  );

  // Fetch view data
  useEffect(() => {
    getRS().then(({ data }) => setRequiredSignoffs(data));
  }, []);

  return (
    <Dashboard title="Required Signoffs">
      {error && <ErrorPanel fixed error={error} />}
      {loading && <Spinner loading />}
      {requiredSignoffs && (
        <Fragment>
          <div className={classes.toolbar}>
            {permissionChanges && (
              <Typography gutterBottom variant="h5">
                Changes to Permissions
              </Typography>
            )}
            {!permissionChanges && rulesOrReleasesChanges && (
              <Typography gutterBottom variant="h5">
                Changes to Rules / Releases
              </Typography>
            )}
            <div className={classes.dropdownDiv}>
              <TextField
                className={classes.dropdown}
                select
                label="Product"
                value={product}
                onChange={handleFilterChange}>
                {Object.keys(requiredSignoffs).map(product => (
                  <MenuItem key={product} value={product}>
                    {product}
                  </MenuItem>
                ))}
              </TextField>
            </div>
          </div>
          {permissionChanges && (
            <SignoffCard
              className={classes.card}
              title={titleCase(product)}
              to={`/required-signoffs/${product}`}>
              {Object.entries(permissionChanges).map(
                ([name, role], index, arr) => {
                  const key = `${name}-${index}`;

                  return (
                    <Fragment key={key}>
                      <SignoffCardEntry key={name} name={name} entry={role} />
                      <Divider
                        className={classNames({
                          [classes.lastDivider]: arr.length - 1 === index,
                        })}
                      />
                    </Fragment>
                  );
                }
              )}
            </SignoffCard>
          )}
          <div>
            {rulesOrReleasesChanges && (
              <Fragment>
                {permissionChanges && (
                  <Fragment>
                    <br />
                    <Typography gutterBottom variant="h5">
                      Changes to Rules / Releases
                    </Typography>
                    <br />
                  </Fragment>
                )}
                {Object.entries(rulesOrReleasesChanges).map(
                  ([channelName, roles]) => (
                    <SignoffCard
                      key={`${product}-${channelName}`}
                      className={classes.card}
                      title={titleCase(`${product} ${channelName} Channel`)}
                      to={`/required-signoffs/${product}/${channelName}`}>
                      {Object.entries(roles).map(
                        ([roleName, role], index, arr) => {
                          const key = `${roleName}-${index}`;

                          return (
                            <Fragment key={key}>
                              <SignoffCardEntry
                                key={roleName}
                                name={roleName}
                                entry={role}
                              />
                              <Divider
                                className={classNames({
                                  [classes.lastDivider]:
                                    arr.length - 1 === index,
                                })}
                              />
                            </Fragment>
                          );
                        }
                      )}
                    </SignoffCard>
                  )
                )}
              </Fragment>
            )}
            {!permissionChanges && !rulesOrReleasesChanges && (
              <Typography>No required signoffs for {product}</Typography>
            )}
          </div>
          <Link to="/required-signoffs/create">
            <Tooltip title="Enable Signoff for a New Product">
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
    </Dashboard>
  );
}

export default ListSignoffs;
