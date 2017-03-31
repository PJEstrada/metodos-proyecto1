/**
 * Created by venator on 6/2/16.
 */
(function(angular) {
  'use strict';

  // finance module creation
  angular
    .module('frontend.api', [
      'ngResource',
      'api.ApiGetPredictions',
      'api.ApiGetFinanceData',
      'api.ApiGetSTLM',
      'api.ApiGetMovingAverage',
      'api.ApiGetWeightedMovingAverage'
    ]);
})(angular);
