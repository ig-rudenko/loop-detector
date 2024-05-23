import {User} from "@/services/user";

class UserService {
    getUser(): User | null {
        const data = localStorage.getItem("user")
        if (data) {
            return JSON.parse(data)
        }
        return null
    }

    setUser(user: User): void {
        localStorage.setItem("user", JSON.stringify(user));
    }

    removeUser(): void {
        localStorage.removeItem("user");
    }

}

export default new UserService();