import {CoachOutput} from './coach';
import {HostOrganizationOutput} from './hostorganization';


export interface MatchingOutput {
  id: number;
  key: string;
  coach: CoachOutput;
  host: HostOrganizationOutput;
  coachAccepted: Date;
  coachRejected: Date;
  hostAccepted: Date;
  hostRejected: Date;
  created: Date;
}
