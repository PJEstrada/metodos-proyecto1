(function(angular) {
  'use strict';

  // Module fetch
  angular
    .module('frontend')
    .controller(
      'PredictionController2',
      predictionController);

  predictionController.$inject = [
    '$scope',
    '$stateParams',
    '$log',
    '$state',
    'WeedApi',
    'moment',
    'ApiGetPredictions',
    'ApiGetFinanceData',
    'ApiGetMovingAverage'
  ];
  function predictionController(
    $scope,
    $stateParams,
    $log,
    $state,
    WeedApi,
    moment,
    ApiGetPredictions,
    ApiGetFinanceData,
    ApiGetMovingAverage
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
    vm.loading = false;
    vm.uploadDataset = function(){
      $log.log(vm.newDataset);
      ApiGetPredictions.save(vm.newDataset,function(response){
        vm.fetchMeterData();
      });
    };

    vm.forecast = function(){
      vm.loading = true;
      vm.forecastResource = new ApiGetMovingAverage();
      vm.loading = 'loading';
      vm.forecastResource.$get(function(response){
        $log.log("FORECAST RESPONSE MOVING AVERAGE");
        $log.log(response);
        // Populating prediction data
        for(var i =0; i<response.prediccion.length; i++){
          if(response.prediccion[i].pk == null){
            $scope.data[1].push({'x': response.prediccion[i].fecha , 'y': response.prediccion[i].cobro} )
          }

        }
        for(var i =0; i<response.prediccion.length; i++){
          if(response.prediccion[i].pk == null){
            $scope.data[2].push({'x': response.prediccion[i].fecha , 'y': response.prediccion[i].cobro+response.prediccion[i].std} )
          }

        }
        for(var i =0; i<response.prediccion.length; i++){
          if(response.prediccion[i].pk == null){
            $scope.data[3].push({'x': response.prediccion[i].fecha , 'y': response.prediccion[i].cobro-response.prediccion[i].std} )
          }

        }
        vm.loading = '';
        vm.refreshGrid();
        vm.showError = true;
        vm.error = response.error;

      });
    }
    // Fetch All predictions
    vm.fetchMeterData = function () {

      $scope.series = ["Reales", "Pronostico", "Error-Superior", "Error-Inferior"];
      $scope.datasetOverride = [{ yAxisID: 'y-axis-1' }, { yAxisID: 'y-axis-2' }, { yAxisID: 'y-axis-3' }, { yAxisID: 'y-axis-4' }];
      $scope.data = [
        [],
        [],
        [],
        []
      ];
      vm.timeseries = new ApiGetFinanceData();
      vm.timeseries.$get(function(response){
        vm.loading = false;
        vm.dataseries = response.timeseries;
       for (var i=0; i< vm.dataseries.length; i++){
         $scope.data[0].push({'x': vm.dataseries[i].fecha , 'y': vm.dataseries[i].cobro })
        }
        vm.refreshGrid();

      });


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

        $scope.options = {
          type:'line',
          fill:false,
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
      },
      { backgroundColor : 'rgba(220,220,220,0)',
        pointBackgroundColor: '#FF0000',
        pointHoverBackgroundColor: '#FF0000',
        borderColor: '#FF0000',
        pointBorderColor: '#FF0000',
        pointHoverBorderColor: '#FF0000',
        fill: 'rgba(220,220,220,0)' /* this option hide background-color */
      },
        { backgroundColor : 'rgba(220,220,220,0)',
          pointBackgroundColor: '#00FF00',
          pointHoverBackgroundColor: '#00FF00',
          borderColor: '#00FF00',
          pointBorderColor: '#00FF00',
          pointHoverBorderColor: '#00FF00',
          fill: 'rgba(220,220,220,0)' /* this option hide background-color */
        },
        { backgroundColor : 'rgba(220,220,220,0)',
          pointBackgroundColor: '#451b74',
          pointHoverBackgroundColor: '#451b74',
          borderColor: '#451b74',
          pointBorderColor: '#451b74',
          pointHoverBorderColor: '#451b74',
          fill: 'rgba(220,220,220,0)' /* this option hide background-color */
        },];
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
