// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    self.do_search = function () {
        $.getJSON(search_url,
            {search_string: self.vue.search_string},
            function (data) {

                data.strings.forEach(product => {
                    product["link"] = "{{=URL('default', 'product_page', args=['"+product.id+"'])}}"
                });
                self.vue.strings = data.strings;
            });
    };
 
    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            strings: [],
            search_string: '',
            show_reviews:false,
        },
        methods: {
            do_search: self.do_search
        }

    });

    self.do_search();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});