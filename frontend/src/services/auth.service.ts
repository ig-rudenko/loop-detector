import api from "./api";
import TokenService from "./token.service";
import {LoginUser, UserTokens} from "@/services/user";
import UserService from "@/services/user.service";

class AuthService {
    login(user: LoginUser) {
        return api
            .post("/auth/token", {
                username: user.username,
                password: user.password
            })
            .then(
                response => {
                    if (response.data.accessToken) {
                        TokenService.setUser(
                            new UserTokens(
                                response.data.access,
                                response.data.refresh || null
                            )
                        );
                    }
                    return response
                },
                reason => {
                    return reason
                }
            );
    }

    logout() {
        TokenService.removeUser();
        UserService.removeUser();
    }

}

export default new AuthService();