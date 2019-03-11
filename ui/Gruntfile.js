/*global module:false*/
module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-ng-constant');
  require('./config/lineman').config.grunt.run(grunt);
};
