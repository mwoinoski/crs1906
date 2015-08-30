var ticketmanor_controllers = angular.module('ticketmanor');
ticketmanor_controllers.controller('eventShowCtrl',['$scope', '$rootScope', '$state', 
  '$stateParams', '$timeout', '$window', '$interval', 'concerts', 'sports', 'movies',
  function($scope, $rootScope, $state, $stateParams, $timeout, $window, $interval, concerts, sports, movies) {
  var _scope = {};
  _scope.init = function() {
  }  
  $scope.open_popup = function(url) {
    var w = 500;
    var h = 680;
    var left_adjust = angular.isDefined($window.screenLeft) ? $window.screenLeft : $window.screen.left;
    var top_adjust = angular.isDefined($window.screenTop) ? $window.screenTop : $window.screen.top;
    var width = $window.innerWidth ? $window.innerWidth : $window.document.documentElement.clientWidth ? $window.document.documentElement.clientWidth : $window.screen.width;
    var height = $window.innerHeight ? $window.innerHeight : $window.document.documentElement.clientHeight ? $window.document.documentElement.clientHeight : $window.screen.height;
    var left = ((width / 2) - (w / 2)) + left_adjust;
    var top = ((height / 2) - (h / 2)) + top_adjust;
    var popup = $window.open(url, '', "top=" + top + ", left=" + left + ", width="+w+", height="+h);
  };
  _scope.init();
}]);