<template>
  <div class="col">
    <div class="row justify-between">
      <div class="col">
        <div class="row justify-start q-gutter-sm">
          <div class="q-table__title text-secondary">
            {{ title }}
          </div>
          <q-btn
            v-if="!hideAddButton"
            color="secondary"
            dense
            outline
            icon="add"
            round
            @click="$emit('create')"
          >
            <q-tooltip>{{ createTooltip }}</q-tooltip>
          </q-btn>
          <slot name="extra-actions"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'TableHeader',
  props: {
    title: {
      type: String
    },
    createTooltip: {
      type: String
    },
    hideAddButton: {
      type: Boolean
    }
  }
});
</script>