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
  workerId: number | null
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
}

export interface GroupZone {
  groupID: number|null
  groupName: string
}

export interface Region {
  name: string | null
}



