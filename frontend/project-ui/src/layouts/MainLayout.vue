<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Main Project
        </q-toolbar-title>
<!-- 
        <div><q-btn label="IncrementDate" @click="incrementDate" color="secondary" type="submit" /></div>
        <h6>{{today.date}}</h6> -->
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8"
        >
          Essential Links
        </q-item-label>
        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import EssentialLink from 'components/EssentialLink.vue'

const linksData = [
  {
    title: 'People',
    caption: '',
    icon: 'person',
    link: '#/people'
  },
  {
    title: 'Hospitals',
    caption: '',
    icon: 'house',
    link: '#/healthcenter'
  },
  {
    title: 'Region',
    caption: '',
    icon: 'map',
    link: '#/regions'
  },
  {
    title: 'Messages',
    caption: '',
    icon: 'email',
    link: '#/messages'
  },
  {
    title: 'Group zone',
    caption: '',
    icon: 'group',
    link: '#/groupzones'
  },
  {
    title: 'Alerts',
    caption: '',
    icon: 'notifications',
    link: '#/alerts'
  }
];

import { defineComponent, ref } from '@vue/composition-api';
import { Today } from 'src/components/models';

export default defineComponent({
  name: 'MainLayout',
  components: { EssentialLink },
  setup() {
    const leftDrawerOpen = ref(false);
    const essentialLinks = ref(linksData);

    return {leftDrawerOpen, essentialLinks}
  },
  data() {
    return {
      today: {} as Today
    };
  },
  methods: {
    async incrementDate(){
      await this.$axios
      .get('/increment-date/')
      .then(response => (this.today = response.data as Today));
    }
  }
});
</script>
