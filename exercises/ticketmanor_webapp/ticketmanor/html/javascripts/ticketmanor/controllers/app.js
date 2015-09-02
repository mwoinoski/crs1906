angular.module('ticketmanor', ['ui.router', 'ui.router.state', 'toastr', 'ngFx', 'ngAnimate', 'truncate','ui.bootstrap'])
  .config(['$stateProvider', '$urlRouterProvider',
  function($stateProvider, $urlRouterProvider) {  
  $urlRouterProvider.otherwise('/home');
  $stateProvider
  .state('root', {
    url: '',
    abstract: true,
    views: {
    'container': {
      templateUrl: "javascripts/ticketmanor/views/shared/home_container.html"
      }
    }
  })
  .state('root.home', {
    url: '/home',
    data : { pageTitle: 'TicketManor | Home' },
    views: {
    'header': {
      templateUrl: "javascripts/ticketmanor/views/shared/header.html",
      controller: "homeCtrl"
      },
    'home' : {
      templateUrl : "javascripts/ticketmanor/views/shared/home.html"
      }
    }
  })
  .state('events', {
    url: '',
    views: {
      'container': { 
        templateUrl: "javascripts/ticketmanor/views/shared/events.html",
        controller: "eventCtrl"
      }
    }
  })
  .state('events.show', {
    url: '',
    views: {
    'header': {
      templateUrl: "javascripts/ticketmanor/views/shared/header.html"
      },
    'events': {
      templateUrl: "javascripts/ticketmanor/views/shared/event_show.html",
      controller: "eventShowCtrl"
      }
    }
  })
  .state('events.show.login', {
    url: '/login',
    data : { pageTitle: 'TicketManor | Login' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/auth/login.html",
      controller: "AuthCtrl"
      }
    }
  })
  .state('events.show.signup', {
    url: '/signup',
    data : { pageTitle: 'TicketManor | Signup' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/auth/signup.html"
      }
    }
  })
  .state('events.show.concerts', {
    url: '/concerts',
    data : { pageTitle: 'TicketManor | Concerts' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/concerts/concerts.html"
      }
    }
  })
  .state('events.show.sports', {
    url: '/sports',
    data : { pageTitle: 'TicketManor | Sports' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/sports/sports.html"
      }
    }
  })   
  .state('events.show.movies', {
    url: '/movies',
    data : { pageTitle: 'TicketManor | Movies' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/movies/movies.html"
      }
    }
  })
  .state('events.show.all_news', {
    url: '/news',
    data : { pageTitle: 'TicketManor | All News' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/news/all_news.html"
      }
    }
  })
  .state('events.show.news', {
    url: '/:event_type/news/:news_id',
    data : { pageTitle: 'TicketManor | News' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/news/news.html"
      }
    }
  })
  .state('events.show.event', {
    url: '/:event_type/show/:event_id',
    data : { pageTitle: 'TicketManor | Events' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/shared/show.html"
      }
    }
  })
  .state('events.show.cart', {
    url: '/cart',
    data : { pageTitle: 'TicketManor | Cart' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/cart/cart.html"
      }
    }
  })
  .state('events.show.checkout', {
    url: '/checkout',
    data : { pageTitle: 'TicketManor | Checkout' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/cart/checkout.html"
      }
    }
  })
  .state('events.show.pay-success', {
    url: '/pay-success/:pay_id',
    data : { pageTitle: 'TicketManor | Success' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/cart/success.html",
      controller: "cartCtrl"
      }
    }
  })
  .state('events.show.chat', {
    url: '/chat',
    data : { pageTitle: 'TicketManor | Chat' },
    views: {
    'events': {
      templateUrl: "javascripts/ticketmanor/views/chat/chat.html",
      controller: "chatCtrl"
      }
    }
  });
}]).directive('pulse', function($animate) {
  return function(scope, ele) {
    ele.on('click', function() {
      $animate.animate(ele, 'meme')
      .then(function() {
      });
      scope.$apply();
    });
  }
});
