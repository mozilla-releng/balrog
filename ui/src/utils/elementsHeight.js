export default (theme) => {
  const { htmlFontSize, h6, body1, body2, subtitle1, button } =
    theme.typography;

  return {
    h6TextHeight: parseFloat(h6.fontSize) * htmlFontSize * h6.lineHeight,
    body1TextHeight: (lines = 1) =>
      lines * parseFloat(body1.fontSize) * htmlFontSize * body1.lineHeight,
    body2TextHeight: (lines = 1) =>
      lines * parseFloat(body2.fontSize) * htmlFontSize * body2.lineHeight,
    subtitle1TextHeight: (lines = 1) =>
      lines *
      parseFloat(subtitle1.fontSize) *
      htmlFontSize *
      subtitle1.lineHeight,
    buttonHeight:
      parseFloat(button.fontSize) * htmlFontSize * button.lineHeight + 12,
    signoffSummarylistSubheaderTextHeight:
      parseFloat(subtitle1.fontSize) * htmlFontSize * 1.5,
  };
};
