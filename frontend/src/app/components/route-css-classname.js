(function (angular) {
  'use strict';

  angular
    .module('frontend.common.routeCssClassname', [])
    .directive('fiRouteClassNames', routeCssClassnames);

    // Dependency injection
    routeCssClassnames.$inject = ['$rootScope'];

    function routeCssClassnames($rootScope) {
      return {
        restrict: 'A',
        scope: {},
        link: function (scope, elem) {

          elem.one = $rootScope.$on(
            '$stateChangeSuccess',
            function (event, toState, toParams, fromState) {
              var fromClassnames = angular.isDefined(fromState.data) && angular.isDefined(fromState.data.cssClassnames) ? fromState.data.cssClassnames : null;
              var toClassnames = angular.isDefined(toState.data) && angular.isDefined(toState.data.cssClassnames) ? toState.data.cssClassnames : null;

              // Don't do anything if they are the same
              if (fromClassnames != toClassnames) {
                if (fromClassnames) {
                  elem.removeClass(fromClassnames);
                }

                if (toClassnames) {
                  elem.addClass(toClassnames);
                }
              }
            }
          );
        }
      }
    }
})(angular);
