console.log('this is 3 blogs js')
// odoo.define('custom_web.3_blop', function (require) {
//     console.log('success in loading')
//     var PublicWidget = require('web.public.widget');
//     var rpc = require('web.rpc');
//     var Dynamic = PublicWidget.Widget.extend({
//         selector: '.dynamic_snippet_blog',
//         start: function () {
//             console.log('got the starter')
//             var self = this;
//             rpc.query({
//                 route: '/3blogs',
//                 params: {},
//             }).then(function (result) {
//                 console.log('hiiiiiii')
//                 self.$('#total_sold').text(result);
//             });
//         },
//     });
//     PublicWidget.registry.dynamic_snippet_blog = Dynamic;
//     return Dynamic;
//  });