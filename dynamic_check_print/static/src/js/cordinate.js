console.log('hiiiiiiiiiiiiiiiiiiiiiiiiiii')
odoo.define('dynamic_check_print', function (require) {
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var QWeb = core.qweb;
    // var ParamTemplate = $(QWeb.render("dynamic_check_print.Check", {}));
    var FormEditorDialog = Dialog.extend({
        // xmlDependencies: ['dynamic_check_print/static/src/xml/check_template.xml'],
        init: function (parent, options) {
            this._super(parent, _.extend({
                buttons: [{
                    text: _t('Save'),
                    classes: 'btn-primary',
                    close: true,
                    click: this._onSaveModal.bind(this),
                }, {
                    text: _t('Cancel'),
                    close: true
                }],
            }, options));
        },
        _onSaveModal: function () {
            console.log('here we will save it in future')
        },
    });
    $(document).on('click', '#1234eeeee', function () {
        console.log('this is much better')
       console.log(ParamTemplate)
        dialog = new FormEditorDialog(self, {
            title: 'Check',
            size: 'large',
            // $content: ParamTemplate,
        }).open();
    });
    "use strict";
    var form_widget = require('web.FormRenderer');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    // form_widget.include({
    //     on_click: function() {
    //         console.log('this is the utton',this)
    //          if(this.node.attrs.custom === "click"){
    //             console.log('gooot you')
    //             //code //
    //          return;
    //          }
    //          this._super();
    //     },
    //     start : function(){
    //         console.log('ggggggggggggg')
    //         this._super();
    //     },
    //     _addOnClickAction: function ($el, node) {

    //         var self = this;

    //         $el.click(function () {
    //             if(node.attrs.id === "1234eeeee"){
    //                 console.log('no wayyyy');

    //             }
    //         })
    //     },
    // });
    });