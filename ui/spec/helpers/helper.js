var root = this;

root.context = root.describe;
root.xcontext = root.xdescribe;

console.dbg = function() {
  for (var i = 0; i < arguments.length; i++) {
    var argument = arguments[i];
    if (typeof argument === 'object' || typeof argument === 'string') {
      console.log(JSON.stringify(argument, undefined, 2));
    } else {
      console.log(argument);
    }
  }
};
