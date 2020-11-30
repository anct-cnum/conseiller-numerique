import {GeoPoint} from './geo';


export interface GeoCommune {
  name: string;
  code: string;
  zipCodes: string[];
  departementCode: string;
  regionCode: string;
  center: GeoPoint;
}


export interface ZipCodeWithCommune {
  zipCode: string;
  commune: GeoCommune;
}
