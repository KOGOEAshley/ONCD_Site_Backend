document.addEventListener('DOMContentLoaded', function () {
  var latInput = document.getElementById('id_latitude');
  var lngInput = document.getElementById('id_longitude');
  if (!latInput || !lngInput) return;

  var mapContainer = document.createElement('div');
  mapContainer.id = 'clinique-map-picker';
  mapContainer.style.height = '350px';
  mapContainer.style.marginBottom = '10px';
  mapContainer.style.border = '1px solid #ccc';
  mapContainer.style.borderRadius = '6px';

  var latRow = latInput.closest('.form-row') || latInput.closest('.field-latitude') || latInput.parentNode;
  latRow.parentNode.insertBefore(mapContainer, latRow);

  var hint = document.createElement('p');
  hint.className = 'help';
  hint.style.marginBottom = '15px';
  hint.textContent = 'Cliquez sur la carte pour positionner la clinique, ou glissez le repère.';
  latRow.parentNode.insertBefore(hint, latRow);

  var startLat = parseFloat(latInput.value) || 12.3714;
  var startLng = parseFloat(lngInput.value) || -1.5197;
  var zoomDepart = latInput.value ? 14 : 7;

  var map = L.map('clinique-map-picker').setView([startLat, startLng], zoomDepart);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map);

  var marker = L.marker([startLat, startLng], { draggable: true }).addTo(map);

  function remplirChamps(lat, lng) {
    latInput.value = lat.toFixed(6);
    lngInput.value = lng.toFixed(6);
  }

  marker.on('dragend', function () {
    var pos = marker.getLatLng();
    remplirChamps(pos.lat, pos.lng);
  });

  map.on('click', function (e) {
    marker.setLatLng(e.latlng);
    remplirChamps(e.latlng.lat, e.latlng.lng);
  });
});