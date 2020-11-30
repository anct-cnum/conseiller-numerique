export interface GeoJsonPoint {
  type: string;  // always Point
  coordinates: number[];  // [lng, lat]
}


export interface GeoPoint {
  longitude: number;
  latitude: number;
}
