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
  city: string,
  province: string
  workerId: number | null;
  publicHealthCareCenterId: number | null;
}


