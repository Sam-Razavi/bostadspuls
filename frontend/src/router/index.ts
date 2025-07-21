import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "dashboard",
      component: () => import("../views/DashboardView.vue"),
    },
    {
      path: "/trends",
      name: "trends",
      component: () => import("../views/TrendsView.vue"),
    },
    {
      path: "/regions",
      name: "regions",
      component: () => import("../views/RegionsView.vue"),
    },
    {
      path: "/map",
      name: "map",
      component: () => import("../views/MapView.vue"),
    },
    {
      path: "/distribution",
      name: "distribution",
      component: () => import("../views/DistributionView.vue"),
    },
    {
      path: "/explore",
      name: "explore",
      component: () => import("../views/ExploreView.vue"),
    },
  ],
});

export default router;
