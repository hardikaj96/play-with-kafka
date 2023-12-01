var liveChart = Highcharts.chart('liveChart', {
    chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
    },
    title: {
        text: 'Live Timeseries Data'
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: 'Value'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '</b><br/>' +
                Highcharts.numberFormat(this.y, 2);
        }
    },
    legend: {
        enabled: true
    },
    exporting: {
        enabled: true
    },
    accessibility: {
        enabled: false
    },
    series: [
        { name: 'Numeric 1', data: [] },
        { name: 'Numeric 2', data: [] },
        { name: 'Numeric 3', data: [] },
        { name: 'Numeric 4', data: [] }
    ]
});

// Function to add data to the chart
async function addData() {
    try {
        const latestTimestamp = localStorage.getItem('latestTimestamp');

        // Append the latest timestamp to the API endpoint
        const apiUrl = `/api/data?latestTimestamp=${latestTimestamp}`;

        const response = await fetch(apiUrl);
        const data = await response.json();
        const { documents, latest_timestamp } = data;
        console.log(data);
        if (documents && documents.length > 0) {
            localStorage.setItem('latestTimestamp', latest_timestamp);

            // Loop through each document and add data to the chart
            documents.forEach(doc => {
                var x = (new Date(doc.datetime)).getTime(); // current time

                // Add the data to the chart for each numeric value
                liveChart.series[0].addPoint([x, doc.numeric_1], true, false);
                liveChart.series[1].addPoint([x, doc.numeric_2], true, false);
                liveChart.series[2].addPoint([x, doc.numeric_3], true, false);
                liveChart.series[3].addPoint([x, doc.numeric_4], true, false);
            });

            // Remove the first data point if the chart has too many points
            if (liveChart.series[0].data.length > 15) {
                liveChart.series.forEach(series => series.data[0].remove());
            }
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Fetch prepopulated data
async function fetchPrepopulatedData() {
    try {
        const response = await fetch('/prepopulate');  // Replace with your actual API endpoint
        const data = await response.json();
        console.log(data);
        const { documents, latest_timestamp } = data;

        // Store the latest timestamp in local storage
        localStorage.setItem('latestTimestamp', latest_timestamp);
        // Initialize the chart with prepopulated data
        liveChart.update({
            series: [
                { name: 'Numeric 1', data: documents.map(item => [(new Date(item.datetime)).getTime(), item.numeric_1]) },
                { name: 'Numeric 2', data: documents.map(item => [(new Date(item.datetime)).getTime(), item.numeric_2]) },
                { name: 'Numeric 3', data: documents.map(item => [(new Date(item.datetime)).getTime(), item.numeric_3]) },
                { name: 'Numeric 4', data: documents.map(item => [(new Date(item.datetime)).getTime(), item.numeric_4]) }
            ]
        });
    } catch (error) {
        console.error('Error fetching prepopulated data:', error);
    }
}

// Initialize the chart with an initial fetch of prepopulated data
fetchPrepopulatedData();

// Simulate live data updates
setInterval(addData, 3000); // Update every 3 seconds
