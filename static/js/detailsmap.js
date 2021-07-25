"use strict";


function initMap() {


    const restaurantCoords = {
      lat: 42,
      lng: 42
    };
  
    const basicMap = new google.maps.Map(
      document.querySelector('#map'),
      {
        center: restaurantCoords,
        zoom: 11
      }
    );
  
    const sfMarker = new google.maps.Marker({
      position: restaurantCoords,
      title: 'SF Bay',
      map: basicMap
    });
  
    sfMarker.addListener('click', () => {
      alert('Hi!');
    });
  
    const sfInfo = new google.maps.InfoWindow({
      content: '<h1>San Francisco!</h1>'
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
 