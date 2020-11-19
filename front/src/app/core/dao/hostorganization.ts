

export interface HostOrganizationInput {
  type: string;
  hasCandidate: boolean;
  startDate: Date;
  name: string;
  zipCode: string;
  contactFirstName: string;
  contactLastName: string;
  contactJob: string;
  contactEmail: string;
  contactPhone: string;
  recaptcha: string;
}


export interface HostOrganizationOutput {
  type: string;
  hasCandidate: boolean;
  startDate: Date;
  name: string;
  zipCode: string;
  contactFirstName: string;
  contactLastName: string;
  contactJob: string;
  contactEmail: string;
  contactPhone: string;

  updated: Date;
  created: Date;
}
