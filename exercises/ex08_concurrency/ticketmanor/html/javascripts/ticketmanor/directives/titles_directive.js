var ticketmanor_directive = angular.module('ticketmanor');
ticketmanor_directive.directive('updateTitle', ['$rootScope', '$timeout',
  function($rootScope, $timeout) {
    return {
      restrict: 'A',
      link: function(scope, element) {
        var listener = function(event, toState) {
          var title = 'TicketManor';
          if (toState.data && toState.data.pageTitle) 
            title = toState.data.pageTitle;
            $timeout(function() {
            element.text(title);
          }, 0, false);
        };
        $rootScope.$on('$stateChangeSuccess', listener);
      }
    };
  }
]);

ticketmanor_directive.directive('ngEnter', function () {
  return function (scope, element, attrs) {
    element.bind("keydown keypress", function (event) {
      if(event.which === 13) {
        scope.$apply(function (){
          scope.$eval(attrs.ngEnter);
        });
        event.preventDefault();
      }
    });
  };
});
