import {createRouter, createWebHistory, Router, RouteRecordRaw} from "vue-router";

import Login from "@/pages/Login.vue";
import Home from "@/pages/Home.vue";
import CurrentLoop from "@/pages/CurrentLoop.vue";
import LoopGraph from "@/pages/LoopGraph.vue";

const routes: RouteRecordRaw[] = [
    { path: "/", component: Home },
    { path: "/login", component: Login },
    { path: "/currentLoop", component: CurrentLoop },
    { path: "/loop/stored/:name", component: LoopGraph, name: "storedLoop" },
]

const router: Router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;