import { UserConnection } from "./user-connection.type";

export type User = {
    firstName: string,
    lastName: string,
    email: string,
    password?: string,
    roles?: any[],
    connections: UserConnection[],
}