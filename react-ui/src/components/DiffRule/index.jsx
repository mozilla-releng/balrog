import React, { useMemo } from 'react';
import { makeStyles } from '@material-ui/styles';
import { diffLines, formatLines } from 'unidiff';
import { Diff, Hunk, parseDiff } from 'react-diff-view';
import { rule } from '../../utils/prop-types';
import getDiff from '../../utils/diff';
import getDiffedProperties from '../../utils/getDiffedProperties';
import { RULE_DIFF_PROPERTIES } from '../../utils/constants';

const useStyles = makeStyles(theme => ({
  diff: {
    fontSize: theme.typography.body2.fontSize,
    marginTop: theme.spacing(1),
    display: 'block',
    overflowX: 'auto',
    '& .diff-code': {
      whiteSpace: 'nowrap',
    },
    '& colgroup': {
      width: '100%',
    },
  },
}));

function DiffRule(props) {
  const classes = useStyles();
  const { firstRule, secondRule } = props;
  const diffedProperties = getDiffedProperties(
    RULE_DIFF_PROPERTIES,
    firstRule,
    secondRule
  );
  const diff = useMemo(() => {
    const [oldText, newText] = getDiff(diffedProperties, firstRule, secondRule);
    const diffText = formatLines(diffLines(oldText, newText), {
      context: 0,
    });
    const [diff] = parseDiff(diffText, { nearbySequences: 'zip' });

    return diff;
  }, [firstRule, secondRule]);

  return diff && diff.type ? (
    <Diff
      className={classes.diff}
      viewType="split"
      diffType={diff.type}
      hunks={diff.hunks || []}>
      {hunks => hunks.map(hunk => <Hunk key={hunk.content} hunk={hunk} />)}
    </Diff>
  ) : null;
}

DiffRule.propTypes = {
  firstRule: rule.isRequired,
  secondRule: rule.isRequired,
};

export default DiffRule;
