(function (angular) {
  'use strict';

  angular
    .module('frontend.common.navbar', ['weed'])
    .directive('navbar', navbar);

  function navbar() {
    return {
      restrict: 'A',
      replace: true,
      scope: {},
      templateUrl: 'app/components/navbar/navbar.html',
      controller: navbarController,
      controllerAs: 'ctrl'
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