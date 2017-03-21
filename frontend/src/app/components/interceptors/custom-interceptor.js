(function(angular){
  'use strict';

  angular
    .module('frontend.interceptor.interceptor1', [])
    .factory('customInterceptor', customInterceptor);

  // Dependency injections
  customInterceptor.$inject = ['$injector','$log'];



  function customInterceptor($injector, $log) {
    return {
      // Automatically attach Authorization header
      request: function(config) {
       // Delay injection
        //// $log.log("en interceptor")

        return config;
      },
      response: function(res){
        return res;
      }
    }
  }

})(angular);
