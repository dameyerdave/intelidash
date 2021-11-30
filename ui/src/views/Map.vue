<script setup>
import 'leaflet/dist/leaflet.css'
import { ref, computed, onMounted } from 'vue'
import L, { latLng, latLngBounds } from 'leaflet'
import { project, unproject } from 'swissgrid'
import { createTextVNode } from 'vue'
import {
  LMap,
  LIcon,
  LTileLayer,
  LMarker,
  LControlLayers,
  LTooltip,
  LPopup,
  LPolyline,
  LPolygon,
  LRectangle,
  LGeoJson,
} from "@vue-leaflet/vue-leaflet"

const SR=3857

const available_layers = ref(null)
const available_geojson_layers = ref(null)

async function loadLayers() {
  const res = await fetch(`https://api3.geo.admin.ch/rest/services/api/MapServer/layersConfig?sr=${SR}&lang=de`)
  const layers = await res.json()
  console.log('--layers--', layers)
  
  available_layers.value = Object.values(layers).filter(layer => layer.type === 'wmts').map(layer => {
    return {
      label: layer.label, value: 
      {
        id: layer.serverLayerName, 
        timestamp: layer.timestamps[0]
      }
    }
  })

  available_geojson_layers.value = Object.values(layers).filter(layer => layer.type === 'geojson').map(layer => {
    return {
      label: layer.label, 
      value: layer.geojsonUrl
    }
  })
}
loadLayers()

const base_map = `https://wmts20.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/${SR}/{z}/{x}/{y}.jpeg`
// const url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
const selected_layers = ref([])
const selected_geojson_layer = ref([])
const search_string = ref(null)
const zoom = ref(8)
function zoomUpdate(value) {
  zoom.value = value
}
const center = ref(latLng(46.57591, 7.84956))
// SW / NO
const bounds = ref(latLngBounds(
  { lat: 46.5, lng: 7.8 },
  { lat: 46.6, lng: 7.9 }
))
function boundsUpdate(value) {
  bounds.value = value
  // update_bounds_v95()
}
const bounds_v95 = ref(null)
async function update_bounds_v95() {
  const res1 = await fetch(`https://geodesy.geo.admin.ch/reframe/wgs84tolv95?northing=${bounds.value._southWest.lat}&easting=${bounds.value._southWest.lng}&format=json`)
  const res2 = await fetch(`https://geodesy.geo.admin.ch/reframe/wgs84tolv95?northing=${bounds.value._northEast.lat}&easting=${bounds.value._northEast.lng}&format=json`)
  const b1 = await res1.json()
  const b2 = await res2.json()
  bounds_v95.value = [
    Number(b1.easting),
    Number(b1.northing), 
    Number(b2.easting), 
    Number(b2.northing)
  ]
}

const yourPosition = ref(null)
const mapOptions = ref({
  zoomSnap: 0.5
})

const iconSize = 32
const dynamicSize = computed(() => [iconSize * 1.5, iconSize])
const dynamicAnchor = computed(() => [iconSize * 1.5 / 2, iconSize])

const geojson = ref(null)
async function loadGeoJson(url) {
  console.log('--geojson--', url)
  const res = await fetch(url)
  const LV95 = await res.json()
  for (const feature of LV95.features) {
      console.log('--feature--', feature)
      feature.geometry.coordinates = unproject(feature.geometry.coordinates)
  }
  geojson.value = LV95
  console.log('--geojson value--', geojson.value)
}
// const geojson_options = ref(null)
// const geojson_options_style = ref(null)

function handleFeature(feature, layer) {
  console.log('--handleFeature--', feature, layer)
  if (feature.properties) {
    layer.bindPopup(feature.properties.label || feature.properties.description || '')
  }
}

function pointToLayer(feature, latlng) {
  console.log('--pointToLayer--', feature, feature.properties.label || feature.properties.description)
  let marker = L.marker(latlng)
  if (feature.properties.icon) {
    marker = L.marker(latlng, {
      icon: L.icon({alt: feature.properties.label || feature.properties.description || '', iconUrl: feature.properties.icon, iconSize: dynamicSize.value, iconAnchor: dynamicAnchor.value}),
      title: feature.properties.label || feature.properties.description || '',
    })
  }
  //marker.bindPopup(createTextVNode(feature.properties.label || feature.properties.description || ''))
  return marker
}

const search_result = ref(null)
const selected_search_origins = ref(['zipcode','gg25','district','kantone','gazetteer','address','parcel'])
const search_origin_options = [
  {value: 'zipcode', label: 'zipcode'},
  {value: 'gg25', label: 'gg25'},
  {value: 'district', label: 'district'},
  {value: 'kantone', label: 'kantone'},
  {value: 'gazetteer', label: 'gazetteer'},
  {value: 'address', label: 'address'},
  {value: 'parcel', label: 'parcel'},
]
async function search(value) {
  const res = await fetch(`https://api3.geo.admin.ch/rest/services/api/SearchServer?searchText=${value}&type=locations&geometryFormat=geojson&origins=${selected_search_origins.value.join(',')}&sr=4326`)
  search_result.value = await res.json()
  console.log('--search_result--', search_result.value)
}

const map_entries = ref(null)
async function updateMapEntires() {
  const res = await fetch('http://localhost:8000/api/mapentries/geojson/')
  map_entries.value = await res.json()
}
updateMapEntires()

const pointerCoords = ref(null)
function udpatePointerCoords(event) {
  pointerCoords.value = event.latlng
}

onMounted(() => {
  if('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(pos => {
      yourPosition.value = latLng(pos.coords.latitude, pos.coords.longitude);
    }, err => {
      console.error(err)
    })
  }   
})
</script>

<template>
  <div style="height: 1000px; width: 100%">
    {{ pointerCoords }}
    <l-map
      :zoom="zoom"
      :center="center"
      :bounds="bounds"
      :options="mapOptions"
      style="height: 80%"
      @update:zoom="zoomUpdate"
      @update:bounds="boundsUpdate"
      @mousemove="udpatePointerCoords">
      <l-tile-layer
        :url="base_map"
        attribution="" />
      <l-tile-layer v-for="(layer, idx) in selected_layers" :key="'layer'+idx"
        :url="`https://wmts20.geo.admin.ch/1.0.0/${layer.id}/default/${layer.timestamp}/${SR}/{z}/{x}/{y}.png`"/>
      <l-marker v-if="yourPosition" :lat-lng="yourPosition">
        <l-icon
          :icon-size="[iconSize, iconSize]"
          :icon-anchor="[iconSize / 2, iconSize / 2]"
          icon-url="https://pbs.twimg.com/profile_images/1134237351520002048/AEgh9Mhi_400x400.png" />
        <l-popup>
          <div>
            You!
          </div>
        </l-popup>
      </l-marker>
      <l-geo-json
        v-if="geojson"
        :geojson="geojson"
        :options="{onEachFeature: handleFeature}">
      </l-geo-json>
      <l-geo-json
        v-if="search_result"
        :geojson="search_result"
        :options="{onEachFeature: handleFeature}">
      </l-geo-json>
      <l-geo-json
        v-if="map_entries"
        :geojson="map_entries"
        :options="{pointToLayer: pointToLayer}">
      </l-geo-json>
    </l-map>
    <n-input v-model:value="search_string" type="text" placeholder="Search" @change="(value) => search(value)" />
    <n-checkbox-group v-model:value="selected_search_origins">
      <n-space item-style="display: flex;">
        <n-checkbox v-for="option in search_origin_options" :key="option.value" :value="option.value" :label="option.label" />
      </n-space>
    </n-checkbox-group>
    <n-select v-if="available_layers" v-model:value="selected_layers" multiple filterable :options="available_layers" />
    <n-select v-if="available_geojson_layers" v-model:value="selected_geojson_layer" :options="available_geojson_layers" filterable @update:value="(value) => loadGeoJson(value)"/>
  </div>
</template>

<style>
.leaflet-popup-content img {
  width: 100%;
}
</style>