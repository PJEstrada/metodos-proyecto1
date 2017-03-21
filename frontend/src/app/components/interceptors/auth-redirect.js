(function(angular){
  'use strict';
  angular
    .module('frontend.interceptor.interceptor2', [])
    .factory('authRedirectInterceptor', authRedirectInterceptor);
authRedirectInterceptor.$inject = [
  '$injector',
  '$log',
  'WeedApi'
];


function authRedirectInterceptor(
  $injector,
  $log,
  WeedApi
){
  return {
    // The
    request: function(config) {
      return config
    },
    response: function(response) {
      // do something on success
      return response;
    },
    responseError: function(rejection) {


    }
  }
}



})(angular);
