function buildMetadata(coin) {

  // Use `d3.json` to fetch the metadata for a sample
  var url = "/historic/" + coin;
  // Select the panel with id of `#sample-metadata`
  var table = d3.select("#sample-metadata");
  // Clear any existing metadata
  table.html("");
  d3.json(url).then(function(data) {
  // Get the entries for each object in the array

  var name = coin[0];
  var nDate = data.Date[0];
  var popen = data.Open[0].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
  var phigh = data.High[0].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
  var plow = data.Low[0].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
  var pclose = data.Close[0].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
  var Volume = parseInt(data.Volume[0]);

  table.append("h5").text(`Date:    ${nDate}`);
  table.append("h5").text(`Open:   $${popen}`);
  table.append("h5").text(`High:   $${phigh}`);
  table.append("h5").text(`Low:    $${plow}`);
  table.append("h5").text(`Close:  $${pclose}`);
  table.append("h5").text(`Volume: ${Volume}`);

  /*
  Object.entries(data).forEach(([key, value]) => {
    table.append("h5").text(`${key}: ${value[0]}`);
    console.log(`Key: ${key} and Value ${value}`); 
    });
  */
  });
}

function buildCharts(sample) {
  var url = "/samples/" + sample;
  // Fetch the sample data for the plots
  d3.json(url).then(function(data) {
    // Get the entries for each object in the array
    var otu_ids = data['otu_ids'];
    var otu_labels = data['otu_labels'];
    var sample_values = data['sample_values'];

    piedata = [{
        "labels": otu_ids.slice(0,10),
        "values": sample_values.slice(0,10),
        "hovertext": otu_labels.slice(0,10),
        "type": "pie"}]

    var layout = {
      title: "Top 10 OTUs",
      height: 400,
      width: 500}
    // Plot the Pie Chart
    Plotly.newPlot("pie", piedata, layout);

    // Build bubble chart
    var trace1 = {
      x: otu_ids,
      y: sample_values,
      hovertext: otu_labels,
      mode: 'markers',
      marker: {
        size: sample_values,
        color: otu_ids
      }
    };
    
    var bubdata = [trace1];
    
    var bublayout = {
      title: 'OTUs Found',
      showlegend: false,
      height: 600,
      width: 1000
    };

    // Plot the Bubble Chart using the sample data
    Plotly.newPlot('bubble', bubdata, bublayout);
  });
}


function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/currencies").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    //buildCharts(firstSample);
    buildMetadata(firstSample);
    buildPlot(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  //buildCharts(newSample);
  buildMetadata(newSample);
  buildPlot(newSample);
}

// Initialize the dashboard
init();


///////////////////////////////

/**
 * Helper function to select stock data
 * Returns an array of values
 * @param {array} rows
 * @param {integer} index
 * index 0 - Date
 * index 1 - Open
 * index 2 - High
 * index 3 - Low
 * index 4 - Close
 * index 5 - Volume
 */
function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}


function buildTable(dates, openPrices, highPrices, lowPrices, closingPrices, volume) {
  var table = d3.select("#summary-table");
  var tbody = table.select("tbody");
  var trow;

  tbody.html("");

  for (var i = 0; i < 20; i++) {
    trow = tbody.append("tr");
    trow.append("td").text(dates[i]);
    trow.append("td").text(openPrices[i].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
    trow.append("td").text(highPrices[i].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
    trow.append("td").text(lowPrices[i].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
    trow.append("td").text(closingPrices[i].toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
    trow.append("td").text(parseInt(volume[i]));
  }
}

function buildPlot(coin) {
  var url = `/historic/` + coin;

  d3.json(url).then(function(data) {

    //console.log(data.Close);
    // Grab values from the response json object to build the plots
    var name = coin;
    var stock = coin;
    var startDate = Date.parse(data.Date.slice(-1)[0])
    var endDate = Date.parse(data.Date[0])
    var dates = data.Date.map(x => Date.parse(x))
    var openingPrices = data.Open;
    var highPrices = data.High;
    var lowPrices = data.Low;
    var closingPrices = data.Close;
    var Volume = data.Volume;

    //getMonthlyData();

    var trace1 = {
      type: "scatter",
      mode: "lines",
      name: name,
      x: dates,
      y: closingPrices,
      line: {
        color: "#17BECF"
      }
    };

    // Candlestick Trace
    var trace2 = {
      type: "candlestick",
      x: dates,
      high: highPrices,
      low: lowPrices,
      open: openingPrices,
      close: closingPrices
    };

    var plot_data = [trace1, trace2];

    var layout = {
      title: `${stock} closing prices`,
      xaxis: {
        range: [startDate, endDate],
        //autorange: true,
        type: "date"
      },
      yaxis: {
        autorange: true,
        type: "linear"
      },
      showlegend: false
    };

    console.log('Start Date: ' + startDate);
    console.log('End Date: ' + endDate);
    console.log(Date.parse(dates));

    Plotly.newPlot("plot", plot_data, layout);
    buildTable(data.Date, openingPrices, highPrices, lowPrices, closingPrices, Volume);
  });
}



// BONUS - Dynamically add the current date to the report header
var monthNames = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var today = new Date();
var date = `${monthNames[today.getMonth()]} ${today.getFullYear().toString().substr(2, 2)}`;

d3.select("#report-date").text(date);
