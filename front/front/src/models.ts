export interface AuthModel{
    username: string;
    password: string;
}

export interface Token{
    refresh: string;
    access: string;
}