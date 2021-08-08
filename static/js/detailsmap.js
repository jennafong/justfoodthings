"use strict";

// distance matrix api for map centering to get an idea of how zoomed in a map should be

function initMap() {
    
    const bizLatitude = Number(document.querySelector("#details-map-info").getAttribute("business-latitude"))
    const bizLongitude = Number(document.querySelector("#details-map-info").getAttribute("business-longitude"))
    const bizName = document.querySelector("#details-map-info").getAttribute("business-name")
    const userLatitude = Number(document.querySelector("#details-map-info").getAttribute("user-location-latitude"))
    const userLongitude = Number(document.querySelector("#details-map-info").getAttribute("user-location-longitude"))

    const userCoordinates = {
      lat: userLatitude,
      lng: userLongitude
    };

    const restaurantCoords = {
      lat: bizLatitude,
      lng: bizLongitude
    };
  
    const basicMap = new google.maps.Map(
      document.querySelector('#map'),
      {
        center: userCoordinates,
        zoom: 15
      }
    );

    const userMarker = new google.maps.Marker({
      position: userCoordinates,
      title: 'User Location',
      map: basicMap,
    });

    const userInfo = new google.maps.InfoWindow({
      content: '<b>You!</b>'
    });

    userInfo.open(basicMap, userMarker);
  
    const restaurantMarker = new google.maps.Marker({
      position: restaurantCoords,
      title: bizName,
      map: basicMap,
    });

    const restaurantInfo = new google.maps.InfoWindow({
      content: bizName,
    });

    restaurantInfo.open(basicMap, restaurantMarker);
  
  }
 