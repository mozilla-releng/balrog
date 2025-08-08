import { makeStyles } from '@material-ui/styles';
import { createPatch } from 'diff';
import React, { useMemo } from 'react';
import { Diff, Hunk, parseDiff } from 'react-diff-view';
import 'react-diff-view/style/index.css';
import { RULE_DIFF_PROPERTIES } from '../../utils/constants';
import getDiff from '../../utils/diff';
import getDiffedProperties from '../../utils/getDiffedProperties';
import { rule } from '../../utils/prop-types';
import tokenize from './tokenize';

const useStyles = makeStyles((theme) => ({
  diff: {
    fontSize: theme.typography.body2.fontSize,
    marginTop: theme.spacing(1),
    display: 'block',
    overflowX: 'auto',
    '& .diff-code': {
      whiteSpace: 'pre',
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
    secondRule,
  );
  const diff = useMemo(() => {
    const [oldText, newText] = getDiff(diffedProperties, firstRule, secondRule);

    if (!oldText && !newText) {
      return '';
    }

    const patchText = createPatch(
      'rules',
      oldText,
      newText,
      undefined,
      undefined,
      {
        context: 0,
      },
    );

    // createPatch adds `Index: filename\n==========\n` at the top which `parseDiff` does not like
    const diffText = patchText.split('\n').slice(2).join('\n');

    const [diff] = parseDiff(diffText, { nearbySequences: 'zip' });

    return diff;
  }, [firstRule, secondRule]);
  const tokens = useMemo(() => tokenize(diff.hunks), [diff.hunks]);

  return diff?.type ? (
    <Diff
      className={classes.diff}
      viewType="split"
      diffType={diff.type}
      hunks={diff.hunks || []}
      tokens={tokens}
    >
      {(hunks) => hunks.map((hunk) => <Hunk key={hunk.content} hunk={hunk} />)}
    </Diff>
  ) : null;
}

DiffRule.propTypes = {
  firstRule: rule.isRequired,
  secondRule: rule.isRequired,
};

export default DiffRule;
