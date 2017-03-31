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
      .state('pred1', {
        url: '/prediction1/',
        templateUrl: 'app/views/predictions/prediction1/index.html',
        controller: 'PredictionController',
        controllerAs: 'ctrl',
        data:{
          cssClassnames: 'dashboard start'
        }
      })
      .state('pred2', {
          url: '/prediction2/',
          templateUrl: 'app/views/predictions/prediction2/index.html',
          controller: 'PredictionController2',
          controllerAs: 'ctrl',
          data:{
            cssClassnames: 'dashboard start'
          }
        })
      .state('pred3', {
          url: '/prediction3/',
          templateUrl: 'app/views/predictions/prediction3/index.html',
          controller: 'PredictionController3',
          controllerAs: 'ctrl',
          data:{
            cssClassnames: 'dashboard start'
          }
        });
  }

})(angular);
