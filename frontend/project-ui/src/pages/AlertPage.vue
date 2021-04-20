<template>
  <q-page class="row items-center justify-evenly">
    <div style="max-width: 1100px">
      <alert-table @refresh="refresh" :key="renderKey" :readOnly="false"/>
    </div>
  </q-page>
</template>

<script lang="ts">
import { Meta } from 'components/models';
import { defineComponent, ref } from '@vue/composition-api';
import AlertTable from 'components/AlertTable.vue'

export default defineComponent({
  components: { AlertTable },
  name: 'Alerts',
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
