process.env.NODE_ENV = process.env.NODE_ENV || 'test';

module.exports = {
  rootDir: `${__dirname}`,
  moduleDirectories: ['node_modules'],
  moduleFileExtensions: ['web.jsx', 'web.js', 'wasm', 'jsx', 'js', 'json'],
  moduleNameMapper: {
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/__jest__/fileMock.js',
    '\\.(css|less|sass|scss)$': '<rootDir>/__jest__/styleMock.js',
    '^react-native$': '<rootDir>/node_modules/react-native-web',
  },
  bail: true,
  collectCoverageFrom: ['src/**/*.{mjs,jsx,js}'],
  testEnvironment: 'jsdom',
  testRegex: 'test/.*(_test|_spec|\\.test|\\.spec)\\.(mjs|jsx|js)$',
  verbose: false,
  transform: {
    '\\.(mjs|jsx|js)$': '<rootDir>/__jest__/transformer.js',
  },
};
