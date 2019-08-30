import React, { memo, useState, useEffect } from 'react';
import { clone } from 'ramda';
import deepSortObject from 'deep-sort-object';
import { string, object } from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import { List } from 'react-virtualized';
import Paper from '@material-ui/core/Paper';
import {
  NEW_LINES_REGEX,
  DIFF_COLORS,
  INITIAL_JS_DIFF_SUMMARY,
  CONTENT_MAX_WIDTH,
} from '../../utils/constants';
import DiffWorker from './diff.worker';

const useStyles = makeStyles(theme => ({
  pre: {
    margin: 0,
    fontSize: 13,
    lineHeight: 1.5,
    display: 'inline-block',
  },
  header: {
    height: theme.spacing(4),
    background: 'rgb(250, 251, 252)',
    borderBottom: '1px solid #e1e4e8',
    display: 'flex',
    justifyContent: 'flex-end',
    alignItems: 'center',
    padding: `0 ${theme.spacing(2)}px`,
  },
  greenText: {
    color: '#28a745',
  },
  redText: {
    color: '#cb2431',
  },
  listWrapper: {
    overflowX: 'auto',
    padding: theme.spacing(1),
  },
}));

/**
 * A component to display a diff in a similar fashion as `git diff`.
 * Useful when comparing JSON.
 */
function DiffRelease(props) {
  const {
    firstRelease,
    secondRelease,
    firstFilename,
    secondFilename,
    className,
  } = props;
  const classes = useStyles();
  const [releaseLinesDiff, setReleaseDiffLines] = useState([]);
  const [diffSummary, setDiffSummary] = useState(INITIAL_JS_DIFF_SUMMARY);
  const diffWorker = new DiffWorker();

  diffWorker.onmessage = e => {
    const releaseDiff = e.data;
    const lines = releaseDiff.split(NEW_LINES_REGEX);
    const diffSummary = lines.reduce((acc, curr) => {
      if (curr.startsWith('+') && !curr.startsWith('+++')) {
        return Object.assign(acc, { added: acc.added + 1 });
      }

      if (curr.startsWith('-') && !curr.startsWith('---')) {
        return Object.assign(acc, { removed: acc.removed + 1 });
      }

      return acc;
    }, clone(INITIAL_JS_DIFF_SUMMARY));

    setReleaseDiffLines(lines);
    setDiffSummary(diffSummary);
  };

  useEffect(() => {
    diffWorker.postMessage([
      firstFilename,
      secondFilename,
      JSON.stringify(deepSortObject(firstRelease), null, 2),
      JSON.stringify(deepSortObject(secondRelease), null, 2),
    ]);
  }, [firstFilename, secondFilename, firstRelease, secondRelease]);

  const handleRowRender = ({ index, key, style }) => {
    const line = releaseLinesDiff[index];
    // eslint-disable-next-line no-nested-ternary
    const backgroundColor = line.startsWith('+')
      ? DIFF_COLORS.ADDED
      : line.startsWith('-')
      ? DIFF_COLORS.REMOVED
      : 'unset';

    return (
      <div key={key} style={{ ...style, backgroundColor }}>
        <pre style={{ backgroundColor }} className={classes.pre}>
          {line}
        </pre>
      </div>
    );
  };

  const releaseLinesDiffCount = releaseLinesDiff.length;
  const listHeight = Math.min(releaseLinesDiffCount * 20, 350);

  return (
    Boolean(releaseLinesDiffCount) && (
      <Paper className={className}>
        <div className={classes.header}>
          <strong>
            <span className={classes.greenText}>+{diffSummary.added}</span>
          </strong>
          &nbsp;
          <strong>
            <span className={classes.redText}>-{diffSummary.removed}</span>
          </strong>
        </div>
        <div className={classes.listWrapper}>
          <List
            height={listHeight}
            rowRenderer={handleRowRender}
            overscanRowCount={50}
            rowCount={releaseLinesDiffCount}
            rowHeight={20}
            /* The only way I was able to make the list
            scrollable in the x-direction */
            width={CONTENT_MAX_WIDTH + 1000}
          />
        </div>
      </Paper>
    )
  );
}

DiffRelease.propTypes = {
  firstRelease: object.isRequired,
  secondRelease: object.isRequired,
  firstFilename: string.isRequired,
  secondFilename: string.isRequired,
  className: string,
};

DiffRelease.defaultProps = {
  className: null,
};

export default memo(DiffRelease);
