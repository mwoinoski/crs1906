var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('chatCtrl',['$scope', '$stateParams', '$rootScope', '$state', 
  '$timeout', 'chat', function($scope, $stateParams, $rootScope, $state, $timeout, chat) {
  var _scope = {};
  _scope.init = function() { 
    $scope.welcome_view = true;
    $scope.chat_view = false;
    $rootScope.chat_button = true;
    $scope.isCollapsed = false;
    $scope.toggle = true
    $scope.chat = chat.model.get();
    // if($rootScope.current_user) {
    //   $state.go('events.show.chat');
    // } else {
    //   $state.go('events.show.login');
    // }
  }
  $scope.welcome = function(welcome_params) {
    console.log(welcome_params)
    chat.list.get(welcome_params, $scope.chat).then(function(response) {
      $scope.welcome_view = false;
      $scope.chat_view = true;
    });
  }
  $scope.send = function(message, user) {
    chat.single.post($scope.chat, message, user).then(function(response) {
      $scope.message = "";
    });
  }
  $scope.envite = function(email) {
    chat.single.invite(email, $scope.chat).then(function(response) {
      $scope.isCollapsed = false;
    });
  }
  $scope.close = function() {
    window.close();
  }
  _scope.init();
}]);