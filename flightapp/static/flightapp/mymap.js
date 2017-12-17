/**
* SVG path for target icon
*/
var targetSVG = "M9,0C4.029,0,0,4.029,0,9s4.029,9,9,9s9-4.029,9-9S13.971,0,9,0z M9,15.93 c-3.83,0-6.93-3.1-6.93-6.93S5.17,2.07,9,2.07s6.93,3.1,6.93,6.93S12.83,15.93,9,15.93 M12.5,9c0,1.933-1.567,3.5-3.5,3.5S5.5,10.933,5.5,9S7.067,5.5,9,5.5 S12.5,7.067,12.5,9z";
/**
* SVG path for plane icon
*/
var planeSVG = "m2,106h28l24,30h72l-44,-133h35l80,132h98c21,0 21,34 0,34l-98,0 -80,134h-35l43,-133h-71l-24,30h-28l15,-47";
/**
* Create the map
*/
function printsomestuff(arg) {
   console.log('Logging...');
   console.log(arguments);
}

window.map = null;

function changeAirport(airportId) {
   $.ajax({
       url: '/ajax/validate_airport/',
       data: {
          'id': airportId
       },
       dataType: 'json',
       success: function (data) {
          mapmap(data);
       },
       error: function (error) {
          console.log('ERROR!',error);
       }
   });
}

function updateAirport(name,lon,lat,city) {
   var airport = new AmCharts.MapImage();
   airport.title = '('+name+') <br />'+city;
   airport.latitude = lat;
   airport.longitude = lon;
   airport.svgPath = targetSVG;
   airport.zoomLevel = 5;
   airport.scale = 0.4;
   airport.chart = map;
   map.dataProvider.images.push( airport );
   airport.validate();
}

function updateLine(name,lon_from,lat_from,lon_to,lat_to) {
   var line = new AmCharts.MapLine();
   line.id = name.toString();
   line.arc = -0.3;
   line.alpha = 0.2;
   line.color = "#000";
   line.positionOnLine = 0.5;
   line.latitudes = [lat_from, lat_to];
   line.longitudes = [lon_from, lon_to];
   line.chart = map;
   map.dataProvider.lines.push( line );
   //console.log('line', line);
   line.validate();
}

function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp * 1000);
  var year = a.getFullYear();
  var mon = a.getMonth();
  var day = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = day + ' ' + mon + ' ' + year + ' (' + hour + ':' + min + ':' + sec + ')';
  return time;
}

function updatePlane(line_name,time,city_from,city_to,time_from,time_to) {
   var plane = new AmCharts.MapImage();
   var tfrom = timeConverter(time_from);
   var tto = timeConverter(time_to);
   plane.svgPath = planeSVG;
   plane.color = "#A52A2A";
   plane.animateAlongLine = true;
   plane.lineId = line_name.toString();
   plane.flipDirection = false;
   plane.loop = false;
   plane.scale = 0.04;
   plane.animationDuration = time;
   plane.adjustAnimationSpeed = false;
   plane.balloonText = 'raise: '+line_name+'<br />'+city_from+' - '+city_to+'<br />'+tfrom+' - '+tto;
   //plane.zoomLevel = 6;
   plane.chart = map;
   map.dataProvider.images.push( plane );
   plane.validate();
}


function mapmap (data) {
   updateAirport(data.is_taken_airport,data.is_taken_lon,data.is_taken_lat,data.is_taken_city);

   for (var i=0; i<data.arr_airports_to.length; i++) {
      updateAirport(data.arr_airports_to[i].airport,data.arr_airports_to[i].airport_longitude,data.arr_airports_to[i].airport_latitude,data.arr_airports_to[i].airport_city);
   }

   for (var i=0; i<data.arr_flights.length; i++) {
      console.log(data.arr_flights[i].code_flight)
      updateLine(data.arr_flights[i].code_flight,data.is_taken_lon,data.is_taken_lat,data.arr_flights[i].lon_to,data.arr_flights[i].lat_to);
      updatePlane(data.arr_flights[i].code_flight,data.arr_flights[i].time_of_flight/10,data.arr_flights[i].city_from,data.arr_flights[i].city_to,data.arr_flights[i].flight_from,data.arr_flights[i].flight_to);
      //console.log('time=', data.arr_flights[i].time_of_flight,' (',timeConverter(data.arr_flights[i].time_of_flight),')')
   }
}

function cleanmap () {
   window.map = AmCharts.makeChart( "chartdiv", {
  "type": "map",
  "theme": "none",
  "projection": "winkel3",
  "dataProvider": {
    "map": "worldLow",
    "lines": [ ],
    "images": [ ]
  },

  "areasSettings": {
    "unlistedAreasColor": "#8dd9ff"
  },

  "imagesSettings": {
    "color": "#000",
    "rollOverColor": "#585869",
    "selectedColor": "#585869",
    "pauseDuration": 0.2
  },

  "linesSettings": {
    "color": "#585869",
    "alpha": 0.4
  },

  "export": {
    "enabled": true
  }
} );
}

var map = AmCharts.makeChart( "chartdiv", {
  "type": "map",
  "theme": "none",
  "projection": "winkel3",
  "dataProvider": {
    "map": "worldLow",
    "lines": [ ],
    "images": [ ]
  },

  "areasSettings": {
    "unlistedAreasColor": "#8dd9ff"
  },

  "imagesSettings": {
    "color": "#000",
    "rollOverColor": "#585869",
    "selectedColor": "#585869",
    "pauseDuration": 0.2
  },

  "linesSettings": {
    "color": "#585869",
    "alpha": 0.4
  },

  "export": {
    "enabled": true
  }
} );

function updateTime() {
   console.log('Chart', window.map);
   if (window.map.dataProvider.images.length > 0) {
      for ( var i =0; i < window.map.dataProvider.images.length; i+=1) {
         if (window.map.dataProvider.images[i].svgPath == planeSVG) {
            setInterval(
               _updateMe(window.map.dataProvider.images[i], i), 1000);
         }
      }
   }
   console.log(window.map.dataProvider.images);
}

function _updateMe(item, iterator) {
   console.log(item);
   item.balloonText = item.balloonText + '123123';
   window.map.dataProvider.images[iterator] = item;
   window.map.dataProvider.images[iterator].validate();
}


