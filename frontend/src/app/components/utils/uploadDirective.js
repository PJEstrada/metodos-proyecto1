(function (angular) {
  'use strict';

  angular
    .module('frontend.common.filesModel', ['weed'])
    .directive('filesModel', filesModelDirective);

  function filesModelDirective(){
    return {
      controller: function($parse, $element, $attrs, $scope){
        var exp = $parse($attrs.filesModel);

        $element.on('change', function(){
          exp.assign($scope, this.files);
          $scope.$apply();
        });
      }
    };
  }
  navbarController.$inject = [
    '$attrs',
    '$log',
    '$state',
    '$rootScope',
    '$stateParams',
    'moment',
    '$location',
    'WeedApi'
  ];

  function navbarController(
    $attrs,
    $log,
    $state,
    $rootScope,
    $stateParams,
    moment,
    $location,
    Socket,
    WeedApi
  ) {
    var vm = this;

    var channel = {};



  }
})(angular);

