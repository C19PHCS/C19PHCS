export interface Todo {
  id: number;
  content: string;
}

export interface Meta {
  totalCount: number;
}

export interface Person {
  medicareNumber: string,
  firstName: string,
  lastName: string,
  dateOfBirth: string,
  phoneNumber: string,
  email: string,
  address: string,
  city: string,
  province: string
  postalCode: string
  citizenShip: string
  country: string
  fatherMedicare: string
  motherMedicare: string
}

export interface PublicHealthWorker {
  medicareNumber: string,
  firstName: string,
  lastName: string,
  dateOfBirth: string,
  phoneNumber: string,
  email: string,
  address: string,
  city: string
  province: string
  healthWorkerID: number | null
  publicHealthCareCenterId: number | null
}

export interface HealthCareCenter {
  id: number | null;
  name: string | null;
  address: string | null;
  webAddress: string | null;
  phoneNumber: string | null;
  type: string | null
  city: string | null
  province: string | null
  country: string | null
  driveThru: number | null
  postalCode: string | null
}

export interface GroupZone {
  groupID: number|null
  groupName: string
}

export interface Region {
  name: string | null
}

export interface Alert {
  regionName: string | null
  alertLevelId: number | null
}

export interface Survey {
  medicareNumber: string | null
  dateTime: Date | null
  temprature: number | null
  fever: boolean
  cough: boolean
  shortnessOfBreath: boolean
  lossOfTaste: boolean
  nausea: boolean
  stomachAche: boolean
  diarrhea: boolean
  vomiting: boolean
  headache: boolean
  musclePain: boolean
  soreThroat: boolean
  otherSymptomes: string
}

export interface Symptoms {
  fever: boolean
  cough: boolean
  shortnessOfBreath: boolean
  lossOfTaste: boolean
  nausea: boolean
  stomachAche: boolean
  diarrhea: boolean
  vomiting: boolean
  headache: boolean
  musclePain: boolean
  soreThroat: boolean
  otherSymptoms: string
}

export interface SymptomsSearchCriteria {
  medicareNumber: string
  date: Date
}

export interface SymptomSurvey {
  medicareNumber: string,
  dateOfBirth: string,
  temperature: number,
  symptoms: Symptoms
}

export interface Messages {
  id: number
  dateTime: Date
  email: string
  name: string
  region: string
  oldAlertLevel: number
  newAlertLevel: number
  healthRecomendation: string
  description: string
  testResult: boolean
}


