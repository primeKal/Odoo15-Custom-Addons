odoo.define('test.shop_cart', function (require) {
    "use strict";

    console.log('hyy papiiiiiii i am working')
    var FormController = require('web.FormController');

    var formController = FormController.include({
        // start: function () {
        //     console.log('we are in form view')
        // },
 
        _click: function (event) {
            console.lSog('we are in form view clickkkkk')
            if (event.data.attrs.id === "12345678") {
                console.log('Test');
                alert('Test');
            }
            this._super(event);
        },
    });





    // $(document).on('click', '#12345678', function () {
    // console.log("test")
    // });
    // var dd =$('#12345678')
    // console.log('sdf',dd)
    // $('#12345678').click(function () {
    //     console.log("TEST")
    // });
    // return {
    //     start: function () {
    //         $('#12345678').click(function () {
    //             console.log("TEST")
    //         });
    //     },

    // }

});