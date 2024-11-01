import {createRouter, createWebHistory} from "vue-router";

import Home from "@/pages/Home.vue";
import Login from "@/pages/Login.vue";
import LoopGraph from "@/pages/LoopGraph.vue";
import CurrentLoop from "@/pages/CurrentLoop.vue";
import LoopsHistory from "@/pages/LoopsHistory.vue";
import Notifications from "@/pages/Notifications.vue";


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: "/", component: Home},
        {path: "/login", component: Login},
        {path: "/loops/current", component: CurrentLoop},
        {path: "/loops/history", component: LoopsHistory},
        {path: "/loop/stored/:name", component: LoopGraph, name: "loop"},
        {path: "/notifications", component: Notifications, name: "notifications"}
    ],
});

export default router;