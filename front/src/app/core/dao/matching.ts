import {CoachOutput} from './coach';
import {HostOrganizationOutput} from './hostorganization';


export interface MatchingOutput {
  id: number;
  key: string;
  coach: CoachOutput;
  host: HostOrganizationOutput;
  coachContactOk: boolean;
  hostContactOk: boolean;
  hostMeetingOk: boolean;
  hostInterviewResultOk: boolean;
  created: Date;
}
