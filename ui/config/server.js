/* Define custom server-side HTTP routes for lineman's development server
 *   These might be as simple as stubbing a little JSON to
 *   facilitate development of code that interacts with an HTTP service
 *   (presumably, mirroring one that will be reachable in a live environment).
 *
 * It's important to remember that any custom endpoints defined here
 *   will only be available in development, as lineman only builds
 *   static assets, it can't run server-side code.
 *
 * This file can be very useful for rapid prototyping or even organically
 *   defining a spec based on the needs of the client code that emerge.
 *
 */

module.exports = {
  drawRoutes: function(app) {

    app.get('/api/rules', function(req, res) {
      res.json({
        rules: [
          {
            product: "Firefox",
            channel: "nightly",
            mapping: "Firefox-mozilla-central-nightly-latest",
            rate: 100,
            priority: 1,
            id: 1
          },
          {
            product: "Firefox",
            channel: "aurora",
            mapping: "Firefox-mozilla-aurora-latest",
            rate: 90,
            priority: 2,
            id: 2
          },
        ],
        count: 2
      });
    });
    // app.post('/login', function(req, res) {
    //   res.json({ message: 'logging in!' });
    // });
    //
    // app.post('/logout', function(req, res) {
    //   res.json({ message: 'logging out!'});
    // });
    //
    // app.get('/books', function (req, res) {
    //   res.json([
    //     {title: 'Great Adventures', author: 'Dickens'},
    //     {title: 'Foundation Series', author: 'Asimov'},
    //     {title: 'Treasure Island', author: 'Stephenson'}
    //   ]);
    // });

  }
};
