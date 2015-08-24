angular.module('ticketmanor').service('concerts', ['$http', '$stateParams', '$rootScope', 'toastr',
  function($http, $stateParams, $rootScope, toastr) {
    var get_default = function() {
      return {
          list: [],
          single: {},
          statuses: []
      };
    }

  var list_news = function(news) {
    return $http.get('/rest/news/concerts.json', {params: {max_items: 10}}).  //MW 2015-07-28
      success(function(response) {
       news.list = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var news = function(news_id, news) {
//    return $http.get('/rest/events/concerts/news/1.json',{news_id: news_id}).  //MW 2015-07-28
    return $http.get('/rest/news/concerts/' + news_id + '.json').
      success(function(response) {
      news.single = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var list_search = function(concerts_params, concerts, page, page_size) {
//    return $http.get('/rest/events/concerts/list.json?page=page&page_size=page_size', {params: concerts_params.single}).
    concerts_params.single['page'] = page
    concerts_params.single['page_size'] = page_size
    return $http.get('/rest/events/music.json', {params: concerts_params.single}).
      success(function(response) {
        concerts.title = response.title
        concerts.description = response.notes
        concerts.list.events_length = response.events.length;
        if(page == 0) {
          concerts.list.page_back = page;
        } else {
          concerts.list.page_back = page-1;
        }
        concerts.list.events = response.events.splice(page*page_size, page_size)
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }

  var event = function(event_id, event) {
    return $http.get('/rest/events/music',{event_id: event_id}).
      success(function(response) {
      event.single = response;
    }).error(function(response) {
      toastr.error('Something went wrong');
    });
  }
  
// public methods
   return {
    list: {
      get_news: list_news,
      search: list_search
    },
    single: {
      get_news: news,
      get_event: event
    },
    model: {
      get: get_default
    }
   }
}]);

angular.module('ticketmanor').directive('ngEnter', function() {
        return function(scope, element, attrs) {
            element.bind("keydown, keypress", function(event) {
                if(event.which === 13) {
                    scope.$apply(function(){
                        scope.$eval(attrs.ngEnter, {'event': event});
                    });

                    event.preventDefault();
                }
            });
        };
    });
