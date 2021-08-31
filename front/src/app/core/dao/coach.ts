import {GeoPoint} from './geo';


export interface CoachInput {
  situationLooking: boolean;
  situationJob: boolean;
  situationLearning: boolean;
  situationGraduated: boolean;
  formation: string;
  hasExperience: boolean;
  maxDistance: number;
  startDate: Date;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  recaptcha: string;

  geoName: string;
  zipCode: string;
  communeCode: string;
  departementCode: string;
  regionCode: string;
  comCode: string;
  location: GeoPoint;
}


export interface CoachOutput {
  id: number;
  situationLooking: boolean;
  situationJob: boolean;
  situationLearning: boolean;
  situationGraduated: boolean;
  formation: string;
  hasExperience: boolean;
  maxDistance: number;
  startDate: Date;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;

  updated: Date;
  created: Date;

  geoName: string;
  zipCode: string;
  communeCode: string;
  departementCode: string;
  regionCode: string;
  location: GeoPoint;
}
