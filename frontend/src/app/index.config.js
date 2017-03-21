(function() {
  'use strict';

  angular
    .module('frontend')
    .config(config);

  config.$inject = ['$logProvider', '$httpProvider', '$resourceProvider'];

  function config($logProvider, $httpProvider, $resourceProvider) {
    // Enable log
    $logProvider.debugEnabled(true);
    // This is the place where the interceptors are added.
    $httpProvider.interceptors.push('customInterceptor');
    $httpProvider.interceptors.push('authRedirectInterceptor');
    $resourceProvider.defaults.stripTrailingSlashes = false;
  }

})();
