angular.module('ticketmanor').service('cart', ['$http', '$stateParams', '$rootScope', 'toastr',
  function($http, $stateParams, $rootScope, toastr) {
    var get_default = function() {
    return {
        list: [],
        single: {},
        statuses: []
    };
  }

  var list_cart = function(id, cart) {
    return $http.get('/rest/events/cart/1.json').
      success(function(response) {
       cart.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var add_qty =function(id, cart) {
    return $http.get('/rest/events/cart/2.json?id=id',{id: id}).
      success(function(response) {
       cart.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var remove_qty =function(id, cart) {
    return $http.get('/rest/events/cart/1.json?id=id',{id: id}).
      success(function(response) {
       cart.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var payment = function(card_info, amount, cart) {
    return $http.get('/rest/events/cart/1.json',{card_info: card_info, amount: amount, cart_list: cart.list}).
      success(function(response) {
        cart.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var payment_status = function(pay_id, cart) {
    return $http.get('/rest/events/cart/1.json?id=pay_id',{pay_id: pay_id}).
      success(function(response) {
        cart.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }
  
// public methods
   return {
    list: {
      get: list_cart,
      add: add_qty,
      remove: remove_qty
    },
    single: {
      payment: payment,
      status: payment_status
    },
    model: {
      get: get_default
    }
   }
}]);
