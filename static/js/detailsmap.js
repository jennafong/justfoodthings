"use strict";


function initMap() {
    
    const bizLatitude = Number(document.querySelector("#details-map-info").getAttribute("business-latitude"))
    const bizLongitude = Number(document.querySelector("#details-map-info").getAttribute("business-longitude"))
    const bizName = document.querySelector("#details-map-info").getAttribute("business-name")
    const userLocation = document.querySelector("#details-map-info").getAttribute("user-location-center")

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

    const user = new google.maps.Marker({
      position: userLocation,
      title: 'User Location',
      map: basicMap
    });

    const restaurant = new google.maps.Marker({
      position: restaurantCoords,
      title: 'Restaurant Location',
      map: basicMap
    });
  
    const restuarantInfo = new google.maps.InfoWindow({
      content: bizName
    });
  
      const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        maxWidth: 200
      });
  
      marker.addListener('click', () => {
        infoWindow.open(basicMap, marker);
      });
    }
  }
 