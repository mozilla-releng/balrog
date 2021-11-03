export const handleSignoff = async (roles, details, dialogState, props) => {
  const { doSignoff, updateSignoffs, setDialogState} = props;
  const requiredRole = roles.filter(role => role in details.required_signoffs);

  if (requiredRole.length === 1) {
    const { error, result } = await doSignoff(requiredRole[0], details);

    if (!error) {
      updateSignoffs(result);
    }
  } else {
    setDialogState(dialogState);
  }
};