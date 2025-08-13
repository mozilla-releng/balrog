import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/styles';
import { useVirtualizer } from '@tanstack/react-virtual';
import deepSortObject from 'deep-sort-object';
import { object, string } from 'prop-types';
import { clone } from 'ramda';
import React, { memo, useEffect, useRef, useState } from 'react';
import {
  DIFF_COLORS,
  INITIAL_JS_DIFF_SUMMARY,
  NEW_LINES_REGEX,
} from '../../utils/constants';
import DiffWorker from './diff.worker';

const useStyles = makeStyles((theme) => ({
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
  const parentRef = useRef(null);
  const classes = useStyles();
  const [releaseLinesDiff, setReleaseDiffLines] = useState([]);
  const [diffSummary, setDiffSummary] = useState(INITIAL_JS_DIFF_SUMMARY);
  const diffWorker = new DiffWorker();
  diffWorker.onmessage = (e) => {
    const releaseDiff = e.data;
    const lines = releaseDiff.split(NEW_LINES_REGEX);
    const diffSummary = lines.reduce((acc, curr) => {
      if (curr.startsWith('+') && !curr.startsWith('+++')) {
        acc.added++;
      }

      if (curr.startsWith('-') && !curr.startsWith('---')) {
        acc.removed++;
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

    // This component usually renders multiple times, and because
    // the diff is done asynchronously in a worker, the last one to
    // finish will "win" and be displayed. Terminating the current worker
    // in a cleanup function like this will make sure any old workers
    // from previous renders cannot win the race, because they most recent
    // one will always start (and finish) after any old ones have been
    // terminated.
    return () => diffWorker.terminate();
  }, [firstFilename, secondFilename, firstRelease, secondRelease]);

  const handleRowRender = (index, key, ref) => {
    const line = releaseLinesDiff[index];
    const backgroundColor = line.startsWith('+')
      ? DIFF_COLORS.ADDED
      : line.startsWith('-')
        ? DIFF_COLORS.REMOVED
        : 'unset';

    return (
      <div ref={ref} data-index={index} key={key} style={{ backgroundColor }}>
        <pre style={{ backgroundColor }} className={classes.pre}>
          {line}
        </pre>
      </div>
    );
  };

  const releaseLinesDiffCount = releaseLinesDiff.length;
  const virtualizer = useVirtualizer({
    count: releaseLinesDiffCount,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 20,
  });

  const items = virtualizer.getVirtualItems();
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
        <div
          className={classes.listWrapper}
          ref={parentRef}
          style={{ maxHeight: 350, overflowY: 'auto' }}
        >
          <div
            style={{
              height: virtualizer.getTotalSize(),
              position: 'relative',
            }}
          >
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                transform: `translateY(${items[0]?.start ?? 0}px)`,
                minWidth: '101%',
              }}
            >
              {virtualizer.getVirtualItems().map((virtualRow) => {
                return handleRowRender(
                  virtualRow.index,
                  virtualRow.key,
                  virtualRow.measureElement,
                );
              })}
            </div>
          </div>
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
