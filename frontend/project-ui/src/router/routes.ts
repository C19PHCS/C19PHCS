import { RouteConfig } from 'vue-router';

const routes: RouteConfig[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/people', component: () => import('pages/PersonPage.vue') },
      { path: '/messages', component: () => import('pages/MessagesPage.vue') },
      { path: '/healthcenter', component: () => import('pages/HospitalPage.vue') },
      { path: '/regions', component: () => import('pages/RegionPage.vue') },
      { path: '/groupzones', component: () => import('pages/GroupZonePage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
];

export default routes;
