

export interface CoachInput {
  situationLooking: boolean;
  situationJob: boolean;
  situationLearning: boolean;
  situationGraduated: boolean;
  formation: string;
  hasExperience: boolean;
  zipCode: string;
  maxDistance: number;
  startDate: Date;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  recaptcha: string;
}


export interface CoachOutput {
  id: number;
  situationLooking: boolean;
  situationJob: boolean;
  situationLearning: boolean;
  situationGraduated: boolean;
  formation: string;
  hasExperience: boolean;
  zipCode: string;
  maxDistance: number;
  startDate: Date;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;

  updated: Date;
  created: Date;
}
