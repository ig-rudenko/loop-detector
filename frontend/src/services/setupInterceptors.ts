import axiosInstance from "./api";
import TokenService from "./token.service";
import router from "@/router";
import {AxiosError, AxiosResponse, InternalAxiosRequestConfig} from "axios";


interface InterceptorInternalAxiosRequestConfig extends InternalAxiosRequestConfig {
    _retry?: boolean;
}


async function logoutUser(store: any, resp: AxiosError<any>): Promise<AxiosResponse> {
    store.dispatch("auth/logout")
    await router.push("/login");
    return Promise.reject(resp);
}


async function checkNotEnoughPermissions(store: any, resp: AxiosError<any>): Promise<undefined | AxiosResponse<any>> {
    if (resp.response && resp.response.status === 403 && String(resp.response.data?.detail).includes("Not enough permissions")) {
        return await logoutUser(store, resp)
    }
    return
}


async function checkRefreshTokens(store: any, resp: AxiosError<any>): Promise<undefined | AxiosResponse<any>> {
    const originalConfig = <InterceptorInternalAxiosRequestConfig>resp.config!;

    // Пропускаем URL, который отвечает за получение токена, чтобы не было рекурсии.
    if (originalConfig.url == "/api/v1/auth/token") return;

    // Пропускаем все коды ошибок кроме 401, а также повторные запросы.
    if (!resp.response || resp.response.status !== 401 || originalConfig._retry) return;

    // Access Token was expired
    originalConfig._retry = true;  // Указываем, что это повторный запрос.
    originalConfig.headers["Content-Type"] = "application/json";

    try {
        // Получаем refresh токен
        const refreshToken = TokenService.getLocalRefreshToken()
        if (!refreshToken) {
            // Падаем в на страницу входа, если нет токена.
            return await logoutUser(store, resp)
        }

        // Запрос на обновление токена.
        const rs = await axiosInstance.post("auth/token/refresh", {refresh: refreshToken}, originalConfig)
            .then(value => value, reason => reason.response)
            .catch(reason => reason.response);

        // Если произошла ошибка в обновлении access токена,
        // то refresh токен неверный, надо залогиниться заново.
        if (rs.status !== 200) {
            return await logoutUser(store, resp)
        }

        const {access, refresh} = rs.data;
        // Обновляем access и refresh токены.
        store.dispatch('auth/refreshTokens', rs.data);
        TokenService.updateLocalTokens(access, refresh);
        return axiosInstance(originalConfig);

    } catch (_error) {
        return await logoutUser(store, resp)
    }
}

const setup = (store: any) => {
    axiosInstance.interceptors.request.use(
        (config) => {
            const token = TokenService.getLocalAccessToken();
            if (token) {
                config.headers["Authorization"] = 'Bearer ' + token;
            }
            return config;
        },
        error => Promise.reject(error)
    );

    axiosInstance.interceptors.response.use(
        res => res,
        async (err: AxiosError<any>) => {

            let resp = await checkNotEnoughPermissions(store, err);
            if (resp) return resp;

            resp = await checkRefreshTokens(store, err);
            if (resp) return resp;

            return Promise.reject(err);
        }
    );
};

export default setup;