<template>
  <q-page class="row items-center justify-evenly">
    <div style="max-width: 1100px">
      <group-zone-table @refresh="refresh" :key ="renderKey" :readOnly="false"/>
    </div>
  </q-page>
</template>

<script lang="ts">
import { Meta } from 'components/models';
import { defineComponent, ref } from '@vue/composition-api';
import GroupZoneTable from 'components/GroupZoneTable.vue';

export default defineComponent({
  components: { GroupZoneTable },
  name: 'GroupZonePage',
  data() {
    return {
      renderKey: 0
    }
  },
  setup() {
    const meta = ref<Meta>({
      totalCount: 1200
    });
    return { meta };
  },
  methods: {
    refresh () {
      this.renderKey ++;
    }
  }
});
</script>
