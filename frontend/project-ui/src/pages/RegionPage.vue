<template>
  <q-page class="row items-center justify-evenly">
    <div style="max-width: 1100px">
      <region-table @refresh="refresh" :key="renderKey" :readOnly="false"/>
    </div>
  </q-page>
</template>

<script lang="ts">
import { Meta } from 'components/models';
import { defineComponent, ref } from '@vue/composition-api';
import RegionTable from 'components/RegionTable.vue';

export default defineComponent({
  components: { RegionTable },
  name: 'PageIndex',
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
