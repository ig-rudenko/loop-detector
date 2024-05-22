import {createRouter, createWebHistory, Router, RouteRecordRaw} from "vue-router";

import Login from "@/pages/Login.vue";
import LoopGraph from "@/pages/LoopGraph.vue";

const routes: RouteRecordRaw[] = [
    { path: "/", component: LoopGraph },
    { path: "/login", component: Login },
]

const router: Router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;