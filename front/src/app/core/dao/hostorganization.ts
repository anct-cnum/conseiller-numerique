import {GeoPoint} from "./geo";


export interface HostOrganizationInput {
  type: string;
  hasCandidate: boolean;
  coachesRequested: number;
  startDate: Date;
  siret: string;
  name: string;
  contactFirstName: string;
  contactLastName: string;
  contactJob: string;
  contactEmail: string;
  contactPhone: string;
  recaptcha: string;

  geoName: string;
  zipCode: string;
  communeCode: string;
  departementCode: string;
  regionCode: string;
  location: GeoPoint;
}


export interface HostOrganizationOutput {
  type: string;
  hasCandidate: boolean;
  startDate: Date;
  name: string;
  contactFirstName: string;
  contactLastName: string;
  contactJob: string;
  contactEmail: string;
  contactPhone: string;

  updated: Date;
  created: Date;

  geoName: string;
  zipCode: string;
  communeCode: string;
  departementCode: string;
  regionCode: string;
  location: GeoPoint;
}
