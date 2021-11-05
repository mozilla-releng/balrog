import React from 'react';
import { func, object } from 'prop-types';
import {
  revokeSignoffV2,
} from '../../../services/releases';
import useAction from '../../../hooks/useAction';
import Button from '../Button';

function SignoffButton({user, signoffs, roles, signoffType, updateSignoffs, setDialogState, setSignoffType }) {
  const [revokeAction, revoke] = useAction(props =>
    revokeSignoff({ type: 'releases', ...props })
  );
  const [revokeV2Action, revokeV2] = useAction(revokeSignoffV2);

  const doSignoff = async (roleToSignoffWith) => {
    // special conditions just for releases?
    if (signoffType.api_version === 1) {
      const { error } = await signoff({
        scId: signoffType.scheduledChange.sc_id,
        role: roleToSignoffWith,
      });

      return { error, result: { roleToSignoffWith, signoffType } };
    }

    const { error } = await signoffV2(signoffType.name, roleToSignoffWith);

    return { error, result: { roleToSignoffWith, signoffType } };
  };

  // const handleSignoffDialogSubmit = async () => {
  //   const { error, result } = await doSignoff(signoffRole, dialogState.item);

  //   if (error) {
  //     throw error;
  //   }

  //   return result;
  // };

  // const handleSignoffDialogComplete = result => {
  //   updateSignoffs(result);
  //   handleDialogClose();
  // };

  const handleRevoke = async () => {
    let error = null;
    // rules also use revoke, but doesn't check version first
    if (signoffType.api_version === 1) {
      ({ error } = await revoke({
        scId: signoffType.scheduledChange.sc_id,
        role: signoffType.scheduledChange.signoffs[username],
      }));
    } else {
      ({ error } = await revokeV2(signoffType.name));
    }

    if (!error) {
      setSignoffType(
        releases.map(r => {
          if (
            !r.scheduledChange ||
            r.scheduledChange.sc_id !== signoffType.scheduledChange.sc_id
          ) {
            return r;
          }

          const newSignoffType = clone(r);

          delete newSignoffType.scheduledChange.signoffs[username];

          return newSignoffType;
        })
      );
    }
  };
  const handleSignoff = async () => {
    const requiredRole = roles.filter(role => role in signoffType.required_signoffs);
  
    if (requiredRole.length === 1) {
      const { error, result } = await doSignoff(requiredRole[0]);
  
      if (!error) {
        updateSignoffs(result);
      }
    } else {
      setDialogState({
        // ...dialogState,
        open: true,
        destructive: false,
        title: 'Signoff as…',
        confirmText: 'Sign off',
        item: signoffType,
        mode: 'signoff',
        // handleSubmit: handleSignoffDialogSubmit,
        // handleComplete: handleSignoffDialogComplete,
      });
    }
  };
  return (user && user.email in signoffs ? (
    <Button color="secondary" disabled={!user} onClick={handleRevoke}>
      Revoke Signoff
    </Button>
  ) : (
    <Button color="secondary" disabled={!user} onClick={handleSignoff}>
      Signoff
    </Button>
  ))}

  SignoffsButton.propTypes = {
    emergencyShutoff: object,
    onSignoff: func.isRequired,
    onRevoke: func.isRequired,
  };

export default SignoffButton