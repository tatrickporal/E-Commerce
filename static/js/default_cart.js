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

    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};
    
    self.get_id = function() {
        $.getJSON(get_id_url,
            // Data we are sending.
            {
      
            },
            // What do we do when the post succeeds?
            function (data) {
                self.vue.user_id = data.id;
            }
        );
    };

    self.get_cart = function() {
        $.getJSON(get_cart_url,
            {
                user_id: self.vue.user_id
            },
            function(data) {
                self.vue.cart = data.cart_list;   
                self.process_cart();
            }
        );
    };

    self.process_cart = function() {
        enumerate(self.vue.cart);
        self.vue.cart.map(function (e) {
            // e["_shown"] = e.shown;
            Vue.set(e,"num_bought",1)
        });
        self.total_price();
    };

    self.total_price = function() {
        var ans = 0;
        self.vue.cart.map(function (e) {
            var price = e.num_bought * e.product_price;
            ans+=price;
        });
        self.vue.total_amount = ans;
    };

    self.add_bought = function(_idx) {
        var prod = self.vue.cart[_idx];
        prod.num_bought++;
        self.total_price();
    };
    self.remove_bought = function(_idx) {
        var prod = self.vue.cart[_idx];
        prod.num_bought--;
        self.total_price();
    };

    self.clear_cart = function() {
        console.log("klsajfklasj")
        $.post(clear_cart_url,
            // Data we are sending.
            {
      
            },
            // What do we do when the post succeeds?
            function (data) {
                self.get_cart();
                
            }
        );
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            cart:[],
            user_id:0,
            total_amount:0,
        },
        methods: {
            get_cart: self.get_cart,
            get_id: self.get_id,
            process_cart: self.process_cart,
            total_price: self.total_price,
            add_bought: self.add_bought,
            remove_bought: self.remove_bought,
            clear_cart: self.clear_cart
        }
    }); 
    // self.get_id();
    self.get_cart();
    self.process_cart();
    self.total_price();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
