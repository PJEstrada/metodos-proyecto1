(function(angular) {
  'use strict';

  angular
    .module('frontend')
    .config(routerConfig);

  routerConfig.$inject = ['$stateProvider'];

  /** @ngInject */
  function routerConfig($stateProvider) {
    $stateProvider
      .state('metersHome', {
        url: '/',
        templateUrl: 'app/views/predictions/prediction1/index.html',
        controller: 'PredictionController',
        controllerAs: 'ctrl',
        data:{
          cssClassnames: 'dashboard start'
        }
      })
      .state('meter', {
        url: '/prediction1/',
        templateUrl: 'app/views/predictions/prediction1/index.html',
        controller: 'PredictionController',
        controllerAs: 'ctrl',
        data:{
          cssClassnames: 'dashboard start'
        }
      });
  }

})(angular);
