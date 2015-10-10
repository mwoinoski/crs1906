var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('cartCtrl',['$scope', '$stateParams', '$rootScope', '$state', 
  '$timeout', 'cart', function($scope, $stateParams, $rootScope, $state, $timeout, cart) {
  var _scope = {};
  _scope.init = function() {
    $scope.cart = cart.model.get();
    $rootScope.view_cart = false;
    $scope.cart_count = 0;
    if($stateParams.pay_id) {
      cart.single.status($stateParams.pay_id, $scope.cart).then(function(response) {
        if(response.data.pay_id == $stateParams.pay_id) {
          if(response.data.status = 'Success') {
            $state.go('events.show.pay-success',{pay_id: $stateParams.pay_id});
          } else {
            $state.go('events.show.checkout');
          }
        } else {
          $state.go('root.home');
        }
      });
    }
  }
  $scope.add_to_cart = function(id) {
    cart.list.get(id, $scope.cart).then(function(response) {
      $rootScope.view_cart = true;
      $scope.cart_count += 1;
    });
  }
  $scope.checkout = function() {
    if(!$rootScope.current_user) {
      $state.go("events.show.login");
    } else {
      $state.go("events.show.checkout")
    }
  }
  $scope.add_qty = function(id) {
    cart.list.add(id, $scope.cart);
  }
  $scope.remove_qty = function(id) {
    cart.list.remove(id, $scope.cart);
  }
  $scope.payment = function(card, amount) {
    cart.single.payment(card, amount, $scope.cart).then(function(response) {
      if(response.data.pay_id && response.data.status == "Success") {
        $state.go("events.show.pay-success",{'pay_id':response.data.pay_id});
        $rootScope.view_cart = false;
        $scope.cart_count = 0;
      } else {
        $state.go("events.show.checkout");
      }
    });
  }
  _scope.init();
}]);