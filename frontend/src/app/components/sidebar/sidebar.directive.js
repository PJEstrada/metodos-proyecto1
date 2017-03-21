(function (angular) {
  'use strict';

  angular
    .module('frontend.common.sidebar', ['weed'])
    .directive('sidebar', sidebar);

  function sidebar() {
    return {
      restrict: 'A',
      replace: true,
      scope: {},
      templateUrl: 'app/components/sidebar/sidebar.html',
      controller: sidebarController,
      controllerAs: 'ctrl'
    }
  }

  sidebarController.$inject = ['$state','$stateParams','$log'];

  function sidebarController($state,$stateParams,$log){

    var vm = this;
    vm.stateNum = -1;  // 1-> boards  2->committees 3-> allMyDashboards

    vm.state = $state;
    var stateNames = $state.current.name.split("-");
    if(stateNames[0] == 'board') {
      vm.stateNum = 1;
    }
    else if(stateNames[0] == 'committee') {
      vm.stateNum = 2;
    }
    else{
      vm.stateNum = 3;
    }
    // $log.log("STATE: ",$state);
    vm.idState = $stateParams.id;
  }
})(angular);
