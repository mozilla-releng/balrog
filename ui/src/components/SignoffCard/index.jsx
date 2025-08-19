import EditIcon from '@mui/icons-material/Edit';
import Card from '@mui/material/Card';
import CardActionArea from '@mui/material/CardActionArea';
import CardHeader from '@mui/material/CardHeader';
import { node, string } from 'prop-types';
import React from 'react';
import { makeStyles } from 'tss-react/mui';
import Link from '../../utils/Link';

const useStyles = makeStyles()((theme) => ({
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
  const { classes } = useStyles();
  const { title, children, to, ...rest } = props;

  return (
    <Card {...rest}>
      <Link className={classes.link} to={to}>
        <CardActionArea>
          <CardHeader
            classes={{ action: classes.cardHeaderAction }}
            className={classes.cardHeader}
            action={<EditIcon className={classes.linkIcon} />}
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
