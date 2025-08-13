import { json } from '@codemirror/lang-json';
import { materialDark } from '@uiw/codemirror-theme-material';
import CodeMirror from '@uiw/react-codemirror';
import { bool, func, string } from 'prop-types';
import React from 'react';

function CodeEditor({ onChange, value, readOnly, ...rest }) {
  return (
    <CodeMirror
      value={value}
      onChange={onChange}
      theme={materialDark}
      extensions={[json()]}
      readOnly={readOnly}
      {...rest}
    />
  );
}

CodeEditor.propTypes = {
  onChange: func.isRequired,
  value: string.isRequired,
  readOnly: bool,
};

CodeEditor.defaultProps = {
  readOnly: false,
};

export default CodeEditor;
