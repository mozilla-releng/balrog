angular.module("app").factory('Page', function() {
   var title = '';
   return {
     title: function() { return title + ' - Balrog Admin'; },
     setTitle: function(newTitle) { title = newTitle; }
   };
});
