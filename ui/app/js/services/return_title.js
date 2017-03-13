angular.module("app").factory('Page', function() {
   var title = 'Balrog Admin Interface';
   return {
     title: function() { return title; },
     setTitle: function(newTitle) { title = newTitle; }
   };
});
