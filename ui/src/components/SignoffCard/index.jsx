import React from 'react';
import { makeStyles } from '@material-ui/styles';
import { node, string } from 'prop-types';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardActionArea from '@material-ui/core/CardActionArea';
import PencilIcon from 'mdi-react/PencilIcon';
import Link from '../../utils/Link';

const useStyles = makeStyles(theme => ({
  cardHeader: {
    borderBottom: '1px gray dashed',
  },
  cardHeaderAction: {
    alignSelf: 'end',
  },
  linkIcon: {
    marginRight: theme.spacing(1),
  },
  link: {
    ...theme.mixins.link,
  },
}));

function SignoffCard(props) {
  const classes = useStyles();
  const { title, children, to, ...rest } = props;

  return (
    <Card {...rest}>
      <Link className={classes.link} to={to}>
        <CardActionArea>
          <CardHeader
            classes={{ action: classes.cardHeaderAction }}
            className={classes.cardHeader}
            action={<PencilIcon className={classes.linkIcon} />}
            title={title}
          />
        </CardActionArea>
      </Link>
      {children}
    </Card>
  );
}

SignoffCard.propTypes = {
  /** A title for the signoff card. */
  title: string.isRequired,
  /** A link to navigate when the title is clicked. */
  to: string.isRequired,
  /* The content of the signoff card. */
  children: node.isRequired,
};

export default SignoffCard;
