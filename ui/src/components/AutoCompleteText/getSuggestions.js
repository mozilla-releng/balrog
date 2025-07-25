export default (suggestions) => (value) => {
  const inputValue = value.trim().toLowerCase();
  const inputLength = inputValue.length;

  return inputLength === 0
    ? suggestions
    : suggestions.filter(
        (suggestion) =>
          suggestion.slice(0, inputLength).toLowerCase() === inputValue,
      );
};
