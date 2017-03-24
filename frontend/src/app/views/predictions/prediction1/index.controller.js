(function(angular) {
  'use strict';

  // Module fetch
  angular
    .module('frontend')
    .controller(
      'PredictionController',
      predictionController);

  predictionController.$inject = [
    '$scope',
    '$stateParams',
    '$log',
    '$state',
    'WeedApi',
    'moment',
    'ApiGetPredictions',
    'ApiGetFinanceData'
  ];
  function predictionController(
    $scope,
    $stateParams,
    $log,
    $state,
    WeedApi,
    moment,
    ApiGetPredictions,
      ApiGetFinanceData
  ) {
    var vm = this;
    vm.display_mode = "date";
    // Initial end time is current hour
    vm.endTime = new Date(2015,12,31,0,0,0);
    vm.endTimeHours = new Date();
    // Set format for HTML input field
    vm.endTimeInput = moment(vm.endTime).format("HH:mm");
    // Set initial hour as curent hour minus 1 hour
    vm.initialTime = new Date(2012,1,1,0,0,0);
    vm.initialTimeHours = new Date();
    vm.initialTime.setDate(vm.initialTime.getDate() - 1);
    vm.initialTimeHours.setDate(vm.initialTimeHours.getDate() - 1);
    // Set format for HTML input field
    vm.initialTimeInput = moment(vm.initialTime).format("HH:mm");
    vm.newDataset = {};

    vm.uploadDataset = function(){
      $log.log(vm.newDataset);
      ApiGetPredictions.save(vm.newDataset,function(response){
        vm.fetchMeterData();
      });
    };

    // Fetch All predictions
    vm.fetchMeterData = function () {
      vm.data = [[]];
      vm.series = [];
      vm.timeseries = new ApiGetFinanceData();
      vm.timeseries.$get(function(response){
        vm.dataseries = response.timeseries;
        for (var i=0; i< vm.dataseries.length; i++){
          vm.data[0].push({'x': vm.dataseries[i].fecha , 'y': vm.dataseries[i].cobro })
        }
       vm.refreshGrid();

      })


    };

    vm.refreshGrid = function(){
        vm.updateChartOptions();
    };
    /*
     * This function updates the axis on the chart so it
     * reflects any new data it has received.
     * */
    vm.updateChartOptions = function (){
      // Get the min and max levels of the current data

        vm.options = {
          type:'line',
          fill:'rgba(220,220,220,0)',
          scales: {
            xAxes: [{
              type:"time",
              time:{
                min: vm.initialTime,
                max: vm.endTime
              },
              position: 'bottom'
            }]
          }
        };
      $scope.colors = [{
        backgroundColor : 'rgba(220,220,220,0)',
        pointBackgroundColor: '#0062ff',
        pointHoverBackgroundColor: '#0062ff',
        borderColor: '#0062ff',
        pointBorderColor: '#0062ff',
        pointHoverBorderColor: '#0062ff',
        fill: 'rgba(220,220,220,0)' /* this option hide background-color */
      }, '#00ADF9', 'rgba(220,220,220,0)', 'rgba(220,220,220,0)'];
    };

    function getAveragesEntries(data, divisor ){
      var initTime = new Date(vm.initialTime.getTime());
      var dateList = [];
      var endTime = new Date(vm.endTime.getTime());
      var currentTime = new Date(vm.initialTime.getTime());
      var i = 0;
      var result = [];
      while(currentTime < endTime){
        // Add minutes divisor
        currentTime.setMinutes(currentTime.getMinutes()+divisor);

        // Filter dates between current time and previous time
        var timeA = -1;
        var timeB = currentTime;
        if (dateList==0){
          // If is the first iteration, use initial time
          timeA = initTime;
        }
        else{
          // Else, use the previous time
          timeA = dateList[i-1];
        }
        // Save new interval
        dateList.push(new Date(currentTime.getTime()));
        var filteredData = filterDates(data,timeA,timeB);
        if (filteredData == 0){
          // If there are now plots on the interval, try to get the previous input
          if(result.length > 0){
            averageLevel = result[i-1].level;
            result.push({'time': currentTime, 'level': averageLevel});
          }
          else{
            result.push({'time': currentTime, 'level': undefined});
          }

        }
        // If we have data in the interval
        else{
          // Calculate Average
          var averageLevel = 0;
          for(var j = 0; j<filteredData.length; j++){
            averageLevel += filteredData[j].level;
          }
          averageLevel = averageLevel/filteredData.length;
          result.push({'time': new Date(currentTime.getTime()), 'level': averageLevel});
        }

        i++;
      }
      return result;

    }

    /**
     *
     * Filter dates between the dates a and b
     * list is a json of the form {'level': xx, 'time': xx}
     * @param a
     * @param b
     */
    function filterDates(list, a, b){
      var result = [];
      for(var i=0; i < list.length; i++){
        if(list[i].time >= a && list[i].time<=b){
          result.push(list[i]);
        }
      }
      return result;
    }

    vm.fetchMeterData();
  }
})(angular);
