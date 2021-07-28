"use strict";


function initMap() {
    
    const bizLatitude = Number(document.querySelector("#details-map-info").getAttribute("business-latitude"))
    const bizLongitude = Number(document.querySelector("#details-map-info").getAttribute("business-longitude"))
    const bizName = document.querySelector("#details-map-info").getAttribute("business-name")

    const restaurantCoords = {
      lat: bizLatitude,
      lng: bizLongitude
    };
  
    const basicMap = new google.maps.Map(
      document.querySelector('#map'),
      {
        center: restaurantCoords,
        zoom: 15
      }
    );
  
    const sfMarker = new google.maps.Marker({
      position: restaurantCoords,
      title: 'Restaurant Location',
      map: basicMap
    });
  
    sfMarker.addListener('click', () => {
      alert('Hi!');
    });
  
    const sfInfo = new google.maps.InfoWindow({
      content: '<h4>bizName</h4>'
    });
  
    sfInfo.open(basicMap, sfMarker);
  
  
    const locations = [
      {
        name: 'Hackbright Academy',
        coords: {
          lat: 37.7887459,
          lng: -122.4115852
        }
      },
      {
        name: 'Powell Street Station',
        coords: {
          lat: 37.7844605,
          lng: -122.4079702
        }
      },
      {
        name: 'Montgomery Station',
        coords: {
          lat: 37.7894094,
          lng: -122.4013037
        }
      },
    ];
  
    const markers = [];
    for (const location of locations) {
      markers.push(new google.maps.Marker({
        position: location.coords,
        title: location.name,
        map: basicMap,
        icon: {  // custom icon
          url: '/static/img/marker.svg',
          scaledSize: {
            width: 30,
            height: 30
          }
        }
      }));
    }
  
    for (const marker of markers) {
      const markerInfo = (`
        <h1>${marker.title}</h1>
        <p>
          Located at: <code>${marker.position.lat()}</code>,
          <code>${marker.position.lng()}</code>
        </p>
      `);
  
      const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        maxWidth: 200
      });
  
      marker.addListener('click', () => {
        infoWindow.open(basicMap, marker);
      });
    }
  }
 