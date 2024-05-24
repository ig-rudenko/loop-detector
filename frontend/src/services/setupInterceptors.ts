import axiosInstance from "./api";
import TokenService from "./token.service";
import router from "@/router";

const setup = (store: any) => {
    axiosInstance.interceptors.request.use(
        (config) => {
            const token = TokenService.getLocalAccessToken();
            if (token) {
                config.headers["Authorization"] = 'Bearer ' + token;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    axiosInstance.interceptors.response.use(
        (res) => {
            return res;
        },
        async (err) => {
            const originalConfig = err.config;

            if ((originalConfig.url !== "/api/v1/auth/token" || originalConfig.url !== "/api/v1/auth/users") && err.response) {
                // Access Token was expired
                if (err.response.status === 401 && !originalConfig._retry) {
                    originalConfig._retry = true;
                    originalConfig.headers["Content-Type"] = "application/json";

                    try {
                        const refreshToken = TokenService.getLocalRefreshToken()
                        if (!refreshToken) {
                            store.dispatch("auth/logout")
                            await router.push("/login");
                            return Promise.reject(err)
                        }
                        const rs = await axiosInstance.post(
                            "auth/token/refresh",
                            { refresh: refreshToken },
                            originalConfig
                        )
                            .then(
                                value => value,
                                reason => reason.response
                            )
                            .catch(reason => reason.response);

                        if (rs.status !== 200) {
                            store.dispatch("auth/logout")
                            await router.push("/login");
                            return Promise.reject(err)
                        }

                        const { access, refresh } = rs.data;

                        store.dispatch('auth/refreshTokens', access, refresh);
                        TokenService.updateLocalTokens(access, refresh);

                        return axiosInstance(originalConfig);
                    } catch (_error) {
                        localStorage.removeItem("user")
                        return Promise.reject(_error);
                    }
                }
            }

            return Promise.reject(err);
        }
    );
};

export default setup;