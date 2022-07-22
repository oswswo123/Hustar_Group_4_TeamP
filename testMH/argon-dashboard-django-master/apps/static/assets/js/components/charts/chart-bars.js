//
// Bars chart
//

var BarsChart = (function() {
	// Variables
	var $chart = $('#chart-bars');

	// Methods
	// Init chart
	function initChart($chart) {

		// Create chart
		var ordersChart = new Chart($chart, {
			type: 'bar',
			data: {
				labels: ['Positive', 'Negative'],
				datasets: [{
					label: 'Opinion',
					data: [21, 9]
				}]
			}
		});

		// Save to jQuery object
		$chart.data('chart', ordersChart);
	}

	// Init chart
	if ($chart.length) {
		initChart($chart);
	}

})();
