let dataset = []
let provinsi = []
let map;
let totalData;
let sentiment;
let koordinat = [
    {
      "id": "11",
      "name": "ACEH",
      "alt_name": "ACEH",
      "latitude": 4.36855,
      "longitude": 97.0253
    },
    {
      "id": "12",
      "name": "SUMATERA UTARA",
      "alt_name": "SUMATERA UTARA",
      "latitude": 2.19235,
      "longitude": 99.38122
    },
    {
      "id": "13",
      "name": "SUMATERA BARAT",
      "alt_name": "SUMATERA BARAT",
      "latitude": -1.34225,
      "longitude": 100.0761
    },
    {
      "id": "14",
      "name": "RIAU",
      "alt_name": "RIAU",
      "latitude": 0.50041,
      "longitude": 101.54758
    },
    {
      "id": "15",
      "name": "JAMBI",
      "alt_name": "JAMBI",
      "latitude": -1.61157,
      "longitude": 102.7797
    },
    {
      "id": "16",
      "name": "SUMATERA SELATAN",
      "alt_name": "SUMATERA SELATAN",
      "latitude": -3.12668,
      "longitude": 104.09306
    },
    {
      "id": "17",
      "name": "BENGKULU",
      "alt_name": "BENGKULU",
      "latitude": -3.51868,
      "longitude": 102.53598
    },
    {
      "id": "18",
      "name": "LAMPUNG",
      "alt_name": "LAMPUNG",
      "latitude": -4.8555,
      "longitude": 105.0273
    },
    {
      "id": "19",
      "name": "KEPULAUAN BANGKA BELITUNG",
      "alt_name": "KEPULAUAN BANGKA BELITUNG",
      "latitude": -2.75775,
      "longitude": 107.58394
    },
    {
      "id": "21",
      "name": "KEPULAUAN RIAU",
      "alt_name": "KEPULAUAN RIAU",
      "latitude": -0.15478,
      "longitude": 104.58037
    },
    {
      "id": "31",
      "name": "DKI JAKARTA",
      "alt_name": "DKI JAKARTA",
      "latitude": -6.1745,
      "longitude": 106.8227
    },
    {
      "id": "32",
      "name": "JAWA BARAT",
      "alt_name": "JAWA BARAT",
      "latitude": -6.88917,
      "longitude": 107.64047
    },
    {
      "id": "33",
      "name": "JAWA TENGAH",
      "alt_name": "JAWA TENGAH",
      "latitude": -7.30324,
      "longitude": 110.00441
    },
    {
      "id": "34",
      "name": "DI YOGYAKARTA",
      "alt_name": "DI YOGYAKARTA",
      "latitude": -7.7956,
      "longitude": 110.3695
    },
    {
      "id": "35",
      "name": "JAWA TIMUR",
      "alt_name": "JAWA TIMUR",
      "latitude": -6.96851,
      "longitude": 113.98005
    },
    {
      "id": "36",
      "name": "BANTEN",
      "alt_name": "BANTEN",
      "latitude": -6.44538,
      "longitude": 106.13756
    },
    {
      "id": "51",
      "name": "BALI",
      "alt_name": "BALI",
      "latitude": -8.23566,
      "longitude": 115.12239
    },
    {
      "id": "52",
      "name": "NUSA TENGGARA BARAT",
      "alt_name": "NUSA TENGGARA BARAT",
      "latitude": -8.12179,
      "longitude": 117.63696
    },
    {
      "id": "53",
      "name": "NUSA TENGGARA TIMUR",
      "alt_name": "NUSA TENGGARA TIMUR",
      "latitude": -8.56568,
      "longitude": 120.69786
    },
    {
      "id": "61",
      "name": "KALIMANTAN BARAT",
      "alt_name": "KALIMANTAN BARAT",
      "latitude": -0.13224,
      "longitude": 111.09689
    },
    {
      "id": "62",
      "name": "KALIMANTAN TENGAH",
      "alt_name": "KALIMANTAN TENGAH",
      "latitude": -1.49958,
      "longitude": 113.29033
    },
    {
      "id": "63",
      "name": "KALIMANTAN SELATAN",
      "alt_name": "KALIMANTAN SELATAN",
      "latitude": -2.94348,
      "longitude": 115.37565
    },
    {
      "id": "64",
      "name": "KALIMANTAN TIMUR",
      "alt_name": "KALIMANTAN TIMUR",
      "latitude": 0.78844,
      "longitude": 116.242
    },
    {
      "id": "65",
      "name": "KALIMANTAN UTARA",
      "alt_name": "KALIMANTAN UTARA",
      "latitude": 2.72594,
      "longitude": 116.911
    },
    {
      "id": "71",
      "name": "SULAWESI UTARA",
      "alt_name": "SULAWESI UTARA",
      "latitude": 0.65557,
      "longitude": 124.09015
    },
    {
      "id": "72",
      "name": "SULAWESI TENGAH",
      "alt_name": "SULAWESI TENGAH",
      "latitude": -1.69378,
      "longitude": 120.80886
    },
    {
      "id": "73",
      "name": "SULAWESI SELATAN",
      "alt_name": "SULAWESI SELATAN",
      "latitude": -3.64467,
      "longitude": 119.94719
    },
    {
      "id": "74",
      "name": "SULAWESI TENGGARA",
      "alt_name": "SULAWESI TENGGARA",
      "latitude": -3.54912,
      "longitude": 121.72796
    },
    {
      "id": "75",
      "name": "GORONTALO",
      "alt_name": "GORONTALO",
      "latitude": 0.71862,
      "longitude": 122.45559
    },
    {
      "id": "76",
      "name": "SULAWESI BARAT",
      "alt_name": "SULAWESI BARAT",
      "latitude": -2.49745,
      "longitude": 119.3919
    },
    {
      "id": "81",
      "name": "MALUKU",
      "alt_name": "MALUKU",
      "latitude": -3.11884,
      "longitude": 129.42078
    },
    {
      "id": "82",
      "name": "MALUKU UTARA",
      "alt_name": "MALUKU UTARA",
      "latitude": 0.63012,
      "longitude": 127.97202
    },
    {
      "id": "91",
      "name": "PAPUA BARAT",
      "alt_name": "PAPUA BARAT",
      "latitude": -1.38424,
      "longitude": 132.90253
    },
    {
      "id": "94",
      "name": "PAPUA",
      "alt_name": "PAPUA",
      "latitude": -3.98857,
      "longitude": 138.34853
    }
  ]
const popup = new mapboxgl.Popup();
let pieChart, barChart;
/** 
 * Request API
 */
const allData = () => {    
    $.get('http://localhost:5000/api/data', (data, status) => {
        dataset = data.data        
    })
    $.get('http://localhost:5000/api/province', (data, status) => {
        provinsi = data.data
        console.log(provinsi)
    })
    $.get('http://localhost:5000/api/sentiment', (data, status) => {
        sentiment = data.data
        totalData = data.total
        console.log('init');
        console.log(sentiment);
        console.log(totalData);
        
        initChart(sentiment)
    })
}

const dataByProv = (prov) => {
    $.get(`http://localhost:5000/api/sentiment/${prov}`, (data, status) => {
        sentiment = data.data        
        settingChart(sentiment)
    })
}

const dataAll = () => {
    $.get('http://localhost:5000/api/sentiment', (data, status) => {
        sentiment = data.data
        dataSentiment = {
          1: sentiment[0],
          2: sentiment[1],
          3: sentiment[2]
        }      
        settingChart(dataSentiment)
    })
}

/**
 * Setting Mapbox
 */
const settingMapbox = () => {
    mapboxgl.accessToken = 'pk.eyJ1IjoiYWZmYW5kMjAiLCJhIjoiY2p0bGIxYWhkMDZldzQzb2pkdnh5OWZmcCJ9.mqau-lAF-9yDP5-FLPejiQ';
    map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [117.8205, -2.2593],
        zoom: 4.2,    
    });

    map.on('load', function() {

        provinsi.forEach( (item, index) => {
            addMap(item)
        })
    })
}

const addMap = (prov) => {
    map.addSource(prov, {
        'type':'geojson',
        'data': `http://localhost:5000/js/geo/${prov}.geojson`
    })        

    map.addLayer({
        'id':prov,
        'type':'fill',
        'source':prov,
        'layout':{},
        'paint': {
            'fill-color': '#088',
            'fill-opacity': 0.8
        }
    })

    map.on('click', prov, (e) => {        
        $('.list_provinsi').removeAttr('selected')
        dataByProv(prov)

        const selector = prov.toLowerCase().split(' ').join('_')
        $(`#${selector}`).attr('selected', 'true')

        provinsi.forEach((value, index) => {
            map.setPaintProperty(value, 'fill-opacity', 0.3)
        })
        
        let latlng = koordinat.filter(id => id.name == prov)
        latlng = [latlng[0].longitude, latlng[0].latitude]

        map.setPaintProperty(prov, 'fill-opacity', 0.8)
        
        map.flyTo({
            center: latlng,
            zoom:5.5,
            speed: 0.2,
            essential: true
        })       
    })

    map.on('mouseenter', prov, (e) => {
        popup.setLngLat(e.lngLat)
            .setHTML(e.features[0].properties.name)
            .addTo(map)

        map.getCanvas().style.cursor = 'pointer'
    })

    map.on('mouseleave', prov, () => {
        popup.remove()

        map.getCanvas().style.cursor = ''
    })
}

/**
 * Init ChartJS
 */
const initChart = (dataSentiment) => {
    var ctx = document.getElementById('myChart');
    var ctx = document.getElementById('myChart').getContext('2d');
    var ctx = $('#myChart');
    var ctx = 'myChart';

    // var ctxBar = document.getElementById('barChart');
    // var ctxBar = document.getElementById('barChart').getContext('2d');
    // var ctxBar = $('#barChart');
    // var ctxBar = 'barChart';

    var data = {
        datasets: [{
            data: dataSentiment,
            backgroundColor: [
                '#4CAF50',
                '#FF5252',
                '#455A64'
            ],
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Positif',
            'Negatif',
            'Netral'
        ]
    };

    pieChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: {
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        var percentage = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] || '';
                        var label = data.labels[tooltipItem.index]
                        console.log(label);
                        console.log(percentage);

                        if (label) {
                            label += ': ';
                        }
                        label += `${((percentage/totalData)*100).toFixed(2)}%`;
                        
                        return label;
                    }
                }
            }
        }
    })

    // barChart = new Chart(ctxBar, {
    //     type: 'bar',
    //     data: data
    // })
}

const settingChart = (dataSentiment) => {    
    console.log(dataSentiment);    
    pieChart.data.datasets[0].data = [dataSentiment[1], dataSentiment[2], dataSentiment[3]]    
    pieChart.update();
}

$('#select-provinsi').on('change', function() {
    const prov = $('#select-provinsi option:selected').attr('id').toUpperCase().split('_').join(' ')
    
    if (prov == 'ALL') {
      provinsi.forEach((value, index) => {
        map.setPaintProperty(value, 'fill-opacity', 0.8)
        map.flyTo({
          center: [117.8205, -2.2593],
          zoom: 4.2,
          seped: 0.2,
          essential: true
        })
      })
      dataAll()
    } else {
      provinsi.forEach((value, index) => {
        map.setPaintProperty(value, 'fill-opacity', 0.3)
        map.flyTo({
          center: [117.8205, -2.2593],
          zoom: 4.2,
          seped: 0.2,
          essential: true
        })
      })
  
      if (provinsi.indexOf(prov)!=-1) {
          dataByProv(prov)
          let latlng = koordinat.filter(id => id.name == prov)
          console.log(latlng)
          latlng = [latlng[0].longitude, latlng[0].latitude]
  
          map.setPaintProperty(prov, 'fill-opacity', 0.8)
  
          map.flyTo({
              center: latlng,
              zoom:5.5,
              speed: 0.2,
              essential: true
          })
      } else {
          $('.toast').toast('show')        
      }
    }    
})

const requestIntervally = () => {
    let timeout = 1000 * 60 * 10
    setTimeout(run = () => {        
        setTimeout(run, timeout)
    }, timeout);
}