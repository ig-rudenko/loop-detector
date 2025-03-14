import {app} from '@/appInstance';

const basicLifeTime = 3000;

export function infoToast(title: string, body: string, lifeTime: number = basicLifeTime): void {
    app.config.globalProperties.$toast.add({
        severity: "info",
        summary: title,
        detail: body,
        life: lifeTime
    });
}

export function successToast(title: string, body: string, lifeTime: number = basicLifeTime): void {
    app.config.globalProperties.$toast.add({
        severity: "success",
        summary: title,
        detail: body,
        life: lifeTime
    });
}

export function errorToast(title: string, body: string, lifeTime: number = basicLifeTime): void {
    app.config.globalProperties.$toast.add({
        severity: "error",
        summary: title,
        detail: body,
        life: lifeTime
    });
}