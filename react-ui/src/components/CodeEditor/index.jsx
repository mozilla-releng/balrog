import React from 'react';
import { string, func, bool } from 'prop-types';
import { Controlled as CodeMirror } from 'react-codemirror2';
import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/material.css';

function CodeEditor({ onChange, value, readOnly, ...rest }) {
  return (
    <CodeMirror
      value={value}
      onBeforeChange={(editor, data, value) => {
        onChange(value);
      }}
      options={{
        mode: 'application/json',
        theme: 'material',
        indentWithTabs: false,
        lineNumbers: true,
        readOnly: readOnly ? 'nocursor' : false,
      }}
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
